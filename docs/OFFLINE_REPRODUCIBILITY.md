# VTOL Mission Systems — 오프라인 재현성 게이트

## 목적
이 저장소의 **의존성 없는 Python core**를 외부 개발자가 같은 순서로 재현하고 실패 단계가 어디인지 확인할 수 있게 합니다. ROS 2 패키지 빌드, 실제 PX4 SITL, 비행 또는 센서 시험의 증빙이 아닙니다.

## 실행
Python 3.11 이상 권장. 저장소 루트에서:

```sh
python scripts/verify_offline.py
```

다음 4단계를 수행하며 **첫 비정상 종료 코드에서 중단**합니다.

| 단계 | 실제 실행 내용 | 확인 대상 |
| --- | --- | --- |
| structure | `scripts/check_structure.py` | 필수 파일 존재 |
| core-tests | `unittest discover -s tests -v` | 상태·텔레메트리·Failsafe 회귀 |
| smoke | `scripts/smoke_test.py` | 최소 모의 임무 |
| demo | `src/vtol/mission_demo.py` | 종료 코드 0 **및** `FAILSAFE: LOW_BATTERY`, `FINAL STATE: FAILSAFE` 출력 확인 |

## 보고 시 최소 증빙
- 저장소 SHA: `git rev-parse HEAD`
- Python/OS 버전과 실행 명령 및 로그
- 각 단계 종료 코드, 실패가 있으면 원문 메시지
- `PX4BridgeStub` 반환 문자열을 실제 PX4 ACK로 해석하지 않았는지 확인
- 실장비·ROS 2/SITL 연결 여부를 별도 필드로 표기 (이 게이트에서는 **미검증**)

## 주의
이 스크립트는 기존 CI 명령을 하나의 진입점으로 묶었습니다. 코드 동작을 개선했다거나 SITL 테스트를 새로 수행했다는 주장이 아닙니다. 실제 SITL 증거 확보는 [V5 증빙 프로토콜](PX4_SITL_V5_EVIDENCE.md)에 따라 버전 SHA, DDS 샘플, 원시 로그, 드롭아웃/복구 기록을 따로 수집해야 합니다.

## 데모 결과 검증
검증 스크립트는 오프라인 데모가 단순히 종료 코드 0으로 끝나는 것에 만족하지 않습니다. 결과 출력에서 `FAILSAFE: LOW_BATTERY`와 `FINAL STATE: FAILSAFE`를 **완전한 줄 단위로** 확인하고, 하나라도 빠지면 실패로 처리합니다. `tests/test_offline_gate.py`는 잘못된 정상 종료·실패 사유·부분 문자열 오탐을 검증합니다. 이 기준은 현재 제공된 결정론적 모의 입력에만 적용합니다.
