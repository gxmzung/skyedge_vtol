"""Read-only historical mission scenario migration regression."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
try:
    import yaml  # noqa: F401
except ImportError:
    yaml = None

if yaml is not None:
    from twinflight_preview import DEFAULT_SCENARIO, preview, read_mission


@unittest.skipUnless(yaml is not None, "Optional PyYAML not installed; dedicated preview CI tests it")
class TwinflightPreviewTests(unittest.TestCase):
    def test_original_scenario_preserved(self):
        mission = read_mission(DEFAULT_SCENARIO)
        self.assertEqual(mission["mission_name"], "campus_facility_inspection_demo")
        self.assertEqual(
            [p["name"] for p in mission["waypoints"]],
            ["takeoff_hover", "inspect_point_1", "inspect_point_2", "return_point"]
        )
        self.assertEqual(mission["waypoints"][2]["x"], 5.0)
        self.assertEqual(mission["waypoints"][2]["y"], 5.0)
        self.assertEqual(mission["waypoints"][2]["z"], -5.0)
        self.assertEqual(mission["waypoints"][2]["yaw"], 1.57)
        self.assertEqual(mission["waypoints"][3]["yaw"], 3.14)
        text = preview(mission)
        self.assertIn("PREVIEW ONLY", text)
        self.assertIn("inspect_point_2", text)

    def test_reject_invalid_missions(self):
        for raw in (
            "waypoints: []",
            "waypoints: [null]",
            "waypoints: [{name: a, x: .nan, y: 0, z: 0}]",
            "waypoints: [{name: a, x: 0, y: 0, z: 0, hold_sec: -1}]",
            "waypoints: [{name: a, x: 0, y: 0, z: 0, hold_sec: wrong}]",
        ):
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as d:
                p = Path(d) / "bad.yaml"
                p.write_text(raw, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_mission(p)


if __name__ == "__main__":
    unittest.main()
