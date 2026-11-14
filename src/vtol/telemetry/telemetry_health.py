from dataclasses import dataclass
from math import isfinite


@dataclass
class TelemetryHealth:
    battery_percent: float
    signal_strength: float
    gps_satellites: int
    temperature: float
    altitude: float

    def is_battery_safe(self) -> bool:
        return isfinite(self.battery_percent) and 25.0 <= self.battery_percent <= 100.0

    def is_signal_safe(self) -> bool:
        return isfinite(self.signal_strength) and 40.0 <= self.signal_strength <= 100.0

    def is_gps_safe(self) -> bool:
        return type(self.gps_satellites) is int and 8 <= self.gps_satellites <= 100

    def is_temperature_safe(self) -> bool:
        return isfinite(self.temperature) and -40.0 <= self.temperature <= 75.0

    def is_altitude_reasonable(self) -> bool:
        return isfinite(self.altitude) and 0.0 <= self.altitude <= 120.0

    def is_mission_safe(self) -> bool:
        return (
            self.is_battery_safe()
            and self.is_signal_safe()
            and self.is_gps_safe()
            and self.is_temperature_safe()
            and self.is_altitude_reasonable()
        )
