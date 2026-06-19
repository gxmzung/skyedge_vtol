from aruco_detector.aruco_detector import ArucoDetector
from target_detector.target_detector import TargetDetector
from vision_fusion.vision_decision import build_precision_landing_decision


def main():
    aruco = ArucoDetector()
    target = TargetDetector()

    print("SkyEdge vision module demo started")

    for frame_id in [1, 2, 3]:
        aruco_result = aruco.detect_from_mock_frame(frame_id)
        target_result = target.detect_mock_target(frame_id)

        aruco_valid = aruco.is_landing_marker_valid(aruco_result)
        target_valid = target.is_target_actionable(target_result)

        decision = build_precision_landing_decision(
            aruco_valid=aruco_valid,
            target_valid=target_valid,
            offset_x=target_result.offset_x,
            offset_y=target_result.offset_y,
            confidence=target_result.confidence,
        )

        print(f"FRAME={frame_id}")
        print(f"  TARGET={target_result.label} DETECTED={target_result.detected}")
        print(f"  ASSIST={decision.assist_mode} REASON={decision.reason}")

    print("SkyEdge vision module demo finished")


if __name__ == "__main__":
    main()