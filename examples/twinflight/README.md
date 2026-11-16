# TwinFlight Mission v2 — historical package preservation

Original repository: https://github.com/gxmzung/twinflight-mission-v2

This directory preserves **the exact 22 Git-tracked files** from the original repository main branch at the time of migration (see `SOURCE_SHA1_MANIFEST.txt`). This is a **source preservation and repository consolidation** action, not a verified ROS2/PX4 functional migration.

## Layout
- `original/`: the historical README, 4 ROS2 package modules, launch file, config, package metadata, demonstration shell scripts, class presentation documents, team roles and all other tracked files.
- `SOURCE_SHA1_MANIFEST.txt`: Git blob SHA-1 provenance for original files.
- `../twinflight/mission.yaml`: a separate scenario-only demonstration fixture.
- `../../scripts/twinflight_preview.py`: an offline *read-only* preview, without PX4 commands.

## Reproducing historical ROS2 package (sandbox only)

The original ROS2 package is **not** built by the main repo's ROS2 CI. It depends on `px4_msgs` built for a compatible PX4 version and `rclpy`. The original package source remains at `original/ros2_ws/src/twinflight_mission`; when using a separately prepared ROS2/PX4 SITL workspace, copy that package into its `src/` and supply the exact matching dependencies before invoking colcon. Do **not** invoke `mission_node` on a real aircraft. The original code can issue arm and offboard setpoints and advances waypoints by time instead of confirmed position feedback.

No claims are made of successful live SITL build, true hardware interface, or flight safety. Existing team contributions and historical project/assignment materials are retained without changing authorship.

## CI verification
`python -m unittest discover -s tests -p 'test_twinflight_source_integrity.py' -v` verifies SHA identity for every original tracked file. This test proves byte-level preservation **only**; ROS2 runtime compatibility and assignment/public URL references must still be checked before archive.
