"""ROS 2 read-only observer telemetry JSONL recorder.

Subscribes only to /sitl_observer/telemetry. No PX4 publishers, no commands.
Records are evidence candidates, not authenticated simulator transcripts.
"""
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class EvidenceRecorder(Node):
    def __init__(self, output):
        super().__init__("sitl_observer_evidence_recorder")
        self.output = output
        self.count = 0
        self.invalid = 0
        self.create_subscription(String, "/sitl_observer/telemetry", self.on_snapshot, 10)

    def on_snapshot(self, msg):
        try:
            snapshot = json.loads(msg.data)
            if (not isinstance(snapshot, dict)
                    or snapshot.get("mode") != "sitl_observation_only"
                    or snapshot.get("read_only") is not True
                    or snapshot.get("actuation_authorized") is not False):
                raise ValueError("not a read-only observer snapshot")
            payload = {
                "recorded_monotonic_s": time.monotonic(),
                "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
                "snapshot": snapshot,
            }
            self.output.write(json.dumps(payload, allow_nan=False) + "\n")
            self.output.flush()
            self.count += 1
        except (ValueError, TypeError):
            self.invalid += 1
            self.get_logger().warning("rejected malformed or unsafe observer snapshot")


def main():
    parser = argparse.ArgumentParser(description="Record simulator observer snapshots (no flight commands)")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=30.0)
    args = parser.parse_args()
    if not math.isfinite(args.duration) or not 10 <= args.duration <= 600:
        parser.error("duration must be between 10 and 600 seconds")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents unintentional overwrites of experiment evidence.
    with args.output.open("x", encoding="utf-8") as output:
        rclpy.init()
        recorder = EvidenceRecorder(output)
        try:
            deadline = time.monotonic() + args.duration
            while rclpy.ok() and time.monotonic() < deadline:
                rclpy.spin_once(recorder, timeout_sec=0.2)
            print(f"observer records={recorder.count}, rejected={recorder.invalid}")
        finally:
            recorder.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
