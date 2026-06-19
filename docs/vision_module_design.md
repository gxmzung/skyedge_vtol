# Vision Module Design

SkyEdge VTOL includes a vision-assisted mission layer.

The vision module is designed to provide advisory information to the mission stack.

It does not directly override PX4 control.

## Modules

| Module | Role |
| --- | --- |
| ArUco Detector | Detect landing markers and estimate alignment |
| Line Tracker | Detect visual path lines and heading error |
| Target Detector | Detect rescue markers or landing zone targets |
| Vision Fusion | Combine detection results into mission-layer decisions |

## Data Flow

```text
Camera / Mock Frame
        |
        +--> ArUco Detector
        +--> Line Tracker
        +--> Target Detector
        |
        v
Vision Fusion
        |
        v
Mission Manager Advisory Input

Safety Boundary

Vision output is advisory.

The mission manager may use it for:

precision landing assist
search zone confirmation
target approach assist
alignment recommendation

PX4 control authority remains separate.