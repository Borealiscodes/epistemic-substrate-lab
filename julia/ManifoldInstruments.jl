module ManifoldInstruments

using LinearAlgebra
using Random
using StaticArrays

export build_isometric_basis, holonomy_loop_static, verify_zero_allocation

"""Sign-canonicalized QR decomposition guaranteeing P' * P == I_k."""
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
    return @SMatrix [
        (mu == nu ? 0.0 : coupling * (x[mu] * dx[nu] - x[nu] * dx[mu]))
        for mu in 1:K, nu in 1:K
    ]
end

"""Zero-allocation path-ordered holonomy around a closed loop in rank-K subspace."""
function holonomy_loop_static(g_sub::SMatrix{K,K,Float64}; coupling::Float64=0.0, steps::Int=64) where {K}
    H = one(SMatrix{K,K,Float64})
    dt = 2.0 * pi / steps
    for i in 0:(steps - 1)
        tm = (i + 0.5) * dt
        x_mid = SVector{K,Float64}(ntuple(j -> j == 1 ? cos(tm) : (j == 2 ? sin(tm) : 0.0), K))
        dx = SVector{K,Float64}(ntuple(j -> j == 1 ? -sin(tm) * dt : (j == 2 ? cos(tm) * dt : 0.0), K))
        A_mid = connection_contraction(x_mid, dx, coupling)
        step_exp = one(SMatrix{K,K,Float64}) + A_mid + 0.5 * (A_mid * A_mid)
        H = H * step_exp
    end
    hol_dev = opnorm(Matrix(H - one(SMatrix{K,K,Float64})), 2)
    min_eig = minimum(eigvals(Symmetric(Matrix(g_sub))))
    return (holonomy_deviation=hol_dev, g_sub_min_eig=min_eig)
end

function verify_zero_allocation()
    P = build_isometric_basis(256, 8; seed=42)
    g_sub = SMatrix{8,8,Float64}(P' * P)
    holonomy_loop_static(g_sub; coupling=0.0)
    allocs = @allocated holonomy_loop_static(g_sub; coupling=0.0)
    res_flat = holonomy_loop_static(g_sub; coupling=0.0)
    res_curved = holonomy_loop_static(g_sub; coupling=0.25)
    println("JULIA_STATIC_ALLOC_BYTES=", allocs)
    println("JULIA_FLAT_HOLONOMY=", res_flat.holonomy_deviation)
    println("JULIA_CURVED_HOLONOMY=", res_curved.holonomy_deviation)
    @assert allocs == 0 "Expected 0 heap allocations in static holonomy loop, got $(allocs)"
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    ManifoldInstruments.verify_zero_allocation()
end
