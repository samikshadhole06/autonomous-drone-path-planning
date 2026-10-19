import matplotlib.pyplot as plt
import pandas as pd
import game_theory as gt
from matplotlib.patches import Rectangle

from game_theory import utility_components


def plot_solution(env, routes, title, filename):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Obstacles
    for x, y in env.obstacles:
        ax.add_patch(Rectangle((x - .5, y - .5), 1, 1))

    # Surveillance zones
    zone_markers = ["S1", "S2", "S3", "S4", "S5"]
    for zone_name, cells in env.surveillance_zones.items():
        xs = [p[0] for p in cells]
        ys = [p[1] for p in cells]
        ax.scatter(xs, ys, marker="s", s=45, alpha=0.35)
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        ax.text(cx, cy, zone_name, ha="center", va="center", fontsize=9)

    markers = ["o", "^", "D", "s", "P"]

    for idx, drone in enumerate(env.drones):
        route = routes[drone.name]
        path = route["path"]
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]

        ax.plot(
            xs, ys,
            linewidth=2,
            marker=".",
            markersize=5,
            label=f"{drone.name} → {route['target']}"
        )
        ax.scatter(
            [drone.start[0]],
            [drone.start[1]],
            s=120,
            marker=markers[idx],
            edgecolors="black",
            label=f"{drone.name} start"
        )

        ax.scatter(
            [path[-1][0]],
            [path[-1][1]],
            s=120,
            marker="X",
            edgecolors="black"
        )

    ax.set_xlim(-1, env.width)
    ax.set_ylim(-1, env.height)
    ax.set_aspect("equal")
    ax.set_xticks(range(0, env.width, 2))
    ax.set_yticks(range(0, env.height, 2))
    ax.grid(True, alpha=0.2)
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.set_title(title)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3)
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


def plot_comparison(baseline, game_theory, filename):
    metrics = ["distance", "energy", "conflicts", "coverage"]
    labels = ["Distance", "Energy", "Conflicts", "Coverage (%)"]

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.ravel()

    for ax, metric, label in zip(axes, metrics, labels):
        values = [
            baseline[metric],
            game_theory[metric],
        ]
        ax.bar(["Baseline", "Game Theory"], values)
        ax.set_title(label)
        ax.grid(axis="y", alpha=0.2)

    fig.suptitle("Independent Planning vs Game-Theoretic Planning")
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


def plot_utility_evolution(iteration_log, filename):
    if not iteration_log:
        return

    df = pd.DataFrame(iteration_log)
    fig, ax = plt.subplots(figsize=(10, 6))

    for drone_name, group in df.groupby("drone"):
        x = group["iteration"]
        ax.plot(
            x,
            group["old_utility"],
            label=f"{drone_name} old utility",
            linestyle="--",
            alpha=0.7,
            marker="o",
        )
        ax.plot(
            x,
            group["new_utility"],
            label=f"{drone_name} new utility",
            marker="o",
        )

    ax.set_title("Utility Value Across Iterations")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Utility")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best")
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


def plot_utility_breakdown(env, routes, title, filename):
    fig, axes = plt.subplots(1, len(env.drones), figsize=(14, 5), squeeze=False)
    axes = axes.ravel()

    for idx, drone in enumerate(env.drones):
        other_routes = [
            routes[d.name] for d in env.drones if d.name != drone.name
        ]
        components = utility_components(routes[drone.name], env, other_routes)

        contribution_names = [
            "Coverage",
            "Distance",
            "Energy",
            "Conflict",
            "Target overlap",
        ]
        contribution_values = [
            components["coverage_term"],
            -components["distance_term"],
            -components["energy_term"],
            -components["conflict_term"],
            -components["target_overlap_term"],
        ]

        ax = axes[idx]
        ax.bar(contribution_names, contribution_values, color=["green", "orange", "purple", "red", "brown"])
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title(f"{drone.name} Utility Breakdown")
        ax.set_ylabel("Weighted contribution")
        ax.grid(axis="y", alpha=0.2)

    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


def plot_weight_summary(filename):
    weight_names = [
        "Coverage",
        "Distance",
        "Energy",
        "Conflict",
        "Target overlap",
    ]
    values = [
        gt.COVERAGE_WEIGHT,
        gt.DISTANCE_WEIGHT,
        gt.ENERGY_WEIGHT,
        gt.CONFLICT_WEIGHT,
        gt.TARGET_OVERLAP_WEIGHT,
    ]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(weight_names, values, color=["#4CAF50", "#FF9800", "#9C27B0", "#F44336", "#795548"])
    ax.set_title("Current Utility Weight Values")
    ax.set_ylabel("Weight")
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


def plot_weight_sensitivity(env, routes, filename):
    weight_map = {
        "Coverage": ("COVERAGE_WEIGHT", gt.COVERAGE_WEIGHT),
        "Distance": ("DISTANCE_WEIGHT", gt.DISTANCE_WEIGHT),
        "Energy": ("ENERGY_WEIGHT", gt.ENERGY_WEIGHT),
        "Conflict": ("CONFLICT_WEIGHT", gt.CONFLICT_WEIGHT),
        "Target overlap": ("TARGET_OVERLAP_WEIGHT", gt.TARGET_OVERLAP_WEIGHT),
    }

    scale_factors = [0.5, 1.0, 2.0, 4.0]
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), squeeze=False)
    axes = axes.ravel()

    for idx, (label, (attr_name, base_value)) in enumerate(weight_map.items()):
        values = []
        for factor in scale_factors:
            setattr(gt, attr_name, base_value * factor)
            total_utility = 0.0
            for drone in env.drones:
                candidate = routes[drone.name]
                other_routes = [routes[d.name] for d in env.drones if d.name != drone.name]
                total_utility += utility_components(candidate, env, other_routes)["utility"]
            values.append(total_utility)
        setattr(gt, attr_name, base_value)

        ax = axes[idx]
        ax.plot(scale_factors, values, marker="o", linewidth=2)
        ax.set_title(label)
        ax.set_xlabel("Scale factor")
        ax.set_ylabel("Total utility")
        ax.grid(True, alpha=0.25)

    fig.suptitle("Sensitivity of Total Utility to Weight Scaling")
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()
