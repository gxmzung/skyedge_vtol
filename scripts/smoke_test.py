"""
SkyEdge VTOL smoke test.

This script checks that core mission-stack modules can be imported
and that a minimal mission/failsafe scenario runs without crashing.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "vtol"

sys.path.insert(0, str(SRC))

from mission_manager.mission_state import MissionStateMachine, MissionState
from telemetry.telemetry_health import TelemetryHealth
from safety.failsafe_manager import FailsafeManager
from guidance.waypoint_guidance import Waypoint, VehiclePosition, distance_to_waypoint
from px4_bridge.px4_bridge_stub import PX4BridgeStub


def test_mission_state_machine():
    mission = MissionStateMachine()

    assert mission.state == MissionState.IDLE

    mission.next()
    assert mission.state == MissionState.ARMING

    mission.trigger_failsafe()
    assert mission.state == MissionState.FAILSAFE


def test_failsafe_manager():
    failsafe = FailsafeManager()

    safe_health = TelemetryHealth(
        battery_percent=80,
        signal_strength=90,
        gps_satellites=12,
        temperature=42,
        altitude=50,
    )

    unsafe_health = TelemetryHealth(
        battery_percent=15,
        signal_strength=90,
        gps_satellites=12,
        temperature=42,
        altitude=50,
    )

    assert not failsafe.should_trigger(safe_health)
    assert failsafe.should_trigger(unsafe_health)
    assert failsafe.reason(unsafe_health) == "LOW_BATTERY"


def test_guidance_distance():
    position = VehiclePosition(x=0, y=0, z=0)
    waypoint = Waypoint(name="wp1", x=3, y=4, z=0)

    assert round(distance_to_waypoint(position, waypoint), 2) == 5.00


def test_px4_bridge_stub():
    bridge = PX4BridgeStub()

    assert bridge.arm() == "ARM_COMMAND_SENT"
    assert bridge.armed is True

    assert bridge.set_offboard_mode() == "OFFBOARD_MODE_REQUESTED"
    assert bridge.mode == "OFFBOARD"

    command = bridge.send_position_setpoint(1.0, 2.0, 3.0)
    assert command["command"] == "POSITION_SETPOINT"


def main():
    test_mission_state_machine()
    test_failsafe_manager()
    test_guidance_distance()
    test_px4_bridge_stub()

    print("SkyEdge VTOL smoke test passed.")


if __name__ == "__main__":
    main()