# V5 — PX4 SITL telemetry evidence capture and analysis

For the recorded local Ubuntu 22.04 / WSL2 prerequisite installation and outstanding checks, see [WSL2 PX4 environment validation (2026-11-14)](WSL2_PX4_ENVIRONMENT_2026-11-14.md).

**Status:** Recorder and replay analyzer implemented. This is **not** a live PX4 SITL verification result. No actual flight, hardware control or SITL log is bundled.

## Fixed boundary

- `sitl_telemetry_observer`: read-only PX4 DDS subscribers → `/sitl_observer/telemetry`
- `sitl_evidence_recorder`: subscribes only to `/sitl_observer/telemetry` → JSONL timestamps and snapshots
- `sitl_evidence_report`: offline JSONL validation and descriptive metrics
- No component in this V5 path writes to `/fmu/in/*`, sends arm/offboard commands, or verifies that a claimed PX4 source is authentic

## Required exact versions (record before running)

| Component | Value to record |
| --- | --- |
| PX4-Autopilot commit SHA | Run `git rev-parse HEAD` in the PX4 checkout |
| `px4_msgs` commit SHA | Run `git rev-parse HEAD` in the matching ROS package |
| Micro-XRCE-DDS-Agent version / commit | Record the actual installed binary or checkout |
| ROS 2 distro | Humble |
| Gazebo version / simulation model | Record actual installed version; e.g. `gz_x500` |
| `ROS_DOMAIN_ID` / UDP port | Set consistently across SITL, agent and ROS 2 |
| Operating system | Record exact version and hardware/VM type |

The `px4_msgs` definitions must match the selected PX4 firmware or an explicitly configured PX4 message translation layer. **Do not assume that the newest branches are compatible.**

Reference: https://docs.px4.io/main/en/ros/ros2_comm

## Manual live-SITL experiment

These instructions use separate terminals and require you to install a supported simulator and a compatible `px4_msgs` before building. **No SITL or PX4 is started by GitHub CI.**

1. Start Micro XRCE-DDS Agent on the agreed port (often `8888`): `MicroXRCEAgent udp4 -p 8888`.
2. Start simulation from the pinned PX4 checkout: `make px4_sitl gz_x500` (confirm this target for the chosen release).
3. In an ROS 2 Humble terminal, build/source `ros2_ws` and confirm the expected topics exist **and publish actual samples**:
   ```bash
   source /opt/ros/humble/setup.bash
   cd ros2_ws
   colcon build --symlink-install
   source install/setup.bash
   ros2 topic info /fmu/out/vehicle_status
   ros2 topic hz /fmu/out/vehicle_status
   ```
4. Start the opt-in read-only observer: `ros2 run vtol_core sitl_telemetry_observer`.
5. Start the recorder (separate terminal with the workspace sourced):
   ```bash
   mkdir -p evidence
   ros2 run vtol_core sitl_evidence_recorder --output evidence/sitl_baseline.jsonl --duration 60
   ```
6. For a **separate intentionally induced dropout exercise**, start a new recording and **stop the simulator or the Agent after establishing a stable baseline**. Record the times and restart it to observe recovery; do not manipulate real-aircraft connections.
7. Generate the report:
   ```bash
   ros2 run vtol_core sitl_evidence_report --input evidence/sitl_baseline.jsonl --output evidence/sitl_baseline_report.json
   ```
8. Inspect `verification: ANALYSIS_ONLY_NOT_LIVE_SITL_PROOF`. Associate report with exact source hashes and sanitized simulator/Agent logs for independent review.

The recorder uses exclusive file creation to prevent overwriting existing evidence. Do not commit raw traces with credentials, precise real-world coordinates, network identifiers or private team information.

## Report interpretation

- `channel_fresh_percent`: fraction of **recorder snapshots** in which each channel was fresh; **not** raw sensor packet delivery ratio.
- `combined_fresh_percent`: both VehicleStatus and LocalPosition were fresh in the sampled snapshot.
- `fresh_to_stale_transitions`: observed dropouts after a fresh window.
- `stale_to_fresh_transitions`: observed recoveries **after** an established dropout.
- `mean_record_interval_s`: observer report recording interval, not PX4 topic publication interval.

The analyser validates that snapshots remain read-only and have internally consistent freshness flags. It **cannot authenticate the origin of a JSONL file**. For this reason, it never emits a live-SITL `PASS` or a flight-approval claim.

## Acceptance criteria for *future* live SITL validation

- [ ] Version matrix filled with exact immutable hashes
- [ ] Simulator and Micro XRCE-DDS Agent logs captured
- [ ] Real DDS samples observed on all three subscribed PX4 topics
- [ ] Baseline JSONL captured for at least 60 seconds without editing
- [ ] Dropout/recovery JSONL captured with event timestamps
- [ ] Analyzer report checked against the raw JSONL
- [ ] Independent reviewer has reproduced the run or checked provenance
- [ ] No real hardware connected or controlled

The repo's GitHub Actions test **only the analyzer logic and importability**. Mark the full V5 SITL demonstration verified only after the checklist is satisfied.
