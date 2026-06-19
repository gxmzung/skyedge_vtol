# SkyEdge VTOL Architecture

SkyEdge VTOL is organized as a mission-software stack.

## Core Flow

```text
Mission Manager
      |
      +--> Telemetry Health Monitor
      |
      +--> Safety / Failsafe Manager
      |
      +--> Guidance / Waypoint Logic
      |
      +--> PX4 Bridge

Design Boundary

This repository does not directly control a real aircraft.

It models the software architecture around:

mission state transitions
telemetry-based safety checks
waypoint-level guidance logic
PX4 offboard integration boundaries
simulation-first validation