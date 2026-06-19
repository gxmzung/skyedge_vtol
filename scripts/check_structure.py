"""
SkyEdge repository structure check.

This script checks whether important folders and files exist.
It is intended for CI and repository maintenance.
"""

from pathlib import Path


REQUIRED_PATHS = [
    "README.md",
    "docs/architecture.md",
    "docs/mission_flow.md",
    "docs/consolidation_plan.md",
    "src/vtol/mission_manager/mission_state.py",
    "src/vtol/telemetry/telemetry_health.py",
    "src/vtol/safety/failsafe_manager.py",
    "src/vtol/guidance/waypoint_guidance.py",
    "src/vtol/px4_bridge/px4_bridge_stub.py",
    "src/vtol/config/sample_mission.yaml",
    "src/vtol_vision/vision_demo.py",
    "src/hardware_prototypes/udp_tools/vision_udp_sender.py",
]


def main():
    root = Path(__file__).resolve().parents[1]
    missing = []

    for relative_path in REQUIRED_PATHS:
        path = root / relative_path

        if not path.exists():
            missing.append(relative_path)

    if missing:
        print("Missing required paths:")

        for item in missing:
            print(f"- {item}")

        raise SystemExit(1)

    print("SkyEdge structure check passed.")


if __name__ == "__main__":
    main()