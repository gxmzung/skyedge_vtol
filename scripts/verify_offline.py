"""Hardware-free offline evidence gate; no ROS 2, PX4 or vehicle needed."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = (
    ("structure", [sys.executable, "scripts/check_structure.py"]),
    ("core-tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
    ("smoke", [sys.executable, "scripts/smoke_test.py"]),
)
# The deterministic virtual-only demonstration must produce the expected
# failsafe outcome. An exit code of zero is insufficient as evidence.
EXPECTED_DEMO_LINES = ("FAILSAFE: LOW_BATTERY", "FINAL STATE: FAILSAFE")


def verify_demo_output(output: str) -> bool:
    """Reject a nominally successful subprocess with the wrong demo outcome."""
    lines = {line.strip() for line in output.splitlines()}
    return all(expected in lines for expected in EXPECTED_DEMO_LINES)


def main() -> int:
    for label, command in STEPS:
        print(f"\n[offline] {label}: {' '.join(command)}", flush=True)
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            print(f"[offline] FAILED {label}: exit {completed.returncode}", file=sys.stderr)
            return completed.returncode

    demo = [sys.executable, "src/vtol/mission_demo.py"]
    print(f"\n[offline] demo: {' '.join(demo)}", flush=True)
    outcome = subprocess.run(demo, cwd=ROOT, check=False, capture_output=True, text=True)
    print(outcome.stdout, end="", flush=True)
    if outcome.stderr:
        print(outcome.stderr, file=sys.stderr, end="", flush=True)
    if outcome.returncode != 0:
        print(f"[offline] FAILED demo: exit {outcome.returncode}", file=sys.stderr)
        return outcome.returncode
    if not verify_demo_output(outcome.stdout):
        print("[offline] FAILED demo: expected LOW_BATTERY and FAILSAFE outcome absent", file=sys.stderr)
        return 1

    print("\n[offline] PASS: offline tests + asserted demo outcome.")
    print("[offline] NOT evidence of live PX4, SITL or aircraft safety.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
