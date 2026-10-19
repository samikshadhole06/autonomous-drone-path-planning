from collections import Counter
from path_planning import Point


# Utility weights.
COVERAGE_WEIGHT = 12.0
DISTANCE_WEIGHT = 8.0
ENERGY_WEIGHT = 0.5
CONFLICT_WEIGHT = 6.0
TARGET_OVERLAP_WEIGHT = 2.0


def path_distance(path):
    return max(0, len(path) - 1)


def energy_cost(path):
    # Simple energy model: every movement consumes one unit,
    # with a small maneuvering factor.
    return path_distance(path) * 1.15


def route_coverage(path, env):
    covered = set()
    for point in path:
        for zone_name, cells in env.surveillance_zones.items():
            if point in cells:
                covered.add(zone_name)
    return covered


def conflict_cost(path, other_paths):
    """
    Penalize shared spatial cells and approximate head-on/time conflicts.
    """
    if not path:
        return 1000

    cost = 0.0
    for other in other_paths:
        overlap = len(set(path) & set(other))
        cost += overlap

        # Time-indexed conflict: same grid cell at approximately same time.
        tmax = min(len(path), len(other))
        for t in range(tmax):
            if path[t] == other[t]:
                cost += 2.0

    return cost


def target_overlap_cost(candidate, other_strategies):
    target = candidate["target"]
    return sum(
        1 for s in other_strategies
        if s["target"] == target
    )


def utility_components(candidate, env, others):
    path = candidate["path"]
    coverage = len(route_coverage(path, env))
    distance = path_distance(path)
    energy = energy_cost(path)

    other_paths = [s["path"] for s in others]
    conflict = conflict_cost(path, other_paths)
    target_overlap = target_overlap_cost(candidate, others)

    coverage_term = COVERAGE_WEIGHT * coverage
    distance_term = DISTANCE_WEIGHT * distance
    energy_term = ENERGY_WEIGHT * energy
    conflict_term = CONFLICT_WEIGHT * conflict
    target_overlap_term = TARGET_OVERLAP_WEIGHT * target_overlap

    total = (
        coverage_term
        - distance_term
        - energy_term
        - conflict_term
        - target_overlap_term
    )

    return {
        "coverage": coverage,
        "distance": distance,
        "energy": energy,
        "conflict": conflict,
        "target_overlap": target_overlap,
        "coverage_term": coverage_term,
        "distance_term": distance_term,
        "energy_term": energy_term,
        "conflict_term": conflict_term,
        "target_overlap_term": target_overlap_term,
        "utility": total,
    }


def utility(candidate, env, others):
    return utility_components(candidate, env, others)["utility"]


def run_baseline(env, strategies):
    """
    Baseline: each drone independently selects its shortest route,
    ignoring the decisions of other drones.
    """
    selected = {}

    for drone in env.drones:
        candidates = strategies[drone.name]
        selected[drone.name] = min(
            candidates,
            key=lambda s: (len(s["path"]), -len(route_coverage(s["path"], env)))
        )

    return selected


def run_best_response(env, strategies, max_iterations=30):
    """
    Iterative best-response game.
    Each drone chooses the highest-utility strategy against the
    current choices of the other drones.
    """
    current = run_baseline(env, strategies)
    log = []

    for iteration in range(max_iterations):
        changed = False

        for drone in env.drones:
            name = drone.name
            others = [
                current[d.name]
                for d in env.drones
                if d.name != name
            ]

            best = max(
                strategies[name],
                key=lambda s: utility(s, env, others)
            )

            old_components = utility_components(current[name], env, others)
            new_components = utility_components(best, env, others)

            if tuple(best["path"]) != tuple(current[name]["path"]):
                current[name] = best
                changed = True

            log.append({
                "iteration": iteration + 1,
                "drone": name,
                "old_utility": round(old_components["utility"], 2),
                "new_utility": round(new_components["utility"], 2),
                "old_coverage": old_components["coverage"],
                "new_coverage": new_components["coverage"],
                "old_distance": old_components["distance"],
                "new_distance": new_components["distance"],
                "old_energy": old_components["energy"],
                "new_energy": new_components["energy"],
                "old_conflict": old_components["conflict"],
                "new_conflict": new_components["conflict"],
                "old_overlap": old_components["target_overlap"],
                "new_overlap": new_components["target_overlap"],
                "changed": changed,
                "target": current[name]["target"],
            })

        if not changed:
            break

    return current, log
