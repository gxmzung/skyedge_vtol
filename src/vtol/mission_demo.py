from mission_manager.mission_state import MissionStateMachine
from telemetry.telemetry_health import TelemetryHealth
from safety.failsafe_manager import FailsafeManager


def main():
    mission = MissionStateMachine()
    failsafe = FailsafeManager()

    timeline = [
        TelemetryHealth(95, 88, 14, 42, 10),
        TelemetryHealth(82, 79, 13, 48, 40),
        TelemetryHealth(66, 70, 12, 55, 45),
        TelemetryHealth(44, 61, 10, 60, 38),
        TelemetryHealth(22, 55, 9, 66, 30),
    ]

    print("SkyEdge VTOL mission demo started")

    for health in timeline:
        print(f"STATE: {mission.state.value}")

        if failsafe.should_trigger(health):
            print(f"FAILSAFE: {failsafe.reason(health)}")
            mission.trigger_failsafe()
            break

        mission.next()

        if mission.is_finished():
            break

    print(f"FINAL STATE: {mission.state.value}")


if __name__ == "__main__":
    main()