from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DaaSpec:
    # ROV Params
    max_bank: Decimal # degrees
    range: Decimal # meters
    FOV: Decimal # degrees
    ownsize: Decimal # meters
    ownspeed: Decimal # knots
    max_roll_rate: Decimal # degrees/second

    # Intruder speed params
    intruder_speeds: list[Decimal] # knots

    # Azimuth speed params
    azimuths: list[Decimal] # degrees

    # Simulation Params
    time_resol: Decimal
    sigma_al: Decimal
    signma_cross: Decimal
    DMOD: Decimal
    t_sim: Decimal
    post_col: Decimal
    wind_speed: Decimal
    wind_dir: Decimal
    NDecimals: int
    sensor_rate: int
    scans_track: int
    t_warn: int
