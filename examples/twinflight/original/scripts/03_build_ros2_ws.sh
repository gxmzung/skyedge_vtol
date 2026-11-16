#!/usr/bin/env bash
set -e

cd ~/twinflight-mission-v2/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
