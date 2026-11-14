"""ROS 2 integration smoke: record a publisher's read-only observer snapshot to JSONL.

This injects synthetic topic data. It is NOT PX4 or Gazebo integration.
"""
import io
import json
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from vtol_core.sitl_evidence_recorder import EvidenceRecorder
from vtol_core.sitl_evidence import summarize


def main():
    rclpy.init()
    storage = io.StringIO()
    recorder = EvidenceRecorder(storage)
    test_publisher = Node("synthetic_evidence_test_publisher")
    publisher = test_publisher.create_publisher(String, "/sitl_observer/telemetry", 10)
    executor = SingleThreadedExecutor()
    executor.add_node(recorder)
    executor.add_node(test_publisher)
    try:
        payload = {
            "mode": "sitl_observation_only",
            "read_only": True,
            "actuation_authorized": False,
            "telemetry_fresh": True,
            "channels": {
                "vehicle_status": {"fresh": True},
                "local_position": {"fresh": True},
                "battery_status": {"fresh": False},
            },
        }
        msg = String()
        msg.data = json.dumps(payload)
        deadline = time.monotonic() + 6.0
        while recorder.count < 2 and time.monotonic() < deadline:
            publisher.publish(msg)
            executor.spin_once(timeout_sec=0.2)
        assert recorder.count >= 2, "no ROS 2 observer JSONL data recorded"
        samples = [json.loads(line) for line in storage.getvalue().splitlines()]
        assert len(samples) >= 2
        assert summarize(samples)["verification"] == "ANALYSIS_ONLY_NOT_LIVE_SITL_PROOF"
        unsafe = String()
        unsafe.data = json.dumps({**payload, "actuation_authorized": True})
        count = recorder.count
        publisher.publish(unsafe)
        limit = time.monotonic() + 1.0
        while recorder.invalid < 1 and time.monotonic() < limit:
            executor.spin_once(timeout_sec=0.1)
        assert recorder.count == count and recorder.invalid >= 1
        print("ROS 2 synthetic observer -> recorder -> analyzer smoke passed")
    finally:
        executor.shutdown()
        recorder.destroy_node()
        test_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
