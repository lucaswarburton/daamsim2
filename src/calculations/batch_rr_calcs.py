"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
from rr_calcs import rr_calcs
import os
import sys
from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData
import matlab.engine


def batch_calcs(specs: DaaSpec):
    eng = matlab.engine.start_matlab()
    intruder_speeds = specs.intruder_speed_array

    current_data = CurrentData()
    current_data.rtas_specs = specs
    current_data.azimuth_vect = [] * len(intruder_speeds)
    current_data.r_min_m = [] * len(intruder_speeds)
    current_data.r_min_over = [] * len(intruder_speeds)
    current_data.ground_int_speed = [] * len(intruder_speeds)
    current_data.alpha_oncoming_vect = [] * len(intruder_speeds)
    current_data.alpha_overtake_vect = [] * len(intruder_speeds)
    current_data.clos_vel = [] * len(intruder_speeds)
    current_data.clos_vel_over = [] * len(intruder_speeds)
    
    for i, speed in enumerate(intruder_speeds):
        print(f"Evaluating Intruder speed {speed} kts")
        rr_calcs(speed, i, eng)

    eng.quit()

