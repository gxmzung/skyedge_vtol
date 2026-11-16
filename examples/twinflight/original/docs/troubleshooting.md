# Troubleshooting

## ros2 topic list에서 /fmu 토픽이 안 보일 때

- PX4 SITL이 실행 중인지 확인한다.
- Micro XRCE-DDS Agent가 실행 중인지 확인한다.
- PX4 버전과 px4_msgs 버전이 맞는지 확인한다.

## colcon build에서 px4_msgs를 찾지 못할 때

`px4_msgs` 패키지가 ROS2 워크스페이스에 없거나 빌드되지 않은 상태일 수 있다.
PX4 공식 ROS2 사용자 가이드에 따라 `px4_msgs`를 워크스페이스에 추가해야 한다.

## mission.yaml을 못 찾을 때

launch 파일로 실행하거나, 절대경로를 넘긴다.

```bash
ros2 launch twinflight_mission mission.launch.py mission_file:=/absolute/path/to/mission.yaml
```

## 실제 기체 연결 금지

이 프로젝트는 발표용 SITL 시뮬레이션 데모다.
실제 기체에 연결하지 않는다.
