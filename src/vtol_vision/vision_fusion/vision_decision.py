from dataclasses import dataclass


@dataclass
class VisionDecision:
    assist_mode: str
    offset_x: float
    offset_y: float
    confidence: float
    reason: str


def build_precision_landing_decision(
    aruco_valid: bool,
    target_valid: bool,
    offset_x: float,
    offset_y: float,
    confidence: float,
) -> VisionDecision:
    if aruco_valid and target_valid and confidence >= 0.85:
        return VisionDecision(
            assist_mode="PRECISION_LANDING_ASSIST",
            offset_x=offset_x,
            offset_y=offset_y,
            confidence=confidence,
            reason="Aruco and target detector agree",
        )

    if target_valid and confidence >= 0.85:
        return VisionDecision(
            assist_mode="TARGET_APPROACH_ASSIST",
            offset_x=offset_x,
            offset_y=offset_y,
            confidence=confidence,
            reason="Target detector is confident",
        )

    return VisionDecision(
        assist_mode="NO_VISION_ASSIST",
        offset_x=0.0,
        offset_y=0.0,
        confidence=confidence,
        reason="Vision confidence is not sufficient",
    )