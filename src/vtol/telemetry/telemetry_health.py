from dataclasses import dataclass


@dataclass
class TelemetryHealth:
    battery_percent: float
    signal_strength: float
    gps_satellites: int
    temperature: float
    altitude: float

    def is_battery_safe(self) -> bool:
        return self.battery_percent >= 25.0

    def is_signal_safe(self) -> bool:
        return self.signal_strength >= 40.0

    def is_gps_safe(self) -> bool:
        return self.gps_satellites >= 8

    def is_temperature_safe(self) -> bool:
        return self.temperature <= 75.0

    def is_altitude_reasonable(self) -> bool:
        return 0.0 <= self.altitude <= 120.0

    def is_mission_safe(self) -> bool:
        return (
            self.is_battery_safe()
            and self.is_signal_safe()
            and self.is_gps_safe()
            and self.is_temperature_safe()
            and self.is_altitude_reasonable()
        )