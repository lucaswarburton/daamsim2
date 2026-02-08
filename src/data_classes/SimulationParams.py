from dataclasses import dataclass

@dataclass
class SimulationParams:
    t_sim: float
    post_col: float
    time_resol: float
    ground_speed_h: float
    ground_int_speed: float
    sigma_al: float
    sigma_cross: float
    nz: float
    DMOD: float
    vx_w: float
    vy_w: float
    max_bank: float
    max_roll_rate: float
    azimuth_vect: list