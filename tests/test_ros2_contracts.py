"""Pure-Python ROS 2 prototype-contract regression (no ROS installation)."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ros2_ws" / "src" / "vtol_core"))
from vtol_core.contracts import parse_detection, parse_status


class ContractTests(unittest.TestCase):
    def test_forged_bridge_never_counts_as_px4_connected(self):
        self.assertFalse(parse_status('{"connected": true, "armed": true}')["connected"])
        self.assertFalse(parse_status("{}")["connected"])
        self.assertFalse(parse_status("{broken")["connected"])
        self.assertTrue(parse_status('{"connected": true}')["simulated"])

    def test_detection_requires_boolean_and_valid_payload(self):
        self.assertTrue(parse_detection('{"found": true, "timestamp": 10.0}'))
        for bad in ('', 'null', '[]', '{"found": 1}', '{"found": "true"}',
                    '{"found": true, "timestamp": "today"}',
                    '{"found": true, "timestamp": NaN}', '{invalid}'):
            with self.subTest(bad=bad):
                self.assertFalse(parse_detection(bad))


if __name__ == "__main__":
    unittest.main()
