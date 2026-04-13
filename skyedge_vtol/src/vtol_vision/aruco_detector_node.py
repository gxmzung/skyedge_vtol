import json

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ArucoDetectorNode(Node):
    def __init__(self):
        super().__init__('aruco_detector_node')

        self.declare_parameter('camera_topic', '/camera/image_raw')
        self.declare_parameter('target_marker_id', 0)
        self.declare_parameter('publish_debug_image', True)

        self.camera_topic = self.get_parameter('camera_topic').get_parameter_value().string_value
        self.target_marker_id = self.get_parameter('target_marker_id').get_parameter_value().integer_value
        self.publish_debug_image = self.get_parameter('publish_debug_image').get_parameter_value().bool_value

        self.bridge = CvBridge()

        self.result_pub = self.create_publisher(String, '/vision/aruco_result', 10)
        self.debug_pub = self.create_publisher(Image, '/vision/aruco_debug', 10)

        self.image_sub = self.create_subscription(
            Image,
            self.camera_topic,
            self.image_callback,
            10,
        )

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()

        self.get_logger().info(f'Aruco detector subscribed to {self.camera_topic}')

    def image_callback(self, msg: Image):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge conversion failed: {e}')
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected = cv2.aruco.detectMarkers(
            gray,
            self.aruco_dict,
            parameters=self.aruco_params
        )

        result = {
            'detected': False,
            'target_id': int(self.target_marker_id),
            'marker_id': -1,
            'offset_x': 0.0,
            'offset_y': 0.0,
            'area': 0.0,
        }

        debug_frame = frame.copy()

        if ids is not None and len(ids) > 0:
            cv2.aruco.drawDetectedMarkers(debug_frame, corners, ids)

            ids_flat = ids.flatten()
            found_target = False

            for i, marker_id in enumerate(ids_flat):
                if int(marker_id) == int(self.target_marker_id):
                    pts = corners[i][0]
                    center_x = float(np.mean(pts[:, 0]))
                    center_y = float(np.mean(pts[:, 1]))

                    h, w = frame.shape[:2]
                    offset_x = (center_x - (w / 2.0)) / (w / 2.0)
                    offset_y = (center_y - (h / 2.0)) / (h / 2.0)

                    area = cv2.contourArea(pts.astype(np.float32))

                    result = {
                        'detected': True,
                        'target_id': int(self.target_marker_id),
                        'marker_id': int(marker_id),
                        'offset_x': float(offset_x),
                        'offset_y': float(offset_y),
                        'area': float(area),
                    }

                    cv2.circle(debug_frame, (int(center_x), int(center_y)), 6, (0, 255, 0), -1)
                    cv2.putText(
                        debug_frame,
                        f'id={marker_id} ox={offset_x:.2f} oy={offset_y:.2f}',
                        (int(center_x) + 10, int(center_y)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

                    found_target = True
                    break

            if not found_target:
                result['detected'] = False

        self.result_pub.publish(String(data=json.dumps(result)))

        if self.publish_debug_image:
            try:
                debug_msg = self.bridge.cv2_to_imgmsg(debug_frame, encoding='bgr8')
                debug_msg.header = msg.header
                self.debug_pub.publish(debug_msg)
            except Exception as e:
                self.get_logger().error(f'debug image publish failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()