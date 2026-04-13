from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='vtol_core',
            executable='px4_bridge_node',
            name='px4_bridge_node',
            output='screen',
            parameters=['config/global_params.yaml', {'vtol.use_sim': False}],
        ),
        Node(
            package='vtol_core',
            executable='mission_manager_node',
            name='mission_manager_node',
            output='screen',
            parameters=['config/global_params.yaml', {'vtol.use_sim': False}],
        ),
        Node(
            package='vtol_core',
            executable='guidance_node',
            name='guidance_node',
            output='screen',
            parameters=['config/global_params.yaml', {'vtol.use_sim': False}],
        ),
        Node(
            package='vtol_core',
            executable='safety_manager',
            name='safety_manager',
            output='screen',
            parameters=['config/global_params.yaml', {'vtol.use_sim': False}],
        ),
        Node(
            package='vtol_vision',
            executable='line_tracker_node',
            name='line_tracker_node',
            output='screen',
            parameters=['config/global_params.yaml', {'vtol.use_sim': False}],
        ),
        Node(
            package='vtol_vision',
            executable='aruco_detector_node',
            name='aruco_detector_node',
            output='screen',
            parameters=['config/global_params.yaml', {'vtol.use_sim': False}],
        ),
    ])
