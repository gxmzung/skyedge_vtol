# Team Roles (6명 기준)

## 전체 구조
- PM / System Lead: 1명
- PX4 / Bridge Lead: 1명
- Vision Lead: 1명
- Guidance / Control Lead: 1명
- Integration / Test Lead: 1명
- Docs / Ops / QA Lead: 1명

---

## 1. PM / System Lead
담당:
- 전체 아키텍처 결정
- 상태머신 승인
- 주간 목표 고정
- 브랜치/머지 기준 확정
- 발표/심사 대응 메시지 관리

산출물:
- 상태 전이표
- 주간 계획
- 리스크 목록
- 의사결정 로그

---

## 2. PX4 / Bridge Lead
담당:
- PX4 SITL 연결
- ROS2 ↔ PX4 bridge 구현
- arm / offboard / land command 안정화
- 실기체 연결 전담

산출물:
- `px4_bridge_node.py`
- PX4 연결 체크 문서
- 토픽 맵

---

## 3. Vision Lead
담당:
- line tracker
- aruco detector
- 카메라 입력 처리
- 검출 결과 publish

산출물:
- `line_tracker_node.py`
- `aruco_detector_node.py`
- vision test 영상 / 결과 로그

---

## 4. Guidance / Control Lead
담당:
- line offset → setpoint 변환
- marker offset → align setpoint
- return-home guidance
- hover / search pattern logic

산출물:
- `guidance_node.py`
- guidance 파라미터 문서

---

## 5. Integration / Test Lead
담당:
- launch 통합
- 시뮬 반복 테스트
- failure case 재현
- 시뮬/실기체 차이 기록

산출물:
- 테스트 시나리오
- 실패 재현 문서
- 통합 로그

---

## 6. Docs / Ops / QA Lead
담당:
- Ubuntu 설치 문서
- 빌드/실행 문서
- 체크리스트 정리
- 발표 자료 초안
- 심사 대응 Q&A 정리

산출물:
- README
- setup 문서
- 발표 초안
- 질답 문서

---

## 네 역할 추천
네가 PM처럼 움직이려면:
- PM / System Lead를 직접 맡고
- 동시에 Mission Manager와 Bridge의 설계권을 가져가라
- 코드 핵심은 남에게 넘기지 말고 승인 구조를 만들 것
