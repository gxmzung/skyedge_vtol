from dataclasses import dataclass


@dataclass
class CompanionVisionResult:
    target_detected: bool
    offset_x: float
    offset_y: float
    confidence: float


class CompanionDeviceInterface:
    """
    Companion device interface scaffold.

    This layer represents data coming from a companion computer or ESP32-side module.
    It does not directly control flight behavior.
    """

    def parse_vision_message(self, message: str) -> CompanionVisionResult:
        values = {}

        for part in message.split(","):
            key, value = part.split("=")
            values[key] = value

        return CompanionVisionResult(
            target_detected=values.get("TARGET", "0") == "1",
            offset_x=float(values.get("OX", 0.0)),
            offset_y=float(values.get("OY", 0.0)),
            confidence=float(values.get("CONF", 0.0)),
        )

    def should_assist_precision_landing(self, result: CompanionVisionResult) -> bool:
        return result.target_detected and result.confidence >= 0.85