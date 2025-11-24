"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
import time
from rr_calcs import rr_calcs
import os
import sys
from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData
import matlab.engine


def batch_calcs(specs: DaaSpec):
    eng = matlab.engine.start_matlab()
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    MEX_PATH = os.path.join(PROJECT_ROOT, "matlab-scripts")
    eng.addpath(MEX_PATH, nargout=0)

    intruder_speeds = specs.intruder_speed_array

    current_data = CurrentData()
    current_data.specs = specs
    current_data.azimuth_vect = [None] * len(intruder_speeds)
    current_data.r_min_m = [None] * len(intruder_speeds)
    current_data.r_min_over = [None] * len(intruder_speeds)
    current_data.ground_int_speed = [None] * len(intruder_speeds)
    current_data.alpha_oncoming_vect = [None] * len(intruder_speeds)
    current_data.alpha_overtake_vect = [None] * len(intruder_speeds)
    current_data.clos_vel = [None] * len(intruder_speeds)
    current_data.clos_vel_over = [None] * len(intruder_speeds)
    
    for i, speed in enumerate(intruder_speeds):
        print(f"Evaluating Intruder speed {speed} kts")
        rr_calcs(speed, i, eng)

    eng.quit()

