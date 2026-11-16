# Capture Checklist

## 필수 캡처

- [ ] `mission.yaml` waypoint 설정 화면
- [ ] `mission_node.py` 코드 화면
- [ ] PX4 SITL 실행 터미널
- [ ] Micro XRCE-DDS Agent 실행 터미널
- [ ] ROS2 mission node 실행 로그
- [ ] Gazebo 드론 시뮬레이션 화면
- [ ] QGroundControl 상태 화면
- [ ] `rqt_graph` 노드 구조 화면

## 로그 예시

```text
[MISSION] Start mission: campus_facility_inspection_demo
[MISSION] Waypoint count: 4
[MISSION] Switching to Offboard mode
[MISSION] Arming vehicle
[MISSION] Moving to takeoff_hover: x=0.0, y=0.0, z=-5.0
[MISSION] Moving to inspect_point_1: x=5.0, y=0.0, z=-5.0
[MISSION] Moving to inspect_point_2: x=5.0, y=5.0, z=-5.0
[MISSION] Moving to return_point: x=0.0, y=0.0, z=-5.0
[MISSION] Mission completed. Holding last position.
```
