#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y || true
colcon build
echo "[INFO] build complete"
