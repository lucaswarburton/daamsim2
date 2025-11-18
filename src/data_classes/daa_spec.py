from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DaaSpec:
    #Read RTAS Characteristics
    rtas_max_bank_deg: Decimal
    rtas_wingspan: Decimal
    rtas_max_roll_rate: Decimal
    rtas_speed_array: list

    #Intruder Characteristics
    intruder_speed_array: list

    #DAA Characteristics
    daa_declaration_range: Decimal
    daa_fov_deg: Decimal
    rate_of_revisit: int
    scans_track: int

    #Simulation Variables
    NDecimals: int
    time_resol: Decimal
    conflict_volume: Decimal
    t_sim: Decimal
    post_col: Decimal
    wind_speed: Decimal
    wind_dir: Decimal
    human_factor_delay: int
    encounter_azimuth_array: list

