from dataclasses import dataclass

@dataclass
class InitialConditions:
    x_h: float
    y_h: float
    vx_h: float
    vy_h: float
    x_i: float
    y_i: float
    vx_i: float
    vy_i: float