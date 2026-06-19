# Precision Landing Flow

## Goal

Use visual detection results to support precision landing decisions.

## Flow

```text
Detect ArUco marker
        |
Detect landing zone target
        |
Compare confidence and offset
        |
Generate vision assist decision
        |
Mission manager decides whether to use advisory input

Decision Modes
Mode	Meaning
PRECISION_LANDING_ASSIST	ArUco and target detector agree
TARGET_APPROACH_ASSIST	Target detector is confident
NO_VISION_ASSIST	Vision confidence is insufficient
Constraints
Vision module must not directly command flight controller output
Low-confidence detection must be ignored
Manual override and failsafe always have priority
Detection result should be logged for later review