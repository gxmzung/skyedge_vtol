import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .state_defs import MissionState


class MissionManagerNode(Node):
    def __init__(self) -> None:
        super().__init__('mission_manager_node')

        self.state = MissionState.IDLE

        self.state_pub = self.create_publisher(String, '/mission/state', 10)
        self.command_pub = self.create_publisher(String, '/mission/command', 10)

        self.line_sub = self.create_subscription(String, '/vision/line_result', self.on_line, 10)
        self.marker_sub = self.create_subscription(String, '/vision/aruco_result', self.on_marker, 10)
        self.bridge_sub = self.create_subscription(String, '/px4_bridge/status', self.on_bridge_status, 10)

        self.line_found = False
        self.marker_found = False
        self.bridge_connected = False

        self.timer = self.create_timer(1.0, self.tick)
        self.get_logger().info('Mission manager node started')

    def on_line(self, msg: String) -> None:
        data = json.loads(msg.data)
        self.line_found = bool(data.get('found', False))

    def on_marker(self, msg: String) -> None:
        data = json.loads(msg.data)
        self.marker_found = bool(data.get('found', False))

    def on_bridge_status(self, msg: String) -> None:
        data = json.loads(msg.data)
        self.bridge_connected = bool(data.get('connected', False))

    def publish_state(self) -> None:
        msg = String()
        msg.data = self.state.value
        self.state_pub.publish(msg)

    def publish_command(self, **kwargs) -> None:
        msg = String()
        msg.data = json.dumps(kwargs)
        self.command_pub.publish(msg)

    def tick(self) -> None:
        if self.state == MissionState.IDLE:
            if self.bridge_connected:
                self.state = MissionState.ARMING
                self.publish_command(arm=True, offboard=False)

        elif self.state == MissionState.ARMING:
            self.state = MissionState.TAKEOFF
            self.publish_command(arm=True, offboard=True, action='takeoff')

        elif self.state == MissionState.TAKEOFF:
            self.state = MissionState.SEARCH_LINE

        elif self.state == MissionState.SEARCH_LINE:
            if self.line_found:
                self.state = MissionState.FOLLOW_LINE

        elif self.state == MissionState.FOLLOW_LINE:
            if self.marker_found:
                self.state = MissionState.ALIGN_MARKER

        elif self.state == MissionState.ALIGN_MARKER:
            self.state = MissionState.RESCUE_ACTION

        elif self.state == MissionState.RESCUE_ACTION:
            self.state = MissionState.RETURN_HOME

        elif self.state == MissionState.RETURN_HOME:
            self.state = MissionState.LAND
            self.publish_command(arm=True, offboard=True, action='land')

        elif self.state == MissionState.LAND:
            self.state = MissionState.DONE

        self.publish_state()


def main() -> None:
    rclpy.init()
    node = MissionManagerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
