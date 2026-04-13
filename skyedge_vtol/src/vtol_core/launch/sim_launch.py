from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('vtol_core'),
        'config',
        'global_params.yaml'
    )

    return LaunchDescription([
        Node(
            package='vtol_core',
            executable='px4_bridge_node',
            name='px4_bridge_node',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='vtol_core',
            executable='mission_manager_node',
            name='mission_manager_node',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='vtol_core',
            executable='guidance_node',
            name='guidance_node',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='vtol_core',
            executable='safety_manager',
            name='safety_manager',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='vtol_vision',
            executable='line_tracker_node',
            name='line_tracker_node',
            output='screen',
            parameters=[config_file],
        ),
        Node(
            package='vtol_vision',
            executable='aruco_detector_node',
            name='aruco_detector_node',
            output='screen',
            parameters=[config_file],
        ),
    ])