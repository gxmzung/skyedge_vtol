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


class LineTrackerNode(Node):
    def __init__(self) -> None:
        super().__init__('line_tracker_node')

        self.declare_parameter('camera_topic', '/camera/image_raw')
        self.declare_parameter('line_roi_ratio', 0.45)
        self.declare_parameter('line_min_area', 500.0)
        self.declare_parameter('line_publish_debug', False)
        self.declare_parameter('line_lower_hsv', [15, 60, 60])
        self.declare_parameter('line_upper_hsv', [40, 255, 255])
        self.declare_parameter('line_no_image_timeout_sec', 1.0)

        self.camera_topic = self.get_parameter('camera_topic').value
        self.roi_ratio = float(self.get_parameter('line_roi_ratio').value)
        self.min_area = float(self.get_parameter('line_min_area').value)
        self.publish_debug = bool(self.get_parameter('line_publish_debug').value)
        self.lower_hsv = np.array(self.get_parameter('line_lower_hsv').value, dtype=np.uint8)
        self.upper_hsv = np.array(self.get_parameter('line_upper_hsv').value, dtype=np.uint8)
        self.timeout_sec = float(self.get_parameter('line_no_image_timeout_sec').value)

        self.bridge = CvBridge()
        self.last_image_ts = 0.0

        self.result_pub = self.create_publisher(String, '/vision/line_result', 10)
        self.debug_pub = self.create_publisher(Image, '/vision/line_debug', 10) if self.publish_debug else None
        self.image_sub = self.create_subscription(Image, self.camera_topic, self.on_image, 10)
        self.timer = self.create_timer(0.2, self.on_timer)

        self.get_logger().info(f'Line tracker subscribed to {self.camera_topic}')

    def on_timer(self) -> None:
        if self.last_image_ts == 0.0:
            return
        if time.time() - self.last_image_ts > self.timeout_sec:
            self.publish_result(False, 0.0, 0.0, 0.0, 0.0)

    def on_image(self, msg: Image) -> None:
        self.last_image_ts = time.time()
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        result = self.detect_line(frame)
        found, offset_x, offset_y, angle_deg, confidence, debug_img = result
        self.publish_result(found, offset_x, offset_y, angle_deg, confidence)
        if self.debug_pub is not None and debug_img is not None:
            self.debug_pub.publish(self.bridge.cv2_to_imgmsg(debug_img, encoding='bgr8'))

    def detect_line(self, frame: np.ndarray) -> Tuple[bool, float, float, float, float, Optional[np.ndarray]]:
        h, w = frame.shape[:2]
        roi_start = int(h * (1.0 - self.roi_ratio))
        roi = frame[roi_start:, :]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        debug_img = roi.copy() if self.publish_debug else None

        if not contours:
            return False, 0.0, 0.0, 0.0, 0.0, debug_img

        contour = max(contours, key=cv2.contourArea)
        area = float(cv2.contourArea(contour))
        if area < self.min_area:
            return False, 0.0, 0.0, 0.0, 0.0, debug_img

        m = cv2.moments(contour)
        if m['m00'] == 0:
            return False, 0.0, 0.0, 0.0, 0.0, debug_img

        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        offset_x = (cx - (w / 2.0)) / (w / 2.0)
        offset_y = ((cy + roi_start) - h) / h

        rect = cv2.minAreaRect(contour)
        angle_deg = float(rect[2])
        confidence = min(area / max((w * h * self.roi_ratio), 1.0), 1.0)

        if debug_img is not None:
            cv2.drawContours(debug_img, [contour], -1, (0, 255, 0), 2)
            cv2.circle(debug_img, (cx, cy), 6, (0, 0, 255), -1)
            cv2.line(debug_img, (w // 2, 0), (w // 2, debug_img.shape[0]), (255, 0, 0), 1)
            cv2.putText(debug_img, f'offset_x={offset_x:.3f}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            cv2.putText(debug_img, f'angle={angle_deg:.1f}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        return True, float(offset_x), float(offset_y), angle_deg, confidence, debug_img

    def publish_result(self, found: bool, offset_x: float, offset_y: float, angle_deg: float, confidence: float) -> None:
        payload = {
            'found': bool(found),
            'offset_x': float(offset_x),
            'offset_y': float(offset_y),
            'angle_deg': float(angle_deg),
            'confidence': float(confidence),
            'timestamp': time.time(),
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.result_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = LineTrackerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
