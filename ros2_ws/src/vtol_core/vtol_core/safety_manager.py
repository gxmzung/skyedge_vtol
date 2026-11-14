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
        _ = json.loads(msg.data)
        self.last_bridge_time = time.time()

    def on_state(self, msg: String) -> None:
        self.last_state = msg.data

    def tick(self) -> None:
        if self.last_bridge_time == 0.0:
            return

        if time.time() - self.last_bridge_time > 3.0:
            self.get_logger().warning('bridge timeout detected, sending failsafe command')
            msg = String()
            msg.data = json.dumps({'arm': True, 'offboard': False, 'action': 'failsafe_land'})
            self.command_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = SafetyManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
