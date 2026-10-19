import heapq
import math
from collections import defaultdict
from environment import Point, Environment


def neighbors(p, env):
    x, y = p
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        q = (x + dx, y + dy)
        if (
            0 <= q[0] < env.width
            and 0 <= q[1] < env.height
            and q not in env.obstacles
        ):
            yield q


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal, env, extra_penalty=None):
    extra_penalty = extra_penalty or {}

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for nxt in neighbors(current, env):
            new_cost = (
                cost_so_far[current]
                + 1
                + extra_penalty.get(nxt, 0)
            )
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    if goal not in came_from:
        return []

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    return list(reversed(path))


def candidate_penalties(index):
    # Different corridor preferences produce route diversity.
    if index == 0:
        return {}
    if index == 1:
        return {(x, y): 3 for x in range(9, 17) for y in range(0, 8)}
    if index == 2:
        return {(x, y): 3 for x in range(8, 18) for y in range(17, 25)}
    if index == 3:
        return {(x, y): 3 for x in range(0, 9) for y in range(8, 18)}
    return {(x, y): 3 for x in range(16, 25) for y in range(8, 18)}


def build_candidate_strategies(env, k=5):
    """
    Each drone receives candidate routes to each surveillance zone.
    Strategy = (target zone, path).
    """
    strategies = {}

    for drone in env.drones:
        candidates = []
        seen = set()

        for zone_name, cells in env.surveillance_zones.items():
            # Use the closest cell in the zone for each route variant.
            zone_targets = sorted(
                cells,
                key=lambda p: heuristic(drone.start, p)
            )[:3]

            for target in zone_targets:
                for variant in range(k):
                    path = astar(
                        drone.start,
                        target,
                        env,
                        candidate_penalties(variant)
                    )
                    if len(path) >= 2:
                        key = tuple(path)
                        if key not in seen:
                            seen.add(key)
                            candidates.append({
                                "drone": drone.name,
                                "target": zone_name,
                                "path": path,
                            })

        # Keep a useful but manageable strategy set.
        candidates.sort(key=lambda c: (len(c["path"]), c["target"]))
        strategies[drone.name] = candidates[:25]

    return strategies
