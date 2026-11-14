"""Offline analysis of recorded PX4 SITL observer snapshots.

A JSONL analysis is not PX4 SITL authentication or flight validation.
No real telemetry is bundled or fabricated by this module.
"""
import argparse
import json
import math
from pathlib import Path

CHANNELS = ("vehicle_status", "local_position", "battery_status")


def summarize(records):
    """Return descriptive metrics and safety flags, never a live-PX4 PASS."""
    if not isinstance(records, list) or not records:
        raise ValueError("At least one observation record is required")
    last_t = None
    counts = {name: 0 for name in CHANNELS}
    stale_windows = 0
    recovered = 0
    previously_fresh = None
    rows = 0
    durations = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("record must be an object")
        t = record.get("recorded_monotonic_s")
        if type(t) not in (int, float) or not math.isfinite(t) or t < 0:
            raise ValueError("invalid observation monotonic timestamp")
        if last_t is not None and t <= last_t:
            raise ValueError("timestamps must be strictly increasing")
        if last_t is not None:
            durations.append(t - last_t)
        last_t = t
        snap = record.get("snapshot")
        if not isinstance(snap, dict):
            raise ValueError("snapshot must be an object")
        if snap.get("mode") != "sitl_observation_only":
            raise ValueError("not a SITL-observation snapshot")
        if snap.get("read_only") is not True or snap.get("actuation_authorized") is not False:
            raise ValueError("unsafe or malformed observation contract")
        ch = snap.get("channels")
        if not isinstance(ch, dict):
            raise ValueError("missing channels")
        for name in CHANNELS:
            value = ch.get(name)
            if not isinstance(value, dict) or type(value.get("fresh")) is not bool:
                raise ValueError("invalid channel state: " + name)
            if value["fresh"]:
                counts[name] += 1
        fresh = bool(ch["vehicle_status"]["fresh"] and ch["local_position"]["fresh"])
        if type(snap.get("telemetry_fresh")) is not bool or snap["telemetry_fresh"] != fresh:
            raise ValueError("inconsistent freshness indicator")
        if previously_fresh is True and not fresh:
            stale_windows += 1
        if previously_fresh is False and fresh:
            recovered += 1
        previously_fresh = fresh
        rows += 1

    first_t = records[0]["recorded_monotonic_s"]
    duration = last_t - first_t
    return {
        "schema": "vtol-sitl-evidence-v1",
        "verification": "ANALYSIS_ONLY_NOT_LIVE_SITL_PROOF",
        "observations": rows,
        "duration_s": round(duration, 3),
        "mean_record_interval_s": round(sum(durations) / len(durations), 3) if durations else None,
        "channel_fresh_percent": {name: round(100.0 * counts[name] / rows, 2) for name in CHANNELS},
        "combined_fresh_percent": round(100.0 * sum(
            1 for rec in records if rec["snapshot"]["telemetry_fresh"]
        ) / rows, 2),
        "fresh_to_stale_transitions": stale_windows,
        "stale_to_fresh_transitions": recovered,
        "limits": [
            "These metrics reflect the supplied observer log, not authenticated PX4 connectivity.",
            "Observation sampling rate is not raw PX4 topic publishing rate.",
            "Live SITL verification requires a matching version matrix and independently reviewed run logs.",
        ],
    }


def read_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except (ValueError, TypeError) as exc:
                raise ValueError(f"invalid JSONL at line {line_number}") from exc
    return records


def main():
    parser = argparse.ArgumentParser(description="Analyze observer JSONL without claiming SITL certification")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    report = summarize(read_jsonl(args.input))
    payload = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as target:
            target.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
