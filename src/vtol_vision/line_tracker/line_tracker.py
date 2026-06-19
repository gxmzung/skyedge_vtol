from dataclasses import dataclass


@dataclass
class LineTrackResult:
    line_detected: bool
    offset_x: float
    angle_error: float
    confidence: float


class LineTracker:
    """
    Line tracker scaffold.

    Future implementation:
    - OpenCV thresholding
    - contour detection
    - path line extraction
    - heading correction suggestion
    """

    def analyze_mock_frame(self, frame_id: int) -> LineTrackResult:
        samples = {
            1: LineTrackResult(True, 0.12, -4.5, 0.88),
            2: LineTrackResult(True, 0.06, -2.1, 0.91),
            3: LineTrackResult(False, 0.0, 0.0, 0.20),
        }

        return samples.get(frame_id, LineTrackResult(False, 0.0, 0.0, 0.0))

    def should_correct_heading(self, result: LineTrackResult) -> bool:
        return result.line_detected and abs(result.angle_error) >= 3.0 and result.confidence >= 0.75