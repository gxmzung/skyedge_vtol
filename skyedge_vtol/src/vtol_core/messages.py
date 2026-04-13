from dataclasses import dataclass

@dataclass
class GuidanceSetpoint:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    yaw: float = 0.0

@dataclass
class VisionTarget:
    found: bool = False
    offset_x: float = 0.0
    offset_y: float = 0.0
    target_id: int = -1
