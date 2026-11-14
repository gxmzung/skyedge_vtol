# ROS 2 Humble Integration & Topic Contracts (V2)

## Verification status

The dedicated `.github/workflows/ros2-humble-build.yml` uses a `ros:humble-ros-base` container and runs dependency resolution, `colcon build`, ROS package executable discovery and a basic package import. It does **not** launch PX4 or a real vehicle. Always check the run result before claiming build success.

## Topic map (prototype only)

| Topic | Producer | Consumer | Type | Trust |
| --- | --- | --- | --- | --- |
| `/px4_bridge/status` | `px4_bridge_node` | `mission_manager_node`, `safety_manager` | `std_msgs/String` JSON | Simulated and **not connected to PX4** |
| `/mission/state` | `mission_manager_node` | `safety_manager` | String enum | Internal state |
| `/mission/command` | mission/safety manager | prototype bridge | String JSON | Test commands only |
| `/guidance/setpoint` | guidance node | prototype bridge | String JSON | Untrusted simulation setpoint |
| `/vision/line_result` | line tracker | mission manager | String JSON | No calibration or end-to-end proof |
| `/vision/aruco_result` | ArUco detector | mission manager | String JSON | No calibration or end-to-end proof |

## V2 safety changes

- The bridge can only publish `connected:false`, `simulated:true`, `armed:false`, `offboard:false` until a **separate** validated SITL adapter exists.
- The mission manager uses fail-closed parsers. JSON strings like `{"found":1}` or malformed messages do not become valid detections.
- Any untrusted bridge JSON claiming `connected:true` is ignored by the offline contract validator.
- ROS 2 launch wiring, sensor ingestion, and PX4 command transport are not verified by Python-only CI.

## Build locally (Ubuntu 22.04 with ROS 2 Humble)

```bash
source /opt/ros/humble/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 pkg executables vtol_core
ros2 pkg executables vtol_vision
```

For validation without ROS 2, run `python -m unittest discover -s tests -v` at the repository root.

## Known limitations / next gate

1. Both ROS 2 packages still have duplicate top-level Python module copies versus installable package modules. They are intentionally not deleted until build/import parity and provenance review.
2. ROS 2 Humble system OpenCV may not support `cv2.aruco.ArucoDetector`. A runtime camera replay/integration test is required.
3. A `colcon build` only proves packaging, not ROS communication, functioning vision, PX4 SITL, or flight safety.
4. SITL adapter must explicitly verify timestamps, QoS, frame conventions, heartbeat freshness and offboard ack; no automatic hardware control path is included.
