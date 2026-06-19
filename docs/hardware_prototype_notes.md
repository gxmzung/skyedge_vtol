# Hardware Prototype Notes

SkyEdge VTOL includes hardware-adjacent prototype modules for future companion-device and embedded integration.

## Prototype Areas

| Area | Purpose |
| --- | --- |
| ESP32 Vision Receiver | Receive vision detection packets over UDP |
| ESP32 IMU Probe | Bring-up sketch for IMU-style telemetry output |
| UDP Tools | Send simulated detection messages for testing |
| Companion Device Interface | Parse companion-module messages in the mission stack |

## Boundary

These files are prototype scaffolds.

They do not directly control a real aircraft and are not flight-certified.

Their role is to document and test the software boundary between:

```text
Vision / Sensor Device
        |
        v
Companion Interface
        |
        v
Mission Stack
        |
        v
PX4 Bridge

Future Work
replace mock IMU values with real sensor driver output
define packet checksum
add message timestamp
add packet loss detection
connect companion-device data to mission safety rules