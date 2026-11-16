from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path


def generate_launch_description():
    default_mission_file = str(
        Path(get_package_share_directory("twinflight_mission")) / "config" / "mission.yaml"
    )

    mission_file_arg = DeclareLaunchArgument(
        "mission_file",
        default_value=default_mission_file,
        description="Path to mission.yaml",
    )

    mission_node = Node(
        package="twinflight_mission",
        executable="mission_node",
        name="twinflight_mission_node",
        output="screen",
        parameters=[{"mission_file": LaunchConfiguration("mission_file")}],
    )

    return LaunchDescription([
        mission_file_arg,
        mission_node,
    ])
