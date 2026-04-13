import json
import time
from typing import Optional, Tuple

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ArucoDetectorNode(Node):
    def __init__(self) -> None:
        super().__init__('aruco_detector_node')

        self.declare_parameter('camera_topic', '/camera/image_raw')
        self.declare_parameter('aruco_dict_name', 'DICT_4X4_50')
        self.declare_parameter('aruco_target_id', 1)
        self.declare_parameter('aruco_marker_length_m', 0.15)
        self.declare_parameter('aruco_publish_debug', False)
        self.declare_parameter('aruco_no_image_timeout_sec', 1.0)

        self.camera_topic = self.get_parameter('camera_topic').value
        self.target_id = int(self.get_parameter('aruco_target_id').value)
        self.marker_length = float(self.get_parameter('aruco_marker_length_m').value)
        self.publish_debug = bool(self.get_parameter('aruco_publish_debug').value)
        self.timeout_sec = float(self.get_parameter('aruco_no_image_timeout_sec').value)

        dict_name = self.get_parameter('aruco_dict_name').value
        dict_id = getattr(cv2.aruco, dict_name, cv2.aruco.DICT_4X4_50)
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(dict_id)
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, cv2.aruco.DetectorParameters())

        self.bridge = CvBridge()
        self.last_image_ts = 0.0

        self.result_pub = self.create_publisher(String, '/vision/aruco_result', 10)
        self.debug_pub = self.create_publisher(Image, '/vision/aruco_debug', 10) if self.publish_debug else None
        self.image_sub = self.create_subscription(Image, self.camera_topic, self.on_image, 10)
        self.timer = self.create_timer(0.2, self.on_timer)

        self.get_logger().info(f'Aruco detector subscribed to {self.camera_topic}')

    def on_timer(self) -> None:
        if self.last_image_ts == 0.0:
            return
        if time.time() - self.last_image_ts > self.timeout_sec:
            self.publish_result(False, -1, 0.0, 0.0, 0.0, 0.0)

    def on_image(self, msg: Image) -> None:
        self.last_image_ts = time.time()
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        result = self.detect_marker(frame)
        found, target_id, offset_x, offset_y, area_ratio, distance_hint, debug_img = result
        self.publish_result(found, target_id, offset_x, offset_y, area_ratio, distance_hint)
        if self.debug_pub is not None and debug_img is not None:
            self.debug_pub.publish(self.bridge.cv2_to_imgmsg(debug_img, encoding='bgr8'))

    def detect_marker(self, frame: np.ndarray) -> Tuple[bool, int, float, float, float, float, Optional[np.ndarray]]:
        h, w = frame.shape[:2]
        corners, ids, _ = self.detector.detectMarkers(frame)
        debug_img = frame.copy() if self.publish_debug else None

        if ids is None or len(ids) == 0:
            return False, -1, 0.0, 0.0, 0.0, 0.0, debug_img

        ids_flat = ids.flatten().tolist()
        best_index = None
        if self.target_id in ids_flat:
            best_index = ids_flat.index(self.target_id)
        else:
            best_index = 0

        target_id = int(ids_flat[best_index])
        pts = corners[best_index][0]
        cx = float(np.mean(pts[:, 0]))
        cy = float(np.mean(pts[:, 1]))
        offset_x = (cx - (w / 2.0)) / (w / 2.0)
        offset_y = (cy - (h / 2.0)) / (h / 2.0)

        area = float(cv2.contourArea(pts.astype(np.float32)))
        area_ratio = min(area / max(float(w * h), 1.0), 1.0)
        distance_hint = 0.0
        if area > 1.0:
            distance_hint = (self.marker_length * 1000.0) / np.sqrt(area)

        if debug_img is not None:
            cv2.aruco.drawDetectedMarkers(debug_img, corners, ids)
            cv2.circle(debug_img, (int(cx), int(cy)), 6, (0, 0, 255), -1)
            cv2.putText(debug_img, f'id={target_id}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(debug_img, f'offset_x={offset_x:.3f}', (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
            cv2.putText(debug_img, f'area_ratio={area_ratio:.4f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        return True, target_id, float(offset_x), float(offset_y), float(area_ratio), float(distance_hint), debug_img

    def publish_result(self, found: bool, target_id: int, offset_x: float, offset_y: float, area_ratio: float, distance_hint: float) -> None:
        payload = {
            'found': bool(found),
            'target_id': int(target_id),
            'offset_x': float(offset_x),
            'offset_y': float(offset_y),
            'area_ratio': float(area_ratio),
            'distance_hint': float(distance_hint),
            'timestamp': time.time(),
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.result_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = ArucoDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
