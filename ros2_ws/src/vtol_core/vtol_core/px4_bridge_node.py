import json
from typing import Optional

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PX4BridgeNode(Node):
    """
    PX4 실제 메시지 대신 팀 내부 구조를 먼저 검증하기 위한 브리지 골격.
    추후 px4_msgs 기반으로 바꿔 끼울 수 있게 설계한다.
    """

    def __init__(self) -> None:
        super().__init__('px4_bridge_node')

        self.status_pub = self.create_publisher(String, '/px4_bridge/status', 10)
        self.feedback_pub = self.create_publisher(String, '/px4_bridge/mission_feedback', 10)

        self.guidance_sub = self.create_subscription(
            String, '/guidance/setpoint', self.on_guidance, 10
        )
        self.command_sub = self.create_subscription(
            String, '/mission/command', self.on_command, 10
        )

        self.timer = self.create_timer(0.5, self.publish_status)
        self.latest_setpoint: Optional[dict] = None
        self.latest_command: Optional[dict] = None

        self.get_logger().info('PX4 bridge node started')

    def on_guidance(self, msg: String) -> None:
        try:
            self.latest_setpoint = json.loads(msg.data)
            self.get_logger().info(f"guidance received: {self.latest_setpoint}")
        except json.JSONDecodeError:
            self.get_logger().warning('invalid guidance json')

    def on_command(self, msg: String) -> None:
        try:
            self.latest_command = json.loads(msg.data)
            self.get_logger().info(f"mission command received: {self.latest_command}")
        except json.JSONDecodeError:
            self.get_logger().warning('invalid mission command json')

    def publish_status(self) -> None:
        payload = {
            'connected': True,
            'armed': False if self.latest_command is None else self.latest_command.get('arm', False),
            'offboard': False if self.latest_command is None else self.latest_command.get('offboard', False),
            'latest_setpoint': self.latest_setpoint,
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.status_pub.publish(msg)

    def send_feedback(self, text: str) -> None:
        msg = String()
        msg.data = text
        self.feedback_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = PX4BridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
