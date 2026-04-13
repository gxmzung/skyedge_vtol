# 빌드 및 실행 가이드

## 권장 환경
- Ubuntu 22.04
- ROS 2 Humble
- PX4 SITL
- QGroundControl

## 설치
```bash
cd ~/skyedge_vtol_final
bash scripts/install_ubuntu.sh
```

## 빌드
```bash
cd ~/skyedge_vtol_final
bash scripts/build_workspace.sh
```

## PX4 SITL 실행
```bash
cd ~/PX4-Autopilot
make px4_sitl gz_standard_vtol
```

## QGroundControl 실행
- PX4 SITL 실행 후 QGroundControl을 켠다.
- 연결 상태, 모드, HUD를 확인한다.

## ROS 2 실행
```bash
cd ~/skyedge_vtol_final
bash scripts/run_sim.sh
```

## 확인할 토픽
```bash
ros2 topic list
ros2 topic echo /mission/state
ros2 topic echo /vision/line_result
ros2 topic echo /vision/aruco_result
```
