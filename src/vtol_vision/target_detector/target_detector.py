from dataclasses import dataclass


@dataclass
class TargetDetection:
    label: str
    detected: bool
    offset_x: float
    offset_y: float
    confidence: float


class TargetDetector:
    """
    Target detector scaffold.

    Future implementation:
    - YOLO-style object detection
    - rescue target recognition
    - landing zone classification
    - mission-layer advisory output
    """

    def detect_mock_target(self, frame_id: int) -> TargetDetection:
        samples = {
            1: TargetDetection("landing_zone", True, 0.10, -0.05, 0.89),
            2: TargetDetection("rescue_marker", True, -0.18, 0.07, 0.86),
            3: TargetDetection("unknown", False, 0.0, 0.0, 0.12),
        }

        return samples.get(frame_id, TargetDetection("unknown", False, 0.0, 0.0, 0.0))

    def is_target_actionable(self, detection: TargetDetection) -> bool:
        return detection.detected and detection.confidence >= 0.85