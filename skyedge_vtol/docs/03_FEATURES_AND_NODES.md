# 기능 및 노드 설명

## vtol_core
### px4_bridge_node
- PX4 상태 수신
- arm / offboard / land 명령 전송
- local position, status publish

### mission_manager_node
- 대회 상태머신 관리
- 탐색, 정렬, 구조, 복귀, 착륙 전이 담당

### guidance_node
- 비전 결과를 제어 setpoint로 변환

### safety_manager
- timeout, 미검출, 연결 끊김 등 감시

## vtol_vision
### line_tracker_node
- 카메라 영상에서 라인 검출
- 중심 오차를 정규화하여 publish

### aruco_detector_node
- ArUco 마커 검출
- 타깃 ID, 중심 오차, 추정 거리 정보를 publish
