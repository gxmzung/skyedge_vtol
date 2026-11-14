"""Strict, ROS-independent validation for prototype JSON topic contracts.

A ROS 2 String message is not equivalent to verified PX4 telemetry.
All values fail closed and unknown/malformed payloads are rejected.
"""
import json
import math


def parse_status(raw: str) -> dict:
    try:
        d = json.loads(raw)
    except (ValueError, TypeError):
        return {"connected": False, "simulated": True}
    if not isinstance(d, dict):
        return {"connected": False, "simulated": True}
    # No externally supplied status can authorize the prototype to claim
    # a real PX4 link. The research bridge is always simulated.
    return {"connected": False, "simulated": True}


def parse_detection(raw: str) -> bool:
    try:
        d = json.loads(raw)
    except (ValueError, TypeError):
        return False
    if not isinstance(d, dict) or type(d.get("found")) is not bool:
        return False
    stamp = d.get("timestamp")
    if stamp is not None and (type(stamp) not in (int, float) or not math.isfinite(stamp)):
        return False
    return d["found"]
