#!/usr/bin/env python3

"""mission.yaml 내용을 발표 준비용으로 터미널에 미리 출력하는 도구."""

import argparse
from .mission_planner import MissionPlanner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission-file", default="config/mission.yaml")
    args = parser.parse_args()

    mission = MissionPlanner(args.mission_file).load()

    print(f"Mission: {mission.name}")
    print(f"Description: {mission.description}")
    print()
    print("Waypoints:")
    for idx, wp in enumerate(mission.waypoints, start=1):
        print(
            f"{idx}. {wp.name} | "
            f"x={wp.x}, y={wp.y}, z={wp.z}, yaw={wp.yaw}, hold={wp.hold_sec}s"
        )


if __name__ == "__main__":
    main()
