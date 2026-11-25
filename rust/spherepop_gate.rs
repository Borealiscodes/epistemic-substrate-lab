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
    let mut args = env::args().skip(1);
    let count_arg = args.next();
    if let Some(c_str) = count_arg {
        let est_str = args.next().unwrap_or_default();
        let bud_str = args.next().unwrap_or_default();
        let cob_str = args.next().unwrap_or_default();
        let state = V8SelfHealingState {
            corrupted_patch_count: c_str.parse().unwrap_or(99),
            target_established: est_str == "true",
            burden_within_budget: bud_str == "true",
            post_repair_coboundary_zero: cob_str == "true",
        };
        match evaluate_self_healing_pass(&state) {
            Disposition::Collapsed => println!("COLLAPSE"),
            Disposition::Refused(reason) => println!("REFUSE:{}", reason),
        }
    } else if env::args().len() == 1 {
        println!("RUST_SPHEREPOP_V8_GATE_VERIFIED=true");
    } else {
        eprintln!("Usage: spherepop_gate [<corrupted_count> <established> <budget_ok> <coboundary_ok>]");
        process::exit(2);
    }
}
