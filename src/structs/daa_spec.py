from dataclasses import dataclass

@dataclass
class daa_spec:
    max_bank: float # degrees
    range: float # meters
    FOV: float # degrees
    ownsize: float # meters
    ownspeed: float # knots
    max_roll_rate: float # degrees/second