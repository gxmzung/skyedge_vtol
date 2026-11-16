"""Read-only TwinFlight mission.yaml preview.

Educational migration aid; neither PX4 nor ROS2 is imported or controlled.
Requires PyYAML, installed only for the optional preview/CI job.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO = ROOT / "examples" / "twinflight" / "mission.yaml"


def read_mission(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("waypoints"), list):
        raise ValueError("mission must be a YAML mapping with a waypoints list")
    if not data["waypoints"]:
        raise ValueError("mission needs at least one waypoint")
    waypoints = []
    for i, raw in enumerate(data["waypoints"]):
        if not isinstance(raw, dict):
            raise ValueError(f"waypoint {i} must be an object")
        name = raw.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"waypoint {i} needs a name")
        values = {}
        for field in ("x", "y", "z", "yaw", "hold_sec"):
            try:
                value = float(raw.get(field, 0.0 if field == "yaw" else
                                      2.0 if field == "hold_sec" else None))
            except (ValueError, TypeError) as exc:
                raise ValueError(f"waypoint {i} has invalid {field}") from exc
            if not math.isfinite(value):
                raise ValueError(f"waypoint {i} contains nonfinite {field}")
            values[field] = value
        if values["hold_sec"] < 0:
            raise ValueError(f"waypoint {i} negative hold time")
        waypoints.append({"name": name, **values})
    title = str(data.get("mission_name", "unnamed_mission"))
    description = str(data.get("description", ""))
    return {"mission_name": title, "description": description, "waypoints": waypoints}


def preview(mission: dict) -> str:
    lines = [f"Mission: {mission['mission_name']}",
             f"Description: {mission['description']}", "", "Waypoints:"]
    for i, wp in enumerate(mission["waypoints"], 1):
        lines.append(
            f"{i}. {wp['name']} | x={wp['x']}, y={wp['y']}, z={wp['z']}, "
            f"yaw={wp['yaw']}, hold={wp['hold_sec']}s"
        )
    lines.append("")
    lines.append("PREVIEW ONLY: no ROS2, PX4, MAVSDK, SITL, or aircraft control.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mission-file", type=Path, default=DEFAULT_SCENARIO)
    args = parser.parse_args()
    print(preview(read_mission(args.mission_file)))


if __name__ == "__main__":
    main()
