from enum import Enum


class MissionState(Enum):
    IDLE = "IDLE"
    ARMING = "ARMING"
    TAKEOFF = "TAKEOFF"
    MISSION = "MISSION"
    RETURN_HOME = "RETURN_HOME"
    LANDING = "LANDING"
    COMPLETE = "COMPLETE"
    FAILSAFE = "FAILSAFE"


class MissionStateMachine:
    def __init__(self):
        self.state = MissionState.IDLE

    def next(self):
        flow = {
            MissionState.IDLE: MissionState.ARMING,
            MissionState.ARMING: MissionState.TAKEOFF,
            MissionState.TAKEOFF: MissionState.MISSION,
            MissionState.MISSION: MissionState.RETURN_HOME,
            MissionState.RETURN_HOME: MissionState.LANDING,
            MissionState.LANDING: MissionState.COMPLETE,
        }

        self.state = flow.get(self.state, self.state)
        return self.state

    def trigger_failsafe(self):
        self.state = MissionState.FAILSAFE
        return self.state

    def is_finished(self):
        return self.state in {MissionState.COMPLETE, MissionState.FAILSAFE}