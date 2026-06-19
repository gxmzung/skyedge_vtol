# SkyEdge Consolidation Plan

This repository is the canonical SkyEdge VTOL mission stack.

## Consolidation Sources

| Source | Planned Use |
| --- | --- |
| skyedge_vtol | Canonical final repository |
| skyedge-vtol-ws | ROS2/PX4-style workspace code and test ideas |
| skyedge_mission | hardware prototype notes and ESP32/UDP experiments |
| SkyEdge-VTOL-System | project narrative and competition documentation |
| test_vtol_yejun | archive only, generated build artifacts excluded |

## Rules

- Keep source code, configs, and useful docs
- Remove build, install, log, and generated artifacts
- Do not merge duplicate experimental folders blindly
- Preserve only runnable or inspectable modules
- Keep safety boundaries clear