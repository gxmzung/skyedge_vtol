# SkyEdge VTOL Mission Stack

![SkyEdge CI](https://github.com/gxmzung/skyedge_vtol/actions/workflows/skyedge-ci.yml/badge.svg)

SkyEdge VTOL Mission Stack is a ROS 2 / PX4-based VTOL mission software prototype.

This repository focuses on the software layer around VTOL mission execution, including mission state management, PX4 bridge logic, safety handling, guidance logic, and vision-assisted mission support.

The project is not presented as a completed flight-certified system.  
It is a software-side mission stack prototype intended for simulation, architecture validation, and future hardware integration.

---

## Why This Project Exists

PX4 provides a reliable flight-control foundation, but a real mission system needs more than basic flight control.

This project explores the software layer needed around a VTOL platform:

- mission state transitions
- PX4 bridge / command interface
- safety fallback logic
- guidance logic
- vision-assisted detection
- simulation and real-flight launch separation
- parameter-based configuration

The goal is to reduce software uncertainty before connecting to real hardware.

---

## Core Principle

```text
PX4 handles low-level flight control.
SkyEdge handles mission logic, safety decisions, guidance, and vision-side software.
```

This repository treats simulation success as an intermediate checkpoint, not as final validation.

---

## Main Components

```text
skyedge_vtol/
├─ README.md
├─ docs/
│  └─ README.md
├─ src/
│  ├─ vtol_core/
│  │  ├─ mission_manager_node.py
│  │  ├─ px4_bridge_node.py
│  │  ├─ safety_manager.py
│  │  ├─ guidance_node.py
│  │  ├─ messages.py
│  │  ├─ state_defs.py
│  │  ├─ config/global_params.yaml
│  │  └─ launch/
│  │     ├─ sim_launch.py
│  │     └─ real_launch.py
│  │
│  └─ vtol_vision/
│     ├─ aruco_detector_node.py
│     └─ line_tracker_node.py
```

---

## Key Modules

### `vtol_core`

Mission and control-side logic.

- `mission_manager_node.py`  
  Manages mission state transitions and high-level mission flow.

- `px4_bridge_node.py`  
  Provides a bridge layer between mission logic and PX4-side commands or telemetry.

- `safety_manager.py`  
  Handles safety-state checks, fallback logic, and abnormal-condition handling.

- `guidance_node.py`  
  Contains guidance logic for mission execution.

- `state_defs.py`  
  Defines mission states and internal state representation.

- `messages.py`  
  Defines internal message/data structures used by the mission stack.

- `config/global_params.yaml`  
  Central configuration file for mission parameters.

### `vtol_vision`

Vision-side support nodes.

- `aruco_detector_node.py`  
  Prototype node for marker-based detection.

- `line_tracker_node.py`  
  Prototype node for line-tracking or visual guidance support.

---

## Launch Structure

The repository separates simulation and real-flight entry points.

```text
src/vtol_core/launch/sim_launch.py
src/vtol_core/launch/real_launch.py
```

This separation is important because simulation and real hardware should not share the same assumptions.

---

## Suggested Workflow

### 1. Review parameters

```bash
cat skyedge_vtol/src/vtol_core/config/global_params.yaml
```

### 2. Review mission core

```bash
ls skyedge_vtol/src/vtol_core
```

### 3. Review vision nodes

```bash
ls skyedge_vtol/src/vtol_vision
```

### 4. Run inside a ROS 2 workspace

This repository is intended to be placed inside a ROS 2 workspace structure.

Example:

```bash
mkdir -p ~/skyedge_ws/src
cd ~/skyedge_ws/src
git clone https://github.com/gxmzung/skyedge_vtol.git
cd ~/skyedge_ws
colcon build
source install/setup.bash
```

Then launch simulation-side logic after connecting the required PX4 / simulator environment.

```bash
ros2 launch vtol_core sim_launch.py
```

For real hardware integration, use the real launch entry only after configuration and safety checks.

```bash
ros2 launch vtol_core real_launch.py
```

---

## Tech Stack

- ROS 2 Humble
- PX4
- Python
- YAML configuration
- VTOL mission logic
- ArUco marker detection prototype
- Line tracking prototype
- Simulation-first validation workflow

---

## Current Status

This repository is a mission-stack prototype.

Implemented or scaffolded:

- mission manager node
- PX4 bridge node
- safety manager
- guidance node
- mission state definitions
- global parameter file
- simulation launch entry
- real launch entry
- ArUco detector node
- line tracker node

Not yet claimed:

- flight-certified safety
- real aircraft validation
- complete PX4 integration
- production deployment
- autonomous operation approval

---

---

## Validation

This repository includes lightweight validation scripts.

| Script | Role |
| --- | --- |
| `scripts/check_structure.py` | Checks required repository structure |
| `scripts/smoke_test.py` | Runs minimal mission-stack smoke tests |
| `.github/workflows/skyedge-ci.yml` | Runs checks through GitHub Actions |

The current validation target is not flight certification.  
It is repository-level sanity checking for mission software architecture.

---

## Engineering Notes

This project intentionally separates:

```text
flight control     -> PX4
mission logic      -> vtol_core
vision support     -> vtol_vision
configuration      -> YAML
simulation launch  -> sim_launch.py
real launch        -> real_launch.py
```

This structure makes it easier to reason about responsibility boundaries before hardware integration.

---

## Future Work

- Add simulation screenshots
- Add rqt_graph capture
- Add PX4 SITL connection guide
- Add QGroundControl workflow notes
- Add unit tests for mission state transitions
- Add safety scenario test cases
- Add a sample mission timeline
- Document real hardware connection assumptions

---

## Honest Limits

This project is not a finished VTOL autopilot.

It is a software-side mission stack prototype designed to show how PX4, ROS 2, mission management, safety handling, and vision nodes can be organized before moving toward real hardware integration.