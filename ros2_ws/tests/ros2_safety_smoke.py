"""ROS 2 runtime safety contract smoke (no PX4; no aircraft).

Forces an expired *simulated* bridge heartbeat. Safety manager must emit
only a non-arming alert, never a flight command, through the ROS 2 topic.
"""
import json
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from vtol_core.safety_manager import SafetyManager


def main():
    rclpy.init()
    safety = SafetyManager()
    observer = Node("safety_contract_observer")
    observed = []
    observer.create_subscription(
        String, "/mission/command", lambda m: observed.append(json.loads(m.data)), 10
    )
    executor = SingleThreadedExecutor()
    executor.add_node(safety)
    executor.add_node(observer)
    try:
        safety.last_bridge_time = time.time() - 10.0
        deadline = time.monotonic() + 5.0
        while not observed and time.monotonic() < deadline:
            executor.spin_once(timeout_sec=0.2)
        assert observed, "no safety alert published on expired heartbeat"
        for payload in observed:
            assert payload.get("action") == "safety_alert", payload
            assert payload.get("simulated") is True, payload
            assert payload.get("arm") is False, payload
            assert payload.get("offboard") is False, payload
        print("ROS 2 stale-bridge safety alert contract passed")
    finally:
        executor.shutdown()
        observer.destroy_node()
        safety.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
