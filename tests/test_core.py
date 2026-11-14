"""Offline regression tests for the dependency-free mission and safety core.

These tests do not verify ROS 2, PX4/SITL, or real-aircraft behavior.
"""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "vtol"))

from guidance.waypoint_guidance import Waypoint, VehiclePosition, distance_to_waypoint, is_waypoint_reached
from mission_manager.mission_state import MissionState, MissionStateMachine
from px4_bridge.px4_bridge_stub import PX4BridgeStub
from safety.failsafe_manager import FailsafeManager
from telemetry.telemetry_health import TelemetryHealth


def healthy(**overrides):
    data = dict(
        battery_percent=80.0,
        signal_strength=90.0,
        gps_satellites=12,
        temperature=42.0,
        altitude=50.0,
    )
    data.update(overrides)
    return TelemetryHealth(**data)


class MissionTests(unittest.TestCase):
    def test_happy_path(self):
        mission = MissionStateMachine()
        self.assertEqual(mission.state, MissionState.IDLE)
        sequence = [
            MissionState.ARMING, MissionState.TAKEOFF, MissionState.MISSION,
            MissionState.RETURN_HOME, MissionState.LANDING, MissionState.COMPLETE,
        ]
        for state in sequence:
            self.assertEqual(mission.next(), state)
        self.assertTrue(mission.is_finished())
        self.assertEqual(mission.next(), MissionState.COMPLETE)

    def test_failsafe_terminal(self):
        mission = MissionStateMachine()
        mission.next()
        mission.trigger_failsafe()
        self.assertEqual(mission.state, MissionState.FAILSAFE)
        self.assertTrue(mission.is_finished())
        self.assertEqual(mission.next(), MissionState.FAILSAFE)


class TelemetryTests(unittest.TestCase):
    def test_nominal_and_boundaries(self):
        self.assertTrue(healthy().is_mission_safe())
        self.assertTrue(healthy(battery_percent=25, signal_strength=40,
                                gps_satellites=8, temperature=75,
                                altitude=120).is_mission_safe())

    def test_bad_conditions_fail_closed(self):
        cases = [
            ("battery_percent", 24, "LOW_BATTERY"),
            ("signal_strength", 39, "LOW_SIGNAL"),
            ("gps_satellites", 7, "GPS_UNSAFE"),
            ("temperature", 76, "HIGH_TEMPERATURE"),
            ("altitude", -1, "ALTITUDE_OUT_OF_RANGE"),
            ("altitude", 121, "ALTITUDE_OUT_OF_RANGE"),
        ]
        failsafe = FailsafeManager()
        for field, value, reason in cases:
            with self.subTest(field=field, value=value):
                state = healthy(**{field: value})
                self.assertFalse(state.is_mission_safe())
                self.assertTrue(failsafe.should_trigger(state))
                self.assertEqual(failsafe.reason(state), reason)

    def test_non_finite_inputs_fail_closed(self):
        for field in ("battery_percent", "signal_strength", "temperature", "altitude"):
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field, value=value):
                    state = healthy(**{field: value})
                    self.assertFalse(state.is_mission_safe())

    def test_out_of_range_inputs_fail_closed(self):
        for field, value in (
            ("battery_percent", 101),
            ("signal_strength", 101),
            ("gps_satellites", -1),
            ("gps_satellites", True),
            ("temperature", -41),
        ):
            with self.subTest(field=field, value=value):
                self.assertFalse(healthy(**{field: value}).is_mission_safe())


class GuidanceTests(unittest.TestCase):
    def test_distance_and_threshold(self):
        pos = VehiclePosition(0, 0, 0)
        wp = Waypoint("p1", 3, 4, 0)
        self.assertEqual(distance_to_waypoint(pos, wp), 5.0)
        self.assertFalse(is_waypoint_reached(pos, wp, threshold=4.9))
        self.assertTrue(is_waypoint_reached(pos, wp, threshold=5.0))


class StubTests(unittest.TestCase):
    def test_stub_is_local_only(self):
        bridge = PX4BridgeStub()
        self.assertEqual(bridge.arm(), "ARM_COMMAND_SENT")
        self.assertTrue(bridge.armed)
        self.assertEqual(bridge.set_offboard_mode(), "OFFBOARD_MODE_REQUESTED")
        self.assertEqual(bridge.send_position_setpoint(1, 2, 3)["command"], "POSITION_SETPOINT")
        # No real PX4 connection or flight command is established here.


if __name__ == "__main__":
    unittest.main()
