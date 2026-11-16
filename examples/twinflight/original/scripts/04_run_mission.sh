#!/usr/bin/env bash
set -e

cd ~/twinflight-mission-v2/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch twinflight_mission mission.launch.py
