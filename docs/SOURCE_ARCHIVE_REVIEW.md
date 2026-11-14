# Uploaded Source Archive Review (2026-11-14)

This file records a **source audit**, not a blanket import or a claim of individual authorship. The user supplied three ZIP snapshots; their contents are **not automatically relicensed** by being uploaded for review. Historical repository authorship remains in Git history.

## Summary

| Source snapshot | Files | Source-only assessment | Decision |
| --- | ---: | --- | --- |
| `test_vtol_yejun-main` | 15,161 total | Approximately 15 non-generated source/configuration files; rest largely `build/`, `install/`, `log/` | **Candidate for selective ROS 2/C++ integration after build tests and authorship check** |
| `SkyEdge-main` | 68 | ROS 2 Python package skeleton, custom `SystemStatus.msg`, manager, launch, container scaffolding; some core files empty | **Reference architecture only**, not drop-in integration |
| `skyedge-vtol-ws-main` | 64 | ROS 2/PX4 workspace, waypoint node, pure Python trajectory planners (including MPC), simulation config, contract/unit tests | **Candidate components**, subject to team attribution/reuse permission |

## Candidate implementation inventory

### C++ control and vision

Source: `test_vtol_yejun-main`

- `src/vtol_control/src/hovering_control_node.cpp` — `rclcpp` / `px4_msgs` / pose and telemetry subscriptions, offboard-setpoint publishing.
- `src/vtol_vision_cpp/src/aruco_detector_node.cpp` — OpenCV ArUco detection and geometry output.
- `src/vtol_vision/vtol_vision/aruco_detector_node.py` — Python detector experiment.
- `CMakeLists.txt`, `package.xml`, `setup.py` are needed to reproduce package builds.

**Do not commit** generated `build/`, `install/`, `log/`, cached dependencies, machine-specific environments, or unpublished device configuration. C++ code may use PX4 message fields tied to a specific version; compilation and SITL operation are not yet verified.

### Python ROS 2 package architecture

Source: `SkyEdge-main`

- `vtol_manager/manager_node.py` publishes a custom `SystemStatus` message.
- `vtol_msgs/msg/SystemStatus.msg` defines the custom contract.
- `vtol_control/control_node.py`, `vtol_sim/sim_bridge_node.py`, and health-monitor modules were empty in the reviewed snapshot.
- Separate simulation and real launch folders are **not** proof of safe real-vehicle readiness.

### Waypoint navigation and trajectory planning

Source: `skyedge-vtol-ws-main`

- `src/vtol/src/waypoint_nav_node.py` uses `px4_msgs` with ROS 2 topic and QoS assumptions.
- `trajectory_planners/simple.py` implements geometric setpoint interpolation.
- `trajectory_planners/mpc_planner.py` implements a finite-horizon numerical planner without external numerical dependencies.
- Contract/unit test suites exist; integration tests are conditional on a separately running simulated stack.

**Important:** A class named MPC does not establish stable flight control, optimality under actuator constraints, or aircraft safety.

## Decision: not a bulk source dump

**Retain** current `src/vtol` as the independently testable Python safety core. **Retain** `ros2_ws/src` as the current ROS 2 scaffold. Defer integration of external snapshot code until:

1. Source ownership, reuse rights, and individual/team contribution provenance are recorded.
2. Build/reproducibility checks establish a compatible ROS 2 / PX4 / OpenCV version matrix.
3. Incoming modules have test coverage and do not create conflicting package names or duplicate ROS 2 node entrypoints.
4. Real-aircraft commands remain outside default runnable and CI paths.
5. A new PR documents each imported file and its original provenance.

## Recommended next modules

1. **C++ ArUco detector** as a clearly isolated ROS 2 vision package, compile-verified before promoting.
2. **Waypoint trajectory planners** extracted behind a pure-Python test interface after reuse permission confirmation.
3. **MPC numerical verification** against a reference implementation, constraints, finite values, and reproducible trajectories.
4. **ROS 2 contract tests** for timestamp staleness, connection loss, QoS and command/ack separation.
5. **PX4 SITL-only adapter** with an independent simulation gate (no hardware commands).

## Attribution and naming

The current portfolio can use **VTOL Mission Systems** while preserving accurate attribution of historical team work. We will not rewrite Git history or falsify third-party authorship to eliminate a former name. Historical references may exist in archived documents and commit metadata, even after current UI paths and active documentation have been rebranded.
