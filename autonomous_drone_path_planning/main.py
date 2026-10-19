from pathlib import Path
from environment import create_environment
from path_planning import build_candidate_strategies
from game_theory import run_baseline, run_best_response
from metrics import summarize_solution, save_metrics
from visualization import (
    plot_solution,
    plot_comparison,
    plot_utility_evolution,
    plot_utility_breakdown,
    plot_weight_summary,
    plot_weight_sensitivity,
)


def main():
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    env = create_environment()
    strategies = build_candidate_strategies(env, k=5)

    baseline_routes = run_baseline(env, strategies)
    gt_routes, iteration_log = run_best_response(
        env, strategies, max_iterations=30
    )

    baseline_metrics = summarize_solution(env, baseline_routes)
    gt_metrics = summarize_solution(env, gt_routes)

    save_metrics(
        results_dir / "metrics.csv",
        baseline_metrics,
        gt_metrics,
    )

    import pandas as pd
    pd.DataFrame(iteration_log).to_csv(
        results_dir / "iteration_log.csv", index=False
    )

    plot_solution(
        env,
        baseline_routes,
        title="Baseline: Independent Route Selection",
        filename=results_dir / "baseline_paths.png",
    )

    plot_solution(
        env,
        gt_routes,
        title="Game-Theoretic Multi-Drone Route Planning",
        filename=results_dir / "final_paths.png",
    )

    plot_comparison(
        baseline_metrics,
        gt_metrics,
        filename=results_dir / "comparison.png",
    )

    plot_utility_evolution(
        iteration_log,
        filename=results_dir / "utility_evolution.png",
    )

    plot_utility_breakdown(
        env,
        gt_routes,
        title="Game-Theoretic Utility Breakdown",
        filename=results_dir / "utility_breakdown.png",
    )

    plot_weight_summary(
        filename=results_dir / "weight_summary.png",
    )

    plot_weight_sensitivity(
        env,
        gt_routes,
        filename=results_dir / "weight_sensitivity.png",
    )

    print("\n=== AUTONOMOUS DRONE PATH PLANNING ===")
    print("Baseline:", baseline_metrics)
    print("Game Theory:", gt_metrics)
    print("\nResults saved in:", results_dir.resolve())


if __name__ == "__main__":
    main()
