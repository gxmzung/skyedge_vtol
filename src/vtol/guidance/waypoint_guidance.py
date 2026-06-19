from dataclasses import dataclass
from math import sqrt


@dataclass
class Waypoint:
    name: str
    x: float
    y: float
    z: float


@dataclass
class VehiclePosition:
    x: float
    y: float
    z: float


def distance_to_waypoint(position: VehiclePosition, waypoint: Waypoint) -> float:
    dx = waypoint.x - position.x
    dy = waypoint.y - position.y
    dz = waypoint.z - position.z

    return sqrt(dx * dx + dy * dy + dz * dz)


def is_waypoint_reached(
    position: VehiclePosition,
    waypoint: Waypoint,
    threshold: float = 2.0,
) -> bool:
    return distance_to_waypoint(position, waypoint) <= threshold


def select_next_waypoint(
    position: VehiclePosition,
    waypoints: list[Waypoint],
) -> Waypoint | None:
    for waypoint in waypoints:
        if not is_waypoint_reached(position, waypoint):
            return waypoint

    return None