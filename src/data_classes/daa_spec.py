from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DaaSpec:
    max_bank: Decimal # degrees
    range: Decimal # meters
    FOV: Decimal # degrees
    ownsize: Decimal # meters
    ownspeed: Decimal # knots
    max_roll_rate: Decimal # degrees/second
    min_speed: Decimal # knots
    max_speed: Decimal # knots
    speed_increment: Decimal # knots