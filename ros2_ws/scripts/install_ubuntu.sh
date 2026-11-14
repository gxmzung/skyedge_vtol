#!/usr/bin/env bash
set -e

sudo apt update
sudo apt install -y \
  git curl wget python3-pip python3-colcon-common-extensions \
  python3-rosdep python3-vcstool python3-argcomplete build-essential \
  cmake ninja-build python3-opencv

echo "[INFO] 기본 시스템 패키지 설치 완료"
echo "[INFO] ROS 2 Humble과 PX4는 별도 공식 절차로 설치하세요."
