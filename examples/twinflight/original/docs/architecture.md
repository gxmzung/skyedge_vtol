# Architecture

## v2 핵심 구조

```text
mission.yaml
    ↓
MissionPlanner
    - waypoint 목록 로드
    - 임무 이름/설명 로드

    ↓

TwinFlightMissionNode
    - OffboardControlMode publish
    - TrajectorySetpoint publish
    - VehicleCommand publish
    - mission log 기록

    ↓

uXRCE-DDS / PX4 ROS2 Bridge

    ↓

PX4 SITL
    - 비행 모드 관리
    - 자세 제어
    - 위치 제어
    - 고도 유지
    - 모터 출력 제어

    ↓

Gazebo Drone
```

## 발표용 핵심 문장

ROS2가 임무 경로와 목표 위치를 생성하고, PX4가 해당 명령을 받아 실제 비행 안정화를 수행한다.
