#!/usr/bin/env bash
set -e

echo "=== ROS2 node list ==="
ros2 node list || true

echo
echo "=== PX4 fmu topics ==="
ros2 topic list | grep fmu || true

echo
echo "=== Useful commands ==="
echo "rqt_graph"
echo "ros2 topic echo /fmu/in/trajectory_setpoint"
