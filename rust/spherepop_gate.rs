use std::env;
use std::process;

#[derive(Debug, PartialEq, Eq)]
enum Disposition {
    Collapsed,
    Refused(&'static str),
}

struct V8SelfHealingState {
    corrupted_patch_count: usize,
    target_established: bool,
    burden_within_budget: bool,
    post_repair_coboundary_zero: bool,
}

fn evaluate_self_healing_pass(s: &V8SelfHealingState) -> Disposition {
    if s.corrupted_patch_count == 0 {
        Disposition::Collapsed
    } else if s.corrupted_patch_count > 1 {
        Disposition::Refused("BYZANTINE_MULTI_PATCH_OBSTRUCTION")
    } else if !s.target_established {
        Disposition::Refused("UNESTABLISHED")
    } else if !s.burden_within_budget {
        Disposition::Refused("MAINTENANCE_BUDGET_EXCEEDED")
    } else if !s.post_repair_coboundary_zero {
        Disposition::Refused("REPAIR_COBOUNDARY_OBSTRUCTION")
    } else {
        Disposition::Collapsed
    }
}

fn run_self_tests() {
    let clean = V8SelfHealingState {
        corrupted_patch_count: 0,
        target_established: true,
        burden_within_budget: true,
        post_repair_coboundary_zero: true,
    };
    assert_eq!(evaluate_self_healing_pass(&clean), Disposition::Collapsed);

    let single_healed = V8SelfHealingState {
        corrupted_patch_count: 1,
        target_established: true,
        burden_within_budget: true,
        post_repair_coboundary_zero: true,
    };
    assert_eq!(evaluate_self_healing_pass(&single_healed), Disposition::Collapsed);

    let phantom = V8SelfHealingState {
        corrupted_patch_count: 1,
        target_established: false,
        burden_within_budget: true,
        post_repair_coboundary_zero: true,
    };
    assert_eq!(
        evaluate_self_healing_pass(&phantom),
        Disposition::Refused("UNESTABLISHED")
    );

    let byzantine = V8SelfHealingState {
        corrupted_patch_count: 2,
        target_established: true,
        burden_within_budget: true,
        post_repair_coboundary_zero: true,
    };
    assert_eq!(
        evaluate_self_healing_pass(&byzantine),
        Disposition::Refused("BYZANTINE_MULTI_PATCH_OBSTRUCTION")
    );
}

fn main() {
    run_self_tests();
    let args: Vec<String> = env::args().collect();
    if args.len() == 5 {
        let state = V8SelfHealingState {
            corrupted_patch_count: args[1].parse().unwrap_or(99),
            target_established: args[2] == "true",
            burden_within_budget: args[3] == "true",
            post_repair_coboundary_zero: args[4] == "true",
        };
        match evaluate_self_healing_pass(&state) {
            Disposition::Collapsed => println!("COLLAPSE"),
            Disposition::Refused(reason) => println!("REFUSE:{}", reason),
        }
    } else if args.len() == 1 {
        println!("RUST_SPHEREPOP_V8_GATE_VERIFIED=true");
    } else {
        eprintln!("Usage: spherepop_gate [<corrupted_count> <established> <budget_ok> <coboundary_ok>]");
        process::exit(2);
    }
}
