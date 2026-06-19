from telemetry.telemetry_health import TelemetryHealth


class FailsafeManager:
    def should_trigger(self, health: TelemetryHealth) -> bool:
        return not health.is_mission_safe()

    def reason(self, health: TelemetryHealth) -> str:
        if not health.is_battery_safe():
            return "LOW_BATTERY"

        if not health.is_signal_safe():
            return "LOW_SIGNAL"

        if not health.is_gps_safe():
            return "GPS_UNSAFE"

        if not health.is_temperature_safe():
            return "HIGH_TEMPERATURE"

        if not health.is_altitude_reasonable():
            return "ALTITUDE_OUT_OF_RANGE"

        return "MISSION_SAFE"