"""ROS 2 runtime smoke: prototype bridge publishes DISCONNECTED status, and
mission stays IDLE without sending arm/takeoff commands.

Uses an isolated ROS_DOMAIN_ID from CI. No PX4/SITL or aircraft is involved.
"""
import json
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

from vtol_core.mission_manager_node import MissionManagerNode
from vtol_core.px4_bridge_node import PX4BridgeNode


def main():
    rclpy.init()
    bridge = PX4BridgeNode()
    mission = MissionManagerNode()
    observer = Node("offline_contract_observer")
    status = []
    states = []
    commands = []
    observer.create_subscription(String, "/px4_bridge/status", lambda m: status.append(json.loads(m.data)), 10)
    observer.create_subscription(String, "/mission/state", lambda m: states.append(m.data), 10)
    observer.create_subscription(String, "/mission/command", lambda m: commands.append(json.loads(m.data)), 10)
    executor = SingleThreadedExecutor()
    for node in (bridge, mission, observer):
        executor.add_node(node)
    try:
        deadline = time.monotonic() + 8.0
        while time.monotonic() < deadline and (len(status) < 2 or len(states) < 2):
            executor.spin_once(timeout_sec=0.2)
        assert len(status) >= 2, "bridge status messages not observed"
        assert len(states) >= 2, "mission state messages not observed"
        assert all(s.get("connected") is False and s.get("simulated") is True for s in status), status
        assert all(s == "IDLE" for s in states), states
        assert not commands, f"unexpected mission commands: {commands}"
        print("ROS 2 offline node-communication contract passed")
    finally:
        executor.shutdown()
        for node in (observer, mission, bridge):
            node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
