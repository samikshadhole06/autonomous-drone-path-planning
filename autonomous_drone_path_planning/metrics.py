from pathlib import Path
import pandas as pd
from game_theory import (
    path_distance,
    energy_cost,
    route_coverage,
    conflict_cost,
)


def summarize_solution(env, routes):
    total_distance = 0
    total_energy = 0
    total_conflict = 0
    covered_zones = set()

    route_list = list(routes.values())

    for route in route_list:
        path = route["path"]
        total_distance += path_distance(path)
        total_energy += energy_cost(path)
        covered_zones |= route_coverage(path, env)

    for i in range(len(route_list)):
        total_conflict += conflict_cost(
            route_list[i]["path"],
            [r["path"] for j, r in enumerate(route_list) if j != i]
        )

    # Pairwise conflict cost counts each pair from both perspectives.
    total_conflict = total_conflict / 2

    coverage_percent = (
        len(covered_zones) / len(env.surveillance_zones) * 100
    )

    return {
        "distance": round(total_distance, 2),
        "energy": round(total_energy, 2),
        "conflicts": round(total_conflict, 2),
        "coverage": round(coverage_percent, 2),
        "zones_covered": len(covered_zones),
        "total_zones": len(env.surveillance_zones),
    }


def save_metrics(filename, baseline, game_theory):
    rows = []
    for method, data in [
        ("Independent Baseline", baseline),
        ("Game-Theoretic", game_theory),
    ]:
        row = {"method": method}
        row.update(data)
        rows.append(row)

    pd.DataFrame(rows).to_csv(filename, index=False)
