import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .state_defs import MissionState


class GuidanceNode(Node):
    def __init__(self) -> None:
        super().__init__('guidance_node')

        self.state = MissionState.IDLE
        self.line_result = {'found': False, 'offset_x': 0.0, 'offset_y': 0.0}
        self.aruco_result = {'found': False, 'offset_x': 0.0, 'offset_y': 0.0, 'target_id': -1}

        self.guidance_pub = self.create_publisher(String, '/guidance/setpoint', 10)

        self.state_sub = self.create_subscription(String, '/mission/state', self.on_state, 10)
        self.line_sub = self.create_subscription(String, '/vision/line_result', self.on_line, 10)
        self.marker_sub = self.create_subscription(String, '/vision/aruco_result', self.on_marker, 10)

        self.timer = self.create_timer(0.5, self.tick)
        self.get_logger().info('Guidance node started')

    def on_state(self, msg: String) -> None:
        self.state = MissionState(msg.data)

    def on_line(self, msg: String) -> None:
        self.line_result = json.loads(msg.data)

    def on_marker(self, msg: String) -> None:
        self.aruco_result = json.loads(msg.data)

    def publish_setpoint(self, x: float, y: float, z: float, yaw: float) -> None:
        payload = {'x': x, 'y': y, 'z': z, 'yaw': yaw}
        msg = String()
        msg.data = json.dumps(payload)
        self.guidance_pub.publish(msg)

    def tick(self) -> None:
        if self.state == MissionState.TAKEOFF:
            self.publish_setpoint(0.0, 0.0, -10.0, 0.0)

        elif self.state == MissionState.SEARCH_LINE:
            self.publish_setpoint(0.0, 0.0, -10.0, 0.2)

        elif self.state == MissionState.FOLLOW_LINE:
            dx = float(self.line_result.get('offset_x', 0.0))
            self.publish_setpoint(dx, 1.0, -10.0, 0.0)

        elif self.state == MissionState.ALIGN_MARKER:
            dx = float(self.aruco_result.get('offset_x', 0.0))
            dy = float(self.aruco_result.get('offset_y', 0.0))
            self.publish_setpoint(dx, dy, -10.0, 0.0)

        elif self.state == MissionState.RETURN_HOME:
            self.publish_setpoint(0.0, 0.0, -10.0, 0.0)

        elif self.state == MissionState.LAND:
            self.publish_setpoint(0.0, 0.0, -2.0, 0.0)


def main() -> None:
    rclpy.init()
    node = GuidanceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
