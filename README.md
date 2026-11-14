# VTOL Mission Systems

**ROS 2 / PX4 Mission Software · Telemetry Safety · System Integration · Verification**

[![Python verification](https://github.com/gxmzung/vtol-mission-systems/actions/workflows/offline-core.yml/badge.svg)](https://github.com/gxmzung/vtol-mission-systems/actions/workflows/offline-core.yml)

> **Status: research prototype.** This repository provides Python mission logic and ROS 2 node scaffolds. The included PX4 bridge is a **stub**, not an authenticated/flight-tested PX4 connection. No physical aircraft should be controlled using these components.

## Goal

Build a reproducible, simulation-first portfolio around mission-state transitions, telemetry-based safety decisions, guidance calculations, and ROS 2 interface design. Every claimed capability has an explicit verification level.

| Capability | Existing implementation | Verified here |
| --- | --- | --- |
| Mission state machine | Python state transitions and FAILSAFE terminal state | Unit and smoke tests |
| Telemetry safety | Battery, signal, GNSS, temperature, altitude thresholds | Unit tests, boundary and invalid numeric inputs |
| Guidance | 3D waypoint distance and threshold checks | Unit tests |
| PX4 interface | Local in-memory bridge stub and ROS 2 message scaffold | Stub behavior only; **not** real PX4 |
| Vision | ArUco / line-tracking prototypes | Code present; integration not established |
| ROS 2 | Packaged Humble nodes, ROS topic mock bridge and safety guard | `colcon build` + basic DDS runtime topic smoke CI; not PX4 SITL |
| Real aircraft | Not implemented or validated | **Unsupported / blocked** |

## Quick start — dependency-free core tests

Python 3.11+:

```bash
python -m unittest discover -s tests -v
python scripts/check_structure.py
python scripts/smoke_test.py
python src/vtol/mission_demo.py
```

The scripts above exercise pure-Python logic and stubs. They do **not** connect to PX4, ROS 2, SITL, a vehicle, or hardware.

## Repository layout

```text
src/vtol/                 # Dependency-free research core
src/vtol_vision/          # Vision experiment prototypes
src/hardware_prototypes/  # Optional interface examples
ros2_ws/src/             # ROS 2 Humble installable packages; mock DDS checks
scripts/                 # Structure and smoke checks
tests/                   # Offline unittest safety regression suite
docs/                    # Verification and migration decisions
```

The former project-branded workspace directory is now `ros2_ws/`. This is a **directory-only migration**, not evidence of ROS 2 build or SITL integration. Existing historical documentation is retained for provenance.

## Safety boundaries

1. **Simulated != PX4-connected != flight-tested.**
2. The existing ROS 2 bridge publishes mock status and is not an independent source of vehicle arming truth.
3. Invalid or non-finite telemetry readings are treated as unsafe in the dependency-free safety model.
4. Real-aircraft launch is disabled until there is a separately reviewed vehicle adapter, an independent operator-controlled safety path, and documented tests.
5. Do not use this research code to fly or control a physical aircraft.

See [Verification Matrix](docs/VERIFICATION_MATRIX.md), [ROS 2 Topic Contracts](docs/ROS2_CONTRACTS_V2.md), [V4 Read-Only SITL Plan](docs/PX4_SITL_V4.md), and [Migration Plan](docs/REFACTOR_PLAN.md).

## Development roadmap

- **V1 (this PR):** honest README, regression tests, fail-closed telemetry checks, disable legacy real launch.
- **V2 (verified):** ROS 2 Humble `colcon build` and mock DDS topic communication checks.
- **V3 (PR pending):** remove shadow duplicate node files and test stale heartbeat alert over ROS 2 topics.
- **V3:** ROS 2/PX4 SITL adapter with explicit message contracts, simulation logs, and CI evidence.
- **V4 (in PR):** optional read-only PX4 SITL telemetry observer with fail-closed freshness checks. Live SITL subscription remains unverified; no flight command path.
- **Later:** independent HIL and operator safety review *only if authorized*.

## Project history and attribution

This repository evolved from an earlier VTOL competition/team project. Renaming the current portfolio **does not erase prior authorship, team involvement, or commit history**. Historical team documents and directories are retained until their provenance and reuse rights have been reviewed. This repository does not claim that all historical work was created solely by the current maintainer.

## Maintainer

[Youngjun Lee](https://github.com/gxmzung) · [LinkedIn](https://www.linkedin.com/in/youngjoon-gamjeong/)
