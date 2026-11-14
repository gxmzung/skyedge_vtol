"""Offline V5 evidence replay and input-validation tests."""
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ros2_ws" / "src" / "vtol_core"))
from vtol_core.sitl_evidence import read_jsonl, summarize


def observation(t, status=True, position=True, battery=True):
    channels = {
        "vehicle_status": {"fresh": status, "age_s": 0.1 if status else None, "data": {"arming_state": 1} if status else None},
        "local_position": {"fresh": position, "age_s": 0.1 if position else None, "data": {"x": 1} if position else None},
        "battery_status": {"fresh": battery, "age_s": 0.1 if battery else None, "data": {"remaining": 0.7} if battery else None},
    }
    return {
        "recorded_monotonic_s": t,
        "snapshot": {
            "mode": "sitl_observation_only",
            "read_only": True,
            "actuation_authorized": False,
            "telemetry_fresh": status and position,
            "channels": channels,
        },
    }


class EvidenceTests(unittest.TestCase):
    def test_fresh_drop_recover(self):
        rows = [
            observation(1.0),
            observation(1.5),
            observation(2.0, position=False),
            observation(2.5, status=False, position=False),
            observation(3.0),
        ]
        result = summarize(rows)
        self.assertEqual(result["observations"], 5)
        self.assertEqual(result["duration_s"], 2)
        self.assertEqual(result["combined_fresh_percent"], 60)
        self.assertEqual(result["fresh_to_stale_transitions"], 1)
        self.assertEqual(result["stale_to_fresh_transitions"], 1)
        self.assertEqual(result["verification"], "ANALYSIS_ONLY_NOT_LIVE_SITL_PROOF")
        self.assertEqual(result["channel_fresh_percent"]["battery_status"], 100)

    def test_initial_stale_is_not_recovery(self):
        result = summarize([observation(1, status=False), observation(2)])
        self.assertEqual(result["stale_to_fresh_transitions"], 0)

    def test_missing_data_and_bad_order(self):
        with self.assertRaises(ValueError):
            summarize([])
        with self.assertRaises(ValueError):
            summarize([observation(4), observation(4)])
        with self.assertRaises(ValueError):
            summarize([observation(4), observation(3)])
        with self.assertRaises(ValueError):
            summarize([observation(float("nan"))])

    def test_reject_untrusted_or_inconsistent_contract(self):
        for mutate in (
            lambda r: r["snapshot"].update(actuation_authorized=True),
            lambda r: r["snapshot"].update(read_only=False),
            lambda r: r["snapshot"].update(mode="live_flight"),
            lambda r: r["snapshot"].update(telemetry_fresh=False),
            lambda r: r["snapshot"]["channels"]["vehicle_status"].update(fresh="true"),
        ):
            row = observation(1)
            mutate(row)
            with self.subTest(mutate=mutate):
                with self.assertRaises(ValueError):
                    summarize([row])

    def test_jsonl_roundtrip_and_invalid_line(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "recording.jsonl"
            with p.open("w", encoding="utf-8") as output:
                for row in [observation(10), observation(10.5)]:
                    output.write(json.dumps(row) + "\n")
            self.assertEqual(summarize(read_jsonl(p))["observations"], 2)
            p.write_text('{"bad":\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 1"):
                read_jsonl(p)


if __name__ == "__main__":
    unittest.main()
