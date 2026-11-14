# Local SITL development environment — installation evidence

**Recorded:** 2026-11-14 (KST)  
**Evidence type:** user-provided terminal output, transcribed into this report; not independently executed by GitHub Actions  
**Machine type:** Windows / WSL2 Linux x86_64 (personal hostname and IP intentionally omitted)  
**Verification level:** dependency and workspace readiness; **NOT PX4↔ROS 2 live DDS/SITL integration**

## Observed results

| Component | Result in terminal transcript | What this demonstrates |
| --- | --- | --- |
| OS | Ubuntu **22.04.5 LTS**, WSL2, x86_64 | Linux environment starts |
| Python | **3.10.12** | Python runtime available |
| ROS 2 | **Humble**, `ros2 pkg list` reports **273** packages | ROS 2 environment can be sourced |
| ROS build tools | `colcon`, `rosdep` paths available | Tools installed |
| PX4-Autopilot | `v1.18.0-beta1-145-gf1bedda6fe` | Existing development checkout |
| PX4 commit | `f1bedda6fecb11c161045b61341a3628ceb4f591` | Reproducible source identity |
| PX4 SITL binary | `~/PX4-Autopilot/build/px4_sitl_default/bin/px4` exists | Binary file present; **not yet runtime-tested** |
| Gazebo | `/usr/bin/gz` found; `gz sim --version` prints `Invalid arguments` | Command present; actual simulator version/runtime **not verified** |
| Agent source | eProsima Micro-XRCE-DDS-Agent **v2.4.2**, checkout `57d086216d01ec43121845d385894a25987f8a2c` | Tagged source checkout |
| Agent build | `colcon build --executor sequential` → **1 package finished** | Build succeeded; minor CMake TinyXML2 developer warning only |
| Agent executable | `~/px4_ros_uxrce_dds_ws/install/microxrcedds_agent/bin/MicroXRCEAgent` | CLI available when sourcing Agent workspace |
| Project clone | `~/vtol-mission-systems/ros2_ws` | Repository cloned locally |
| Project package discovery | `vtol_core` and `vtol_vision` listed by `colcon list` | Packages discovered; **local `colcon build` not yet reported** |
| `px4_msgs` | `ros2 pkg prefix px4_msgs` failed | **Not found in sourced environment** |
| Remote `px4_msgs` branches | `release/1.18` = `b139ce6ef26ad533f11da3e13fab3ff6598636e2`; `release/1.17` = `86d8239e962f6939e05c3737784f60c02fa884db`; `main` = `fd29a68b2329b3d84b61ad5ff0f1d4d313a3a831` | Remote branch tips at observation time; **no matching message ABI check completed** |
| DDS V3 config probe | No matching output from `grep UXRCE_DDS_CLIENT_USE_DDS_V3 ...` | **Inconclusive**, not proof of compatibility |

## What is NOT yet proven

- Micro XRCE-DDS Agent starts, listens on the configured UDP port and connects to PX4.
- PX4 SITL launches successfully with a Gazebo VTOL model.
- `px4_msgs` definitions match the PX4 uXRCE-DDS client message definitions.
- Actual `/fmu/out/vehicle_status`, `/fmu/out/vehicle_local_position`, or `/fmu/out/battery_status` samples are received.
- `vtol_core` and `vtol_vision` build and run **in this specific WSL2 environment** (GitHub ROS 2 Humble CI is separate evidence).
- Any live-SITL telemetry capture, dropout/recovery measurement, or flight testing.

## Next local verification steps

Run from the Ubuntu 22.04 terminal; all work remains inside `~/`, not `/mnt/c/Windows/system32`.

1. **Check Agent help and executable**, without starting the simulator:

   ```bash
   source /opt/ros/humble/setup.bash
   source ~/px4_ros_uxrce_dds_ws/install/local_setup.bash
   command -v MicroXRCEAgent
   MicroXRCEAgent --help | head -30
   ```

2. **Record the PX4 message definition baseline** before selecting a matching `px4_msgs` revision:

   ```bash
   cd ~/PX4-Autopilot
   git rev-parse HEAD
   ls msg/VehicleStatus.msg msg/VehicleLocalPosition.msg msg/BatteryStatus.msg
   ```

3. **Prepare the project locally** and verify the two ROS 2 packages build before installing or running the optional PX4 interface:

   ```bash
   source /opt/ros/humble/setup.bash
   cd ~/vtol-mission-systems/ros2_ws
   rosdep install --from-paths src --ignore-src -r -y
   colcon build --symlink-install --executor sequential
   source install/setup.bash
   ros2 pkg executables vtol_core
   ros2 pkg executables vtol_vision
   ```

4. **Select and pin a `px4_msgs` revision** only after comparing PX4 firmware's uXRCE-DDS message definitions, including their compatibility/versioning approach. The remote `release/1.18` branch is a candidate, **not a proven match** to the specific post-beta firmware commit.

5. Start the Agent, PX4/Gazebo SITL, and read-only observer in separate terminals; capture real topic samples and exact command/version logs. Follow [V5 capture protocol](PX4_SITL_V5_EVIDENCE.md). Use only virtual vehicles.

## Provenance and disclosure

This document records a user-shared successful installation and build transcript. It is **not** equivalent to a CI log, independently collected host telemetry, a reproducible SITL connection, or a completed benchmark. Hostname, IP addresses and unrelated local paths are omitted.
