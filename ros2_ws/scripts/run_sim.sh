#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch vtol_core sim_launch.py
