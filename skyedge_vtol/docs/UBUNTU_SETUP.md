# Ubuntu 22.04 Setup

## 권장 환경
- Ubuntu 22.04
- ROS 2 Humble
- Python 3.10+
- QGroundControl
- PX4-Autopilot

## 1. 시스템 패키지 설치
```bash
sudo apt update
sudo apt install -y git curl wget python3-pip python3-colcon-common-extensions \
    python3-rosdep python3-vcstool python3-argcomplete build-essential \
    cmake ninja-build
```

## 2. ROS 2 Humble 설치
공식 ROS 2 Humble 설치 절차를 따릅니다.  
설치 후:
```bash
source /opt/ros/humble/setup.bash
```

## 3. rosdep 초기화
```bash
sudo rosdep init
rosdep update
```

## 4. PX4 준비
```bash
cd ~
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
bash ./Tools/setup/ubuntu.sh
```

## 5. QGroundControl
QGroundControl AppImage를 내려받아 실행 권한을 부여합니다.
```bash
chmod +x QGroundControl.AppImage
./QGroundControl.AppImage
```

## 6. 이 프로젝트 빌드
```bash
cd ~/skyedge_vtol_final
bash scripts/build_workspace.sh
```

## 7. PX4 SITL 실행
```bash
cd ~/PX4-Autopilot
make px4_sitl gz_standard_vtol
```

## 8. ROS 2 실행
다른 터미널:
```bash
cd ~/skyedge_vtol_final
source /opt/ros/humble/setup.bash
source install/setup.bash
bash scripts/run_sim.sh
```

## 확인 포인트
- QGroundControl에서 기체 연결 확인
- `ros2 topic list` 에 PX4 관련 토픽 확인
- `/mission/state`, `/guidance/setpoint` 출력 확인
