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
    ("demo", [sys.executable, "src/vtol/mission_demo.py"]),
)

def main() -> int:
    for label, command in STEPS:
        print(f"\n[offline] {label}: {' '.join(command)}", flush=True)
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            print(f"[offline] FAILED {label}: exit {completed.returncode}", file=sys.stderr)
            return completed.returncode
    print("\n[offline] All commands exited successfully; NOT live PX4/SITL evidence.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
