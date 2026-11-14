# Refactor & Provenance Plan

## Scope of V1

- Rebrand active documentation as **VTOL Mission Systems**, not as the original team/product name.
- Maintain repository history and attribution; do **not** rewrite history for branding purposes.
- Improve dependency-free telemetry safety and add reproducible unit tests.
- Disable legacy real-aircraft launch, since its previous content duplicated the simulation entry.
- Move the legacy source layout into `ros2_ws/` without modifying its package internals; source ownership and package builds are still under review.

## Existing duplication that needs V2 attention

- **Resolved in V3 branch:** duplicate top-level `ros2_ws/src/vtol_core/*.py`; canonical package modules remain in `vtol_core/vtol_core/`.
- **Resolved in V3 branch:** duplicate top-level `ros2_ws/src/vtol_vision/*.py`; canonical package modules remain in `vtol_vision/vtol_vision/`.
- Independent prototype code under root `src/vtol` and ROS 2 node scaffolds under the nested legacy directory

The package-import version and installed console-script entry points must be checked using a real ROS 2 environment before deleting either copy.

## V2 acceptance criteria

1. Record file origins and team contributions before copying from historical archives.
2. Normalize duplicated ROS 2 source files under `ros2_ws/src/` without changing the verified import/entrypoint contract.
3. `colcon build`, `ros2 pkg executables`, and ROS 2 launch tests pass on documented versions.
4. Publish architecture diagram, topic contract table and failure-state test cases.
5. No new ROS 2/PX4 functionality is marked verified solely because files exist.

## V3 acceptance criteria

- SITL-only adapter using explicit PX4 message types.
- Contract tests for timestamp, coordinate frame, stale/lost telemetry and state transitions.
- Separate simulation launch and a **not-shipped** real-aircraft adapter.
- Archived logs and reproducible environment information.

## Attribution

The repository originates in earlier team/competition research. Keep commit history and historical acknowledgments. Brand names in archived material may be retained as factual provenance; remove only from current product-facing descriptions and code paths when it is technically safe.

## V3 duplicate-removal gate

- Preserve `setup.py`, `setup.cfg`, `package.xml` and the canonical importable module directory for each ROS 2 package.
- Delete only top-level shadow Python modules, never the installable package or Git authorship history.
- Require Humble `colcon build`, console-script discovery, existing DDS smoke, and stale-heartbeat alert smoke to pass.
- Failure to observe a mock-bridge status MUST NOT count as physical PX4 connectivity.
- Passing smoke tests never implies PX4 SITL or flight validation.
