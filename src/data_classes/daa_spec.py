from dataclasses import dataclass
import numpy as np

@dataclass
class DaaSpec:
    #Read RTAS Characteristics
    rtas_max_bank_deg: float
    rtas_wingspan: float
    rtas_max_roll_rate: float

    rtas_speed_array: np.array

    #Intruder Characteristics
    intruder_speed_array: np.array

    #DAA Characteristics
    daa_declaration_range: float
    daa_fov_deg: float
    rate_of_revisit: float
    scans_track: int

    #Simulation Variables
    NDecimals: int
    time_resol: float
    conflict_volume: float
    t_sim: float
    post_col: float
    wind_speed: float
    wind_dir: float
    human_factor_delay: float
    encounter_azimuth_array: np.array

