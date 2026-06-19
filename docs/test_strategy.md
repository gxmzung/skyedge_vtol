# SkyEdge Test Strategy

SkyEdge uses lightweight validation before full ROS2/PX4 integration.

## Current Test Layers

| Layer | Purpose |
| --- | --- |
| Structure check | Ensures important files and folders exist |
| Smoke test | Ensures core mission modules import and run |
| Manual test notes | Documents expected behavior for future automated tests |
| GitHub Actions | Runs basic checks on push and pull request |

## Current Smoke Test Coverage

- mission state transition
- failsafe trigger condition
- waypoint distance calculation
- PX4 bridge command boundary

## Future Test Plan

### v0.2

- pytest unit tests
- YAML mission config validation
- waypoint selection tests
- vision decision tests

### v0.3

- simulated telemetry replay
- mission timeline replay
- hardware prototype message parsing tests
- UDP packet loss simulation

### v1.0

- ROS2-style integration test
- PX4 offboard bridge mock test
- mission report generation
- CI badge and release checklist