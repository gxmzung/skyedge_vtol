# SkyEdge VTOL Mission Stack

PX4 + ROS 2 Humble 기반 VTOL 구조 임무용 소프트웨어 프로젝트입니다.

## 문서 구조
- `README.md` : 상위 레포 설명
- `docs/README.md` : 문서 인덱스
- `docs/01_PROJECT_OVERVIEW.md` : 프로젝트 개요
- `docs/02_BUILD_AND_RUN.md` : 설치 / 빌드 / 실행
- `docs/03_FEATURES_AND_NODES.md` : 기능 / 노드 설명
- `docs/04_PM_AND_TEAM.md` : PM 운영 / 팀 역할
- `docs/05_ROADMAP.md` : 9월까지 로드맵
- `management/PM_ORDERS.md` : PM 오더 상세
- `management/TEAM_ROLES.md` : 역할 분담
- `management/WEEK1_ACTION_PLAN.md` : 1주차 계획

## 핵심 원칙
- PX4는 검증된 FC 플랫폼으로 사용한다.
- 미션 상태머신, 비전, 가이던스, 실패 대응은 자체개발한다.
- 시뮬 성공만으로 완료 판정하지 않는다.
- 실기체 연결 전까지 소프트웨어 불확실성을 최대한 제거한다.

## 빠른 시작
```bash
cd ~/skyedge_vtol_final
bash scripts/install_ubuntu.sh
bash scripts/build_workspace.sh
```

PX4 SITL:
```bash
cd ~/PX4-Autopilot
make px4_sitl gz_standard_vtol
```

ROS 2 실행:
```bash
cd ~/skyedge_vtol_final
bash scripts/run_sim.sh
```
