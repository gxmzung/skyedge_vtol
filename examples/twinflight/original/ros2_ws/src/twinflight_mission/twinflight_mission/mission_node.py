#!/usr/bin/env python3

"""
TwinFlight Mission v2 - ROS2 PX4 Waypoint Mission Node

목표:
- mission.yaml에서 waypoint 목록을 읽는다.
- ROS2 노드가 PX4로 OffboardControlMode, TrajectorySetpoint, VehicleCommand를 전송한다.
- waypoint를 순서대로 전송하며 시설 점검용 자율비행 임무 흐름을 로그로 남긴다.

주의:
- 실제 기체 비행용이 아니라 PX4 SITL/Gazebo 발표용 구조 예시다.
"""

import math
import time
from pathlib import Path

import rclpy
from rclpy.node import Node

from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleCommand

from .mission_planner import MissionPlanner
from .mission_logger import MissionLogger


class TwinFlightMissionNode(Node):
    def __init__(self):
        super().__init__("twinflight_mission_node")

        self.declare_parameter("mission_file", "mission.yaml")
        mission_file = self.get_parameter("mission_file").get_parameter_value().string_value

        self.mission = MissionPlanner(mission_file).load()
        self.mission_logger = MissionLogger()

        self.offboard_control_mode_pub = self.create_publisher(
            OffboardControlMode,
            "/fmu/in/offboard_control_mode",
            10,
        )
        self.trajectory_setpoint_pub = self.create_publisher(
            TrajectorySetpoint,
            "/fmu/in/trajectory_setpoint",
            10,
        )
        self.vehicle_command_pub = self.create_publisher(
            VehicleCommand,
            "/fmu/in/vehicle_command",
            10,
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.counter = 0
        self.current_index = 0
        self.last_waypoint_time = time.time()
        self.armed_and_offboard = False

        self.log(f"Start mission: {self.mission.name}")
        if self.mission.description:
            self.log(f"Description: {self.mission.description}")
        self.log(f"Waypoint count: {len(self.mission.waypoints)}")

    def log(self, message: str):
        line = self.mission_logger.write(message)
        self.get_logger().info(line)

    def timer_callback(self):
        self.publish_offboard_control_mode()

        # PX4 Offboard 모드는 setpoint를 먼저 주기적으로 받아야 안정적으로 진입한다.
        waypoint = self.mission.waypoints[self.current_index]
        self.publish_trajectory_setpoint(waypoint)

        if self.counter == 10 and not self.armed_and_offboard:
            self.log("Switching to Offboard mode")
            self.publish_vehicle_command(
                VehicleCommand.VEHICLE_CMD_DO_SET_MODE,
                param1=1.0,
                param2=6.0,
            )

            self.log("Arming vehicle")
            self.publish_vehicle_command(
                VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
                param1=1.0,
            )
            self.armed_and_offboard = True
            self.last_waypoint_time = time.time()
            self.log_waypoint(waypoint)

        # 실제 위치 feedback을 쓰지 않는 발표용 단순 mission sequencer.
        # hold_sec 시간이 지나면 다음 waypoint setpoint로 넘어간다.
        if self.armed_and_offboard:
            elapsed = time.time() - self.last_waypoint_time
            if elapsed >= waypoint.hold_sec:
                self.current_index += 1
                if self.current_index >= len(self.mission.waypoints):
                    self.log("Mission completed. Holding last position.")
                    self.current_index = len(self.mission.waypoints) - 1
                    self.timer.cancel()
                    return

                next_wp = self.mission.waypoints[self.current_index]
                self.last_waypoint_time = time.time()
                self.log_waypoint(next_wp)

        self.counter += 1

    def log_waypoint(self, waypoint):
        self.log(
            f"Moving to {waypoint.name}: "
            f"x={waypoint.x:.1f}, y={waypoint.y:.1f}, z={waypoint.z:.1f}, yaw={waypoint.yaw:.2f}, "
            f"hold={waypoint.hold_sec:.1f}s"
        )

    def publish_offboard_control_mode(self):
        msg = OffboardControlMode()
        msg.timestamp = self.get_clock().now().nanoseconds // 1000

        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False

        self.offboard_control_mode_pub.publish(msg)

    def publish_trajectory_setpoint(self, waypoint):
        msg = TrajectorySetpoint()
        msg.timestamp = self.get_clock().now().nanoseconds // 1000

        # PX4 NED 좌표계: z가 음수이면 위쪽 방향이다.
        msg.position = [waypoint.x, waypoint.y, waypoint.z]
        msg.yaw = waypoint.yaw

        self.trajectory_setpoint_pub.publish(msg)

    def publish_vehicle_command(self, command, **params):
        msg = VehicleCommand()
        msg.timestamp = self.get_clock().now().nanoseconds // 1000

        msg.command = command
        msg.param1 = params.get("param1", 0.0)
        msg.param2 = params.get("param2", 0.0)
        msg.param3 = params.get("param3", 0.0)
        msg.param4 = params.get("param4", 0.0)
        msg.param5 = params.get("param5", 0.0)
        msg.param6 = params.get("param6", 0.0)
        msg.param7 = params.get("param7", 0.0)

        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True

        self.vehicle_command_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = None

    try:
        node = TwinFlightMissionNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        if node:
            node.get_logger().info("TwinFlight Mission stopped.")
    finally:
        if node:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
