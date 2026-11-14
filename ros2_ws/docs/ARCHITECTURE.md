# Architecture

## 목표
이 프로젝트는 **PX4 위에 얹는 대회용 자율임무 소프트웨어**입니다.  
FC 자체개발 프로젝트가 아닙니다. FC 자체개발은 별도 장기 과제로 분리합니다.

## 노드 구성

### 1. px4_bridge_node
역할:
- PX4 상태 수신
- vehicle command 송신
- offboard setpoint 송신
- PX4 토픽을 팀 내부 토픽 구조로 정리

입력:
- `/guidance/setpoint`
- `/mission/command`

출력:
- `/px4_bridge/status`
- `/px4_bridge/local_position`
- `/px4_bridge/mission_feedback`

### 2. mission_manager_node
역할:
- 대회 상태머신
- 탐색, 정렬, 구조, 복귀, 착륙 흐름 관리
- timeout, fallback, abort 결정

주요 상태:
- IDLE
- ARMING
- TAKEOFF
- SEARCH_LINE
- FOLLOW_LINE
- SEARCH_MARKER
- ALIGN_MARKER
- RESCUE_ACTION
- RETURN_HOME
- LAND
- FAILSAFE

### 3. guidance_node
역할:
- vision / mission 결과를 실제 setpoint로 변환
- hover, line-follow, marker-align, return-home guidance 생성

### 4. line_tracker_node
역할:
- 카메라 입력에서 라인 검출
- 중심 오차, 검출 여부 publish

### 5. aruco_detector_node
역할:
- ArUco 검출
- marker id, 중심 오차, 거리 추정 publish

### 6. safety_manager
역할:
- 토픽 끊김, 검출 실패, setpoint timeout 감시
- FAILSAFE 전환 보조

## 데이터 흐름
```text
Camera
  ↓
Vision Nodes
  ↓
Mission Manager ↔ Guidance
  ↓
PX4 Bridge
  ↓
PX4 / FC
  ↓
QGroundControl / Vehicle
```

## 왜 이렇게 나누는가
- 연결 문제와 알고리즘 문제를 분리하기 위해
- 비전 실패와 PX4 통신 실패를 다른 계층에서 디버깅하기 위해
- 자체개발 점수 설명을 쉽게 하기 위해
- 팀원 6명이 병렬 작업하기 쉽게 하기 위해

## 절대 하지 말 것
- PX4 내부 제어기까지 동시에 건드리기
- 처음부터 YOLO 붙이기
- 비전, 구조, 전이를 한 번에 묶어서 테스트하기
- 실기체 연결 전에 상태머신 없이 코드만 늘리기
