from dataclasses import dataclass
from typing import List, Tuple, Set, Dict


Point = Tuple[int, int]


@dataclass
class Drone:
    name: str
    start: Point


@dataclass
class Environment:
    width: int
    height: int
    obstacles: Set[Point]
    surveillance_zones: Dict[str, Set[Point]]
    drones: List[Drone]


def rectangle(x1, y1, x2, y2):
    return {(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)}


def create_environment():
    width, height = 25, 25

    obstacles = set()
    obstacles |= rectangle(7, 5, 10, 12)
    obstacles |= rectangle(14, 3, 17, 8)
    obstacles |= rectangle(13, 14, 18, 18)
    obstacles |= rectangle(4, 17, 9, 20)

    # Five surveillance zones. Each is a small 3x3 region.
    zones = {
        "S1": rectangle(2, 2, 4, 4),
        "S2": rectangle(20, 2, 22, 4),
        "S3": rectangle(19, 11, 21, 13),
        "S4": rectangle(3, 11, 5, 13),
        "S5": rectangle(10, 21, 12, 23),
    }

    drones = [
        Drone("D1", (1, 22)),
        Drone("D2", (23, 22)),
        Drone("D3", (12, 1)),
    ]

    # Make sure starts are not obstacles.
    for d in drones:
        obstacles.discard(d.start)

    return Environment(width, height, obstacles, zones, drones)
