# V4 — PX4 SITL Read-Only Telemetry Adapter

## Scope and evidence

This is an **opt-in subscriber**, not a flight controller. It reads a limited subset of PX4 DDS output topics and publishes a sanitized observation JSON. It never creates publishers to `/fmu/in/*`, and **cannot arm, take off, land, set offboard mode, or command a vehicle**.

The core algorithm is exercised by dependency-free Python unit tests and the adapter's package is compiled/imported by the ROS 2 Humble CI. **Until an actual PX4 SITL, a Micro XRCE-DDS Agent, and compatible `px4_msgs` are started and logs are captured, the project does NOT claim that PX4 SITL connectivity has been verified.**

## Architecture

```text
PX4 SITL (not included in current CI)
  |  uXRCE-DDS client → Micro XRCE-DDS Agent → ROS 2 DDS
  +-- /fmu/out/vehicle_status           (px4_msgs/VehicleStatus)
  +-- /fmu/out/vehicle_local_position   (px4_msgs/VehicleLocalPosition)
  +-- /fmu/out/battery_status           (px4_msgs/BatteryStatus)
                                 |
               sitl_telemetry_observer (read-only)
                                 |
              /sitl_observer/telemetry (std_msgs/String JSON)
              {mode,read_only,actuation_authorized,
               telemetry_fresh,channels}
```

The observer uses ROS 2 sensor-data QoS, local monotonic receive time and a configurable 2-second stale threshold. Position is accepted only when `xy_valid` and `z_valid` are true and coordinates are finite. Battery `remaining` must be in [0, 1]. Missing battery data does not count against the separate two-channel freshness indicator and is explicitly marked stale. Battery is **not** used for safety decisions yet.

**`telemetry_fresh=true` only means valid recent messages arrived on the VehicleStatus and VehicleLocalPosition topics.** It is NOT PX4 identity authentication, GNSS validity, flight-control safety, or permission to actuate. The output always contains `actuation_authorized:false`.

## Version compatibility gate

Per PX4 documentation, `px4_msgs` definitions must match those used to build the PX4 uXRCE-DDS client. Select **one pinned PX4 firmware release and matching `px4_msgs` branch/commit**, with the appropriate Micro XRCE-DDS Agent major version for ROS 2 Humble. Avoid unpinned main-branch dependencies. The project does not silently install `px4_msgs`.

Official references:
- https://docs.px4.io/main/en/ros/ros2_comm
- https://docs.px4.io/main/en/middleware/uxrce_dds
- https://docs.px4.io/main/en/middleware/dds_topics

## Manual SITL-only experiment (not yet performed)

1. Install ROS 2 Humble and a mutually compatible PX4 SITL, `px4_msgs` package, and Micro XRCE-DDS Agent. Confirm ROS_DOMAIN_ID matches the simulator.
2. Build `ros2_ws` with `colcon build --symlink-install` and source `install/setup.bash`.
3. Start the Micro XRCE-DDS Agent on UDP port 8888 (matching PX4's client configuration).
4. Start the PX4 Gazebo simulation (`make px4_sitl gz_x500` for a suitable PX4 version).
5. Check `ros2 topic list` and `ros2 topic info /fmu/out/vehicle_status`. Do not infer successful connection from a topic existing without data.
6. Run the **read-only observer** with `ros2 run vtol_core sitl_telemetry_observer`.
7. Inspect `ros2 topic echo /sitl_observer/telemetry`, record topic rates, and stop the simulator to check freshness becomes false within the defined threshold.
8. Capture timestamped command lines, exact version hashes, sanitized logs, and PASS/FAIL results in a reproducible report.

The existing `px4_bridge_node` is still a **mock** and remains separate from this read-only observer.

## V4 verification matrix

| Item | Status |
| --- | --- |
| Finite, range and validity checks | Tested by Python unit tests |
| Stale, missing and clock-regression handling | Tested by Python unit tests |
| Read-only contract, no flight command publishers | Checked in code review and unit tests |
| ROS 2 Humble package installation + observer import | GitHub CI gate |
| Live PX4 SITL DDS subscription | **NOT RUN** |
| Gazebo telemetry replay / dropout measurements | **NOT RUN** |
| PX4 command acknowledgements or offboard control | **OUT OF SCOPE** |
| HIL or physical aircraft | **OUT OF SCOPE** |

## Next gate

Make a manual SITL log artifact and pinned version matrix before adding a separate, explicitly simulator-scoped adapter with proper QoS, message timestamps, finite-range and lost-data checks. Do not present successful smoke tests as real flight integration.
