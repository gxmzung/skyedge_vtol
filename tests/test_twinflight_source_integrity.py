"""Validate archived source matches the 22 original Git blob SHAs byte-for-byte.

No ROS2, px4_msgs, PyYAML, network, or flight interface required.
"""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "examples" / "twinflight"
MANIFEST = ARCHIVE / "SOURCE_SHA1_MANIFEST.txt"


def git_blob_sha(data: bytes) -> str:
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


class TwinFlightSourceIntegrityTest(unittest.TestCase):
    def test_original_blobs_preserved(self):
        entries = [line.split("  ", 1) for line in MANIFEST.read_text(encoding="utf8").splitlines()]
        self.assertEqual(len(entries), 22)
        for expected, relative_path in entries:
            with self.subTest(path=relative_path):
                path = ARCHIVE / "original" / relative_path
                self.assertTrue(path.is_file())
                self.assertEqual(git_blob_sha(path.read_bytes()), expected)

    def test_original_ros2_package_is_outside_active_workspace(self):
        self.assertFalse((ROOT / "ros2_ws" / "src" / "twinflight_mission").exists())
        self.assertTrue((ARCHIVE / "original" / "ros2_ws" / "src" /
                         "twinflight_mission" / "twinflight_mission" / "mission_node.py").exists())


if __name__ == "__main__":
    unittest.main()
