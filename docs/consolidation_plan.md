# VTOL Mission Systems Consolidation Plan

This repository is the canonical VTOL Mission Systems VTOL mission stack.

## Consolidation Sources

| Source | Planned Use |
| --- | --- |
| ros2_ws | Canonical final repository |
| prior team ROS 2 workspace | ROS2/PX4-style workspace code and test ideas |
| skyedge_mission | hardware prototype notes and ESP32/UDP experiments |
| VTOL Mission Systems-VTOL-System | project narrative and competition documentation |
| test_vtol_yejun | archive only, generated build artifacts excluded |

## Rules

- Keep source code, configs, and useful docs
- Remove build, install, log, and generated artifacts
- Do not merge duplicate experimental folders blindly
- Preserve only runnable or inspectable modules
- Keep safety boundaries clear