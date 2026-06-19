class PX4BridgeStub:
    """
    PX4 bridge scaffold.

    This module does not directly control a real aircraft.
    It defines the software boundary for future PX4 offboard integration.
    """

    def __init__(self):
        self.armed = False
        self.mode = "MANUAL"

    def arm(self):
        self.armed = True
        return "ARM_COMMAND_SENT"

    def disarm(self):
        self.armed = False
        return "DISARM_COMMAND_SENT"

    def set_offboard_mode(self):
        self.mode = "OFFBOARD"
        return "OFFBOARD_MODE_REQUESTED"

    def send_position_setpoint(self, x: float, y: float, z: float):
        return {
            "command": "POSITION_SETPOINT",
            "x": x,
            "y": y,
            "z": z,
        }