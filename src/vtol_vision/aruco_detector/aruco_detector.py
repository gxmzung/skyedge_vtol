from dataclasses import dataclass


@dataclass
class ArucoDetection:
    marker_id: int
    center_x: float
    center_y: float
    confidence: float


class ArucoDetector:
    """
    ArUco detector scaffold.

    Future implementation:
    - OpenCV camera frame input
    - marker dictionary selection
    - pose estimation
    - landing target alignment
    """

    def detect_from_mock_frame(self, frame_id: int) -> ArucoDetection | None:
        mock_results = {
            1: ArucoDetection(marker_id=7, center_x=0.52, center_y=0.48, confidence=0.93),
            2: ArucoDetection(marker_id=7, center_x=0.50, center_y=0.51, confidence=0.95),
            3: None,
        }

        return mock_results.get(frame_id, None)

    def is_landing_marker_valid(self, detection: ArucoDetection | None) -> bool:
        if detection is None:
            return False

        return detection.confidence >= 0.85