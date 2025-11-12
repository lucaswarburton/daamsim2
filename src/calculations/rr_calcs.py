from decimal import Decimal

from calculations import math_util
from data_classes.current_data import CurrentData

def rr_calcs(intruder_speed: Decimal):
    current_data = CurrentData()

    # unpack specs
    FOV = CurrentData.specs.FOV # Deg
    range = CurrentData.specs.range # meters
    max_bank = CurrentData.specs.maxBank # degrees
    max_roll_rate = CurrentData.max_roll_rate # degrees/second

    # Own UAS with the following characteristics
    nz = 1/math_util.cosd(max_bank) # 1.5g turn considered reasonable for a UAS
    time_resol = CurrentData.time_resol # time resolution for approximation

    ground_speed_h_vect = CurrentData.specs.ownspeed * 0.514444 # Convert to m/s
    ground_int_speed = intruder_speed * 0.514444; # Convert to m/s
    sigma_al = CurrentData.specs.sigma_al
    sigma_cross = CurrentData.specs.sigma_cross                 
    DMOD = CurrentData.specs.DMOD # collision bubble              
    t_sim = CurrentData.specs.t_sim # simulation time
    post_col = CurrentData.specs.psot_col # post-collision time

    # wind 
    wind_speed = CurrentData.specs.wind_speed # m/s
    wind_dir = CurrentData.specs.wind_dir; # direction wind is coming from

    # Rounding alpha
    num_decimals = CurrentData.specs.Ndecimals
    f = 10 ** num_decimals 

    azimuth_vect = CurrentData.specs.azimuths
    
    sensor_rate = CurrentData.specs.sensor_rate # seconds, time per scan
    scans_track = CurrentData.specs.scans_track # scans needed to establish track after detection
    t_track = sensor_rate * scans_track # seconds, time needed to establish track after detection
    t_warn = CurrentData.specs.t_warn # seconds, time pilot needs to begin executing CA maneuver
    t_delta = t_track + t_warn # seconds, time from detection to maneuver starting


    
