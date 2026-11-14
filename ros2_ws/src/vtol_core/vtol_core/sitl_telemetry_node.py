"""Opt-in read-only ROS 2 PX4 telemetry observer for **SITL use only**.

Requires a separately installed px4_msgs package matching the PX4 firmware.
Publishes sanitized status to /sitl_observer/telemetry; never publishes to /fmu/in.
"""
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import String

from .sitl_telemetry import SITLTelemetryMonitor


class SITLTelemetryObserverNode(Node):
    def __init__(self, vehicle_status_type, local_position_type, battery_status_type):
        super().__init__("sitl_telemetry_observer")
        self.declare_parameter("max_age_sec", 2.0)
        max_age = float(self.get_parameter("max_age_sec").value)
        self.monitor = SITLTelemetryMonitor(max_age_s=max_age)
        self.publisher = self.create_publisher(String, "/sitl_observer/telemetry", 10)
        self.create_subscription(vehicle_status_type, "/fmu/out/vehicle_status",
                                 self.monitor.ingest_vehicle_status, qos_profile_sensor_data)
        self.create_subscription(local_position_type, "/fmu/out/vehicle_local_position",
                                 self.monitor.ingest_local_position, qos_profile_sensor_data)
        self.create_subscription(battery_status_type, "/fmu/out/battery_status",
                                 self.monitor.ingest_battery_status, qos_profile_sensor_data)
        self.create_timer(0.5, self.publish_snapshot)

    def publish_snapshot(self):
        msg = String()
        msg.data = json.dumps(self.monitor.snapshot(), allow_nan=False)
        self.publisher.publish(msg)


def main():
    try:
        from px4_msgs.msg import BatteryStatus, VehicleLocalPosition, VehicleStatus
    except ImportError as exc:
        raise SystemExit(
            "V4 observer requires a compatible px4_msgs build. "
            "This read-only node does not start PX4 SITL or an XRCE-DDS agent."
        ) from exc
    rclpy.init()
    node = SITLTelemetryObserverNode(VehicleStatus, VehicleLocalPosition, BatteryStatus)
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
