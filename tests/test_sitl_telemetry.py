"""V4 fail-closed telemetry monitor tests; no ROS or PX4 dependency."""
import math
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ros2_ws" / "src" / "vtol_core"))
from vtol_core.sitl_telemetry import SITLTelemetryMonitor


def status(arming=1, nav=3):
    return SimpleNamespace(arming_state=arming, nav_state=nav)


def position(x=1.0, y=2.0, z=-4.0, xy_valid=True, z_valid=True):
    return SimpleNamespace(x=x, y=y, z=z, xy_valid=xy_valid, z_valid=z_valid)


def battery(remaining=0.7):
    return SimpleNamespace(remaining=remaining)


class ReadOnlyMonitorTests(unittest.TestCase):
    def test_requires_status_and_position(self):
        m = SITLTelemetryMonitor(max_age_s=2.0)
        self.assertFalse(m.snapshot(now=10)["telemetry_fresh"])
        self.assertTrue(m.ingest_vehicle_status(status(), received_at=10))
        self.assertFalse(m.snapshot(now=10)["telemetry_fresh"])
        self.assertTrue(m.ingest_local_position(position(), received_at=10))
        s = m.snapshot(now=11.9)
        self.assertTrue(s["telemetry_fresh"])
        self.assertTrue(s["read_only"])
        self.assertFalse(s["actuation_authorized"])
        self.assertEqual(s["mode"], "sitl_observation_only")
        self.assertFalse(s["channels"]["battery_status"]["fresh"])

    def test_timeout_and_clock_rollback_fail_closed(self):
        m = SITLTelemetryMonitor(max_age_s=2)
        m.ingest_vehicle_status(status(), received_at=100)
        m.ingest_local_position(position(), received_at=100)
        self.assertTrue(m.snapshot(now=102)["telemetry_fresh"])
        self.assertFalse(m.snapshot(now=102.001)["telemetry_fresh"])
        self.assertFalse(m.snapshot(now=99)["telemetry_fresh"])

    def test_invalid_data_never_refreshes(self):
        m = SITLTelemetryMonitor()
        self.assertFalse(m.ingest_vehicle_status(status(arming="ARMED"), received_at=10))
        self.assertFalse(m.ingest_vehicle_status(status(arming=True), received_at=10))
        for value in (math.nan, math.inf, -math.inf):
            self.assertFalse(m.ingest_local_position(position(x=value), received_at=10))
            self.assertFalse(m.ingest_battery_status(battery(value), received_at=10))
        self.assertFalse(m.ingest_local_position(position(xy_valid=False), received_at=10))
        self.assertFalse(m.ingest_local_position(position(z_valid=False), received_at=10))
        self.assertFalse(m.ingest_battery_status(battery(-0.1), received_at=10))
        self.assertFalse(m.ingest_battery_status(battery(1.1), received_at=10))
        self.assertFalse(m.snapshot(now=10)["telemetry_fresh"])

    def test_reject_out_of_order_and_invalid_clocks(self):
        m = SITLTelemetryMonitor()
        self.assertTrue(m.ingest_vehicle_status(status(), received_at=20))
        self.assertFalse(m.ingest_vehicle_status(status(), received_at=19))
        self.assertFalse(m.ingest_local_position(position(), received_at=math.nan))
        self.assertFalse(m.ingest_local_position(position(), received_at=-1))
        self.assertEqual(m.snapshot(now=20)["channels"]["vehicle_status"]["data"]["arming_state"], 1)
        with self.assertRaises(ValueError):
            m.snapshot(now=math.inf)
        with self.assertRaises(ValueError):
            SITLTelemetryMonitor(max_age_s=0)

    def test_battery_optional_but_validated(self):
        m = SITLTelemetryMonitor()
        m.ingest_vehicle_status(status(), received_at=3)
        m.ingest_local_position(position(), received_at=3)
        self.assertTrue(m.ingest_battery_status(battery(0.4), received_at=3))
        s = m.snapshot(now=3.5)
        self.assertTrue(s["telemetry_fresh"])
        self.assertEqual(s["channels"]["battery_status"]["data"]["remaining"], 0.4)


if __name__ == "__main__":
    unittest.main()
