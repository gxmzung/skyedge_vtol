# Mission Logic Test Notes

## Test Targets

| Module | Test |
| --- | --- |
| MissionStateMachine | state transition order |
| TelemetryHealth | safety rule evaluation |
| FailsafeManager | failsafe reason priority |
| WaypointGuidance | waypoint distance and reached status |
| PX4BridgeStub | command boundary outputs |

## Future Automated Tests

- pytest-based mission state tests
- waypoint calculation tests
- telemetry threshold tests
- failsafe transition tests