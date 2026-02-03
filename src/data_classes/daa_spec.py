from dataclasses import dataclass
import numpy as np

@dataclass
class DaaSpec:
    #Read rpas Characteristics
    rpas_max_bank_deg: float
    rpas_wingspan: float
    rpas_max_roll_rate: float

    rpas_speed_array: np.array

    #Intruder Characteristics
    intruder_speed_array: np.array

    #DAA Characteristics
    daa_declaration_range: float
    daa_fov_deg: float
    rate_of_revisit: int
    scans_track: int

    #Simulation Variables
    NDecimals: int
    time_resol: float
    conflict_volume: float
    t_sim: float
    post_col: float
    wind_speed: float
    wind_dir: float
    human_factor_delay: int
    encounter_azimuth_array: list

