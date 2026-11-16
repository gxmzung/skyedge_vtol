# VTOL 저장소 정리 판단 — 2026-11-16

## 목표
저장소 개수를 줄이되 독립된 검증 근거, 기여자·라이선스, 연구 목적을 훼손하지 않는다.

## 보존 대상
1. `vtol-mission-systems`: ROS 2 Humble 패키지, mock DDS 안전계약, 읽기 전용 PX4 텔레메트리 관찰, 상태·안전 연구. 실물 PX4 SITL 연결은 미검증.
2. `vtol-autonomy-lab`: 독립 MAVSDK 계층, 가상 FC, MissionRaw 업로드·검증, Offboard, Kalman 필터와 결함 검증. ROS 2 패키지의 단순 복제가 아니며 실물 비행은 미검증.
3. `px4-fault-aware-mission-verification`: C++/CMake 기반 명령 가드·고장 주입·가상 FC·결정적 시나리오 테스트. Python 구현과 재사용 후보지만 직접 중복 저장소라고 단정하면 안 된다.

## 작은 통합 후보
`twinflight-mission-v2` (시설점검 교육/발표용):

- 차별점: ROS 2 `px4_msgs` 기반 OffboardControlMode, TrajectorySetpoint, VehicleCommand 발행 노드, PX4 SITL/Gazebo 시연 구조.
- 본 PR에 이관한 것: 기존 `config/mission.yaml`의 시설점검 경로·웨이포인트 및 **읽기 전용** 계획 미리보기. 데이터의 출처를 주석에 표기.
- 본 PR에 **이관하지 않은 것**: `mission_node.py` 명령 송신, ROS 2 launch / package.xml, 기존 실행/의존성 계약, 커밋 이력.
- 기존 노드는 실제 위치 피드백으로 도달 여부를 판단하지 않고 시간으로 다음 웨이포인트에 진입하므로 안전 기준 미달; 실제 기체에서 실행하면 안 된다.
- **Archive 보류**: ROS 2 발표 시연을 재현해야 하는지, 과제 제출 링크와 팀 기여·저작권을 확인하기 전에는 원본을 활성 상태로 둔다.

## 이미 Archived
- `SkyEdge-VTOL-System`: 이력·시험 사진과 팀 자료를 보존한다. 현재 독립적인 배포 프로그램이 아니라는 점은 소스 트리 기준 판단이며, 팀 자료의 이관/삭제는 수행하지 않는다.
- `mission-edge-tech-lab`: 비VTOL 주제가 다수 포함된 통합 연구 기록. VTOL 작업과 일부 유사하다는 이유만으로 추가 삭제하지 않는다.

## 다음 후보군
- `mission-state-machine-cpp` ↔ `px4-fault-aware-mission-verification`: 작은 C++ 상태머신의 알고리즘과 고장처리 테스트 비교 후 재사용·Archive 검토.
- `twinflight-mission-v2`: 프로젝트 제출·시연 의존성이 없다면 ROS 2 launch/노드/의존성까지 안전하게 이관 후 Archive 후보.

## 최종 원칙
- 핵심 2개 저장소는 현재 별도 유지.
- 완전 이관 전 Archive 0개, 영구 삭제 0개.
- 테스트 통과는 PX4 SITL/실기체 비행 안전성의 증거가 아니다.
