# Verification Matrix

This document is a claim-to-evidence checklist. **Do not infer physical flight capability from passing CI.**

| Claim | Evidence | Current classification | Missing proof |
| --- | --- | --- | --- |
| Mission transitions | `tests/test_core.py`, `scripts/smoke_test.py` | Offline unit/smoke | ROS 2 node integration |
| Failsafe threshold checks | `tests/test_core.py` | Offline unit, including non-finite input | Sensor-source semantics, timing, stale data |
| Waypoint distance | `tests/test_core.py` | Offline arithmetic test | Geodesy and operational coordinate frames |
| PX4 arm/offboard interaction | `PX4BridgeStub` | Stub only | Real PX4 message path and SITL evidence |
| ROS 2 launch wiring | Legacy ROS 2 package files | Source only | Build and runtime test in pinned ROS 2 environment |
| Vision-assisted guidance | Prototype files | Unverified integration | Sensor replay, ROS 2 messaging and failure tests |
| Hardware flight | No evidence | **Not supported** | Independent safety review, authorized flight-test protocol |

## Gating policy

- CI job `offline-core` only certifies Python source import, calculations, unit tests, and smoke checks.
- The legacy PX4 bridge reports mock status; it must never be interpreted as actual vehicle state.
- `real_launch.py` is intentionally disabled. No physical aircraft operation is authorized.
- A future ROS 2/SITL CI job must explicitly use a supported ROS 2/PX4 version pair and archive reproducible logs.
- No HIL/field labels without physical test logs, configuration, safety review and ownership consent.
