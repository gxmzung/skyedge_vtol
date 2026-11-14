# VTOL Mission Systems

**ROS 2 / PX4 Mission Software · Telemetry Safety · System Integration · Verification**

[![Python verification](https://github.com/gxmzung/vtol-mission-systems/actions/workflows/offline-core.yml/badge.svg)](https://github.com/gxmzung/vtol-mission-systems/actions/workflows/offline-core.yml)

> **Status: research prototype.** This repository provides Python mission logic and ROS 2 node scaffolds. The included PX4 bridge is a **stub**, not an authenticated/flight-tested PX4 connection. No physical aircraft should be controlled using these components.

## 외부 개발자용 빠른 재현

Python 3.11+로 클론한 저장소의 루트에서 다음 한 줄을 실행하세요.

```bash
python scripts/verify_offline.py
```

필수 구조 확인 → unittest → 스모크 테스트 → 오프라인 데모 순서로 실행하며 첫 실패에서 중단합니다. [재현성·증빙 기준](docs/OFFLINE_REPRODUCIBILITY.md) 및 [오프라인 CI](https://github.com/gxmzung/vtol-mission-systems/actions/workflows/offline-core.yml)를 참고하세요.

**검증 경계:** 이 경로는 순수 Python core와 PX4 브리지 *stub*만 시험합니다. ROS 2 Humble 빌드는 별도 CI이며, 실제 PX4 SITL·DDS 연결·비행 검증으로 대체할 수 없습니다. [SITL 증빙 프로토콜](docs/PX4_SITL_V5_EVIDENCE.md)을 참고하세요.

**프로젝트 구분:** 이 저장소는 ROS 2 텔레메트리 관측·검증 증빙에 초점을 두며, [VTOL Autonomy Lab](https://github.com/gxmzung/vtol-autonomy-lab)은 MAVSDK/가상 FC 기반 자율임무 및 고장 대응 로직에 초점을 둡니다.

## Goal

Build a reproducible, simulation-first portfolio around mission-state transitions, telemetry-based safety decisions, guidance calculations, and ROS 2 interface design. Every claimed capability has an explicit verification level.

| Capability | Existing implementation | Verified here |
| --- | --- | --- |
| Mission state machine | Python state transitions and FAILSAFE terminal state | Unit and smoke tests |
| Telemetry safety | Battery, signal, GNSS, temperature, altitude thresholds | Unit tests, boundary and invalid numeric inputs |
| Guidance | 3D waypoint distance and threshold checks | Unit tests |
| PX4 interface | Local in-memory bridge stub and ROS 2 message scaffold | Stub behavior only; **not** real PX4 |
| Vision | ArUco / line-tracking prototypes | Code present; integration not established |
| ROS 2 | Humble packages, mock DDS status and safety alerts | `colcon build` + ROS 2 runtime topic smoke CI; not PX4 SITL |
| PX4 SITL observer | Read-only `px4_msgs` interfaces, freshness validation | Unit + ROS 2 package CI only; live SITL still **NOT VERIFIED** |
| Evidence pipeline | ROS 2 observer JSONL recorder + metrics reporter | Pure Python tests and synthetic DDS recorder smoke; not live SITL proof |
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

The former project-branded workspace directory is now `ros2_ws/`. ROS 2 Humble CI verifies its package build and mock topic traffic, but **not live PX4 SITL integration**. Existing historical documentation is retained for provenance.

## Safety boundaries

1. **Simulated != PX4-connected != flight-tested.**
2. The existing ROS 2 bridge publishes mock status and is not an independent source of vehicle arming truth.
3. Invalid or non-finite telemetry readings are treated as unsafe in the dependency-free safety model.
4. Real-aircraft launch is disabled until there is a separately reviewed vehicle adapter, an independent operator-controlled safety path, and documented tests.
5. Do not use this research code to fly or control a physical aircraft.

See [Verification Matrix](docs/VERIFICATION_MATRIX.md), [ROS 2 Topic Contracts](docs/ROS2_CONTRACTS_V2.md), [V4 Read-Only Observer](docs/PX4_SITL_V4.md), [V5 Evidence Protocol](docs/PX4_SITL_V5_EVIDENCE.md), and [Migration Plan](docs/REFACTOR_PLAN.md).

## Development status

- **V1 — complete:** accurate scope, offline regression suite and disabled real-vehicle launch.
- **V2 — complete:** ROS 2 Humble `colcon build`, mock DDS topic communication and safety contract tests.
- **V3 — complete:** canonical ROS 2 Python packages and malformed/stale mock heartbeat handling.
- **V4 — implemented:** opt-in read-only PX4 telemetry adapter; **actual PX4 SITL link remains unverified**.
- **V5 — current:** JSONL evidence recorder, deterministic offline analyzer and synthetic DDS pipeline test. Live SITL experiments **not run**.
- **Future:** reproducible PX4 Gazebo + XRCE-DDS + matching `px4_msgs` experiment, measured dropout/recovery and independently reviewed logs.

## Project history and attribution

This repository evolved from an earlier VTOL competition/team project. Renaming the current portfolio **does not erase prior authorship, team involvement, or commit history**. Historical team documents and directories are retained until their provenance and reuse rights have been reviewed. This repository does not claim that all historical work was created solely by the current maintainer.

## Maintainer

[Youngjun Lee](https://github.com/gxmzung) · [LinkedIn](https://www.linkedin.com/in/youngjoon-gamjeong/)
