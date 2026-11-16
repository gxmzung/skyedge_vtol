from dataclasses import dataclass
from pathlib import Path
from typing import List

import yaml


@dataclass
class Waypoint:
    name: str
    x: float
    y: float
    z: float
    yaw: float
    hold_sec: float


@dataclass
class Mission:
    name: str
    description: str
    waypoints: List[Waypoint]


class MissionPlanner:
    """mission.yaml을 읽어 waypoint mission으로 변환하는 클래스."""

    def __init__(self, mission_file: str):
        self.mission_file = Path(mission_file).expanduser()

    def load(self) -> Mission:
        if not self.mission_file.exists():
            raise FileNotFoundError(f"mission file not found: {self.mission_file}")

        with self.mission_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        waypoints = []
        for item in data.get("waypoints", []):
            waypoints.append(
                Waypoint(
                    name=str(item["name"]),
                    x=float(item["x"]),
                    y=float(item["y"]),
                    z=float(item["z"]),
                    yaw=float(item.get("yaw", 0.0)),
                    hold_sec=float(item.get("hold_sec", 2.0)),
                )
            )

        if not waypoints:
            raise ValueError("mission file must contain at least one waypoint")

        return Mission(
            name=str(data.get("mission_name", "unnamed_mission")),
            description=str(data.get("description", "")),
            waypoints=waypoints,
        )
