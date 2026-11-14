import json
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SafetyManager(Node):
    def __init__(self) -> None:
        super().__init__('safety_manager')

        self.command_pub = self.create_publisher(String, '/mission/command', 10)

        self.last_bridge_time = 0.0
        self.last_state = 'UNKNOWN'

        self.bridge_sub = self.create_subscription(String, '/px4_bridge/status', self.on_bridge, 10)
        self.state_sub = self.create_subscription(String, '/mission/state', self.on_state, 10)

        self.timer = self.create_timer(1.0, self.tick)
        self.get_logger().info('Safety manager started')

    def on_bridge(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except (TypeError, ValueError):
            self.get_logger().warning("ignoring malformed mock bridge heartbeat")
            return
        if (not isinstance(payload, dict)
                or payload.get("simulated") is not True
                or payload.get("connected") is not False):
            self.get_logger().warning("ignoring untrusted bridge status")
            return
        self.last_bridge_time = time.monotonic()

    def on_state(self, msg: String) -> None:
        self.last_state = msg.data

    def tick(self) -> None:
        if self.last_bridge_time == 0.0:
            return

        if time.monotonic() - self.last_bridge_time > 3.0:
            self.get_logger().warning('mock bridge timeout detected; publishing non-arming alert')
            msg = String()
            msg.data = json.dumps({'arm': False, 'offboard': False, 'action': 'safety_alert', 'reason': 'bridge_timeout', 'simulated': True})
            self.command_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = SafetyManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
