module ManifoldInstruments

using LinearAlgebra
using Random
using StaticArrays

export build_isometric_basis, holonomy_integrate_static, holonomy_loop_static,
       static_edge_coboundary_sq, sheaf_laplacian_spectrum,
       sheaf_edge_obstruction_profile, compose_depth_holonomy_static,
       verify_zero_allocation

function build_isometric_basis(D::Int, k::Int; seed::Int=42)::Matrix{Float64}
    rng = MersenneTwister(seed)
    A = randn(rng, D, k)
    F = qr(A)
    Q = Matrix(F.Q)[:, 1:k]
    R_diag = diag(F.R)[1:k]
    signs = ifelse.(R_diag .>= 0.0, 1.0, -1.0)
    return Q .* signs'
end

@inline function connection_contraction(x::SVector{K,Float64}, dx::SVector{K,Float64}, coupling::Float64) where {K}
    if coupling == 0.0
        return zero(SMatrix{K,K,Float64})
    end
    return SMatrix{K,K,Float64}(ntuple(Val(K * K)) do idx
        mu = mod1(idx, K)
        nu = cld(idx, K)
        mu == nu ? 0.0 : coupling * (x[mu] * dx[nu] - x[nu] * dx[mu])
    end)
end

"""Purely stack-allocated path-ordered holonomy integrator (0 heap bytes)."""
function holonomy_integrate_static(g_sub::SMatrix{K,K,Float64}; coupling::Float64=0.0, steps::Int=64)::SMatrix{K,K,Float64} where {K}
    H = one(SMatrix{K,K,Float64})
    dt = 2.0 * pi / steps
    for i in 0:(steps - 1)
        tm = (i + 0.5) * dt
        x_mid = SVector{K,Float64}(ntuple(j -> j == 1 ? cos(tm) : (j == 2 ? sin(tm) : 0.0), Val(K)))
        dx = SVector{K,Float64}(ntuple(j -> j == 1 ? -sin(tm) * dt : (j == 2 ? cos(tm) * dt : 0.0), Val(K)))
        A_mid = connection_contraction(x_mid, dx, coupling)
        step_exp = one(SMatrix{K,K,Float64}) + A_mid + 0.5 * (A_mid * A_mid)
        H = H * step_exp
    end
    return H
end

function holonomy_loop_static(g_sub::SMatrix{K,K,Float64}; coupling::Float64=0.0, steps::Int=64) where {K}
    H = holonomy_integrate_static(g_sub; coupling=coupling, steps=steps)
    hol_dev = opnorm(H - one(SMatrix{K,K,Float64}), 2)
    min_eig = minimum(eigvals(Symmetric(g_sub)))
    return (holonomy_deviation=hol_dev, g_sub_min_eig=min_eig)
end

"""Zero-allocation cellular sheaf edge coboundary squared norm."""
@inline function static_edge_coboundary_sq(
    R_i::SMatrix{M,K,Float64}, s_i::SVector{K,Float64},
    R_j::SMatrix{M,K,Float64}, s_j::SVector{K,Float64}
)::Float64 where {M,K}
    diff = (R_j * s_j) - (R_i * s_i)
    return dot(diff, diff)
end

"""Zero-allocation closed-loop depth holonomy composer over N-1 static transport operators."""
function compose_depth_holonomy_static(
    R_steer::NTuple{L,SMatrix{K,K,Float64}},
    R_base_rev::NTuple{L,SMatrix{K,K,Float64}}
)::SMatrix{K,K,Float64} where {L,K}
    H = one(SMatrix{K,K,Float64})
    for t in 1:L
        H = R_steer[t] * H
    end
    for t in 1:L
        H = R_base_rev[t] * H
    end
    return H
end

"""Constructs block Sheaf Laplacian L_F = delta0' * delta0 for a cyclic cover."""
function sheaf_laplacian_spectrum(patches::Vector{Matrix{Float64}})
    m = length(patches)
    k = size(first(patches), 2)
    delta0 = zeros(Float64, m * k, m * k)
    for i in 1:m
        j = mod1(i + 1, m)
        row_rng = ((i - 1) * k + 1):(i * k)
        col_i = ((i - 1) * k + 1):(i * k)
        col_j = ((j - 1) * k + 1):(j * k)
        delta0[row_rng, col_i] .= -(patches[j]' * patches[i])
        delta0[row_rng, col_j] .= Matrix{Float64}(I, k, k)
    end
    L_F = Symmetric(delta0' * delta0)
    evals = eigvals(L_F)
    non_zero = filter(v -> v > 1e-10, evals)
    lambda_1 = isempty(non_zero) ? 0.0 : minimum(non_zero)
    return (delta0=delta0, L_F=Matrix(L_F), lambda_1=lambda_1, max_eig=maximum(evals))
end

"""Localizes coboundary energy across each edge (i, j) to identify which patch overlap caused REFUSE."""
function sheaf_edge_obstruction_profile(patches::Vector{Matrix{Float64}}, sections::Vector{Vector{Float64}})
    m = length(patches)
    edge_norms = Vector{Float64}(undef, m)
    for i in 1:m
        j = mod1(i + 1, m)
        diff = (patches[j]' * (patches[j] * sections[j])) - (patches[j]' * (patches[i] * sections[i]))
        edge_norms[i] = norm(diff, 2)
    end
    worst_edge = argmax(edge_norms)
    return (edge_norms=edge_norms, worst_edge_idx=worst_edge, max_edge_norm=edge_norms[worst_edge], total_norm=norm(edge_norms, 2))
end

function verify_zero_allocation()
    P = build_isometric_basis(256, 8; seed=42)
    g_sub = SMatrix{8,8,Float64}(P' * P)
    holonomy_integrate_static(g_sub; coupling=0.25)
    allocs_hol = @allocated holonomy_integrate_static(g_sub; coupling=0.25)

    R_i = SMatrix{4,8,Float64}(randn(MersenneTwister(1), 4, 8))
    R_j = SMatrix{4,8,Float64}(randn(MersenneTwister(2), 4, 8))
    s_i = SVector{8,Float64}(ntuple(idx -> Float64(idx) * 0.1, Val(8)))
    s_j = SVector{8,Float64}(ntuple(idx -> Float64(idx) * 0.12, Val(8)))
    static_edge_coboundary_sq(R_i, s_i, R_j, s_j)
    allocs_sheaf = @allocated static_edge_coboundary_sq(R_i, s_i, R_j, s_j)

    R_tup = ntuple(_ -> one(SMatrix{8,8,Float64}), Val(23))
    compose_depth_holonomy_static(R_tup, R_tup)
    allocs_depth = @allocated compose_depth_holonomy_static(R_tup, R_tup)

    res_flat = holonomy_loop_static(g_sub; coupling=0.0)
    res_curved = holonomy_loop_static(g_sub; coupling=0.25)
    patches = [build_isometric_basis(64, 8; seed=10 + i) for i in 1:4]
    spec = sheaf_laplacian_spectrum(patches)

    x_test = randn(MersenneTwister(99), 64)
    secs = [P_i' * x_test for P_i in patches]
    first(secs) .+= 0.5 .* randn(MersenneTwister(100), 8)
    loc = sheaf_edge_obstruction_profile(patches, secs)

    println("JULIA_HOLONOMY_ALLOC_BYTES=", allocs_hol)
    println("JULIA_SHEAF_EDGE_ALLOC_BYTES=", allocs_sheaf)
    println("JULIA_DEPTH_HOLONOMY_ALLOC_BYTES=", allocs_depth)
    println("JULIA_FLAT_HOLONOMY=", res_flat.holonomy_deviation)
    println("JULIA_CURVED_HOLONOMY=", res_curved.holonomy_deviation)
    println("JULIA_SHEAF_LAMBDA_1=", spec.lambda_1)
    println("JULIA_WORST_OBSTRUCTION_EDGE=", loc.worst_edge_idx)
    println("JULIA_MAX_EDGE_NORM=", loc.max_edge_norm)

    @assert allocs_hol == 0 "Expected 0 bytes for holonomy, got $(allocs_hol)"
    @assert allocs_sheaf == 0 "Expected 0 bytes for sheaf edge coboundary, got $(allocs_sheaf)"
    @assert allocs_depth == 0 "Expected 0 bytes for depth holonomy, got $(allocs_depth)"
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    ManifoldInstruments.verify_zero_allocation()
end
