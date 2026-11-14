"""Pure-Python, read-only PX4 SITL telemetry observation and freshness checks.

This module never publishes vehicle commands or claims flight readiness.
PX4-compatible message objects are converted into small validated snapshots.
All timing uses a local monotonic receive clock, not PX4 boot timestamps.
"""
from dataclasses import dataclass, field
import math
import time


def _finite(value):
    return type(value) in (int, float) and math.isfinite(value)


@dataclass
class SITLTelemetryMonitor:
    max_age_s: float = 2.0
    _samples: dict = field(default_factory=dict)

    def __post_init__(self):
        if not _finite(self.max_age_s) or self.max_age_s <= 0:
            raise ValueError("max_age_s must be a positive finite number")

    def ingest_vehicle_status(self, message, received_at=None):
        arming_state = getattr(message, "arming_state", None)
        nav_state = getattr(message, "nav_state", None)
        if not all(type(x) is int and 0 <= x <= 255 for x in (arming_state, nav_state)):
            return False
        return self._store("vehicle_status", {"arming_state": arming_state, "nav_state": nav_state}, received_at)

    def ingest_local_position(self, message, received_at=None):
        x, y, z = (getattr(message, k, None) for k in ("x", "y", "z"))
        xy_valid = getattr(message, "xy_valid", None)
        z_valid = getattr(message, "z_valid", None)
        if not all(_finite(v) for v in (x, y, z)) or type(xy_valid) is not bool or type(z_valid) is not bool:
            return False
        if not xy_valid or not z_valid:
            return False
        return self._store("local_position", {"x": float(x), "y": float(y), "z": float(z)}, received_at)

    def ingest_battery_status(self, message, received_at=None):
        remaining = getattr(message, "remaining", None)
        if not _finite(remaining) or not 0.0 <= remaining <= 1.0:
            return False
        return self._store("battery_status", {"remaining": float(remaining)}, received_at)

    def _store(self, topic, data, received_at):
        stamp = time.monotonic() if received_at is None else received_at
        if not _finite(stamp) or stamp < 0:
            return False
        previous = self._samples.get(topic)
        if previous is not None and stamp < previous[0]:
            return False
        self._samples[topic] = (float(stamp), data)
        return True

    def snapshot(self, now=None):
        stamp = time.monotonic() if now is None else now
        if not _finite(stamp) or stamp < 0:
            raise ValueError("now must be a valid monotonic timestamp")
        channels = {}
        for topic in ("vehicle_status", "local_position", "battery_status"):
            sample = self._samples.get(topic)
            age = stamp - sample[0] if sample else None
            fresh = bool(sample and 0 <= age <= self.max_age_s)
            channels[topic] = {"fresh": fresh, "age_s": round(age, 3) if age is not None and _finite(age) else None,
                               "data": sample[1] if fresh else None}
        # Do not use a "connected" flag: DDS samples alone cannot establish PX4 identity,
        # authoritative arming state, or permission to issue commands.
        return {
            "mode": "sitl_observation_only",
            "read_only": True,
            "actuation_authorized": False,
            "telemetry_fresh": channels["vehicle_status"]["fresh"] and channels["local_position"]["fresh"],
            "channels": channels,
        }
