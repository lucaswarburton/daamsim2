"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
from calculations.rr_calcs import rr_calcs
import calculations.math_util as math_util
from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData
import matlab.engine


def batch_calcs(specs: DaaSpec):
    eng = matlab.engine.start_matlab()
    intruder_speeds = specs.intruder_speeds

    current_data = CurrentData()
    CurrentData().clear()
    current_data.specs = specs
    current_data.azimuth_vect = [] * len(intruder_speeds)
    current_data.r_min_m = [] * len(intruder_speeds)
    current_data.r_min_over = [] * len(intruder_speeds)
    current_data.ground_int_speed = [] * len(intruder_speeds)
    current_data.alpha_oncoming_vect = [] * len(intruder_speeds)
    current_data.alpha_overtake_vect = [] * len(intruder_speeds)
    current_data.clos_vel = [] * len(intruder_speeds)
    current_data.clos_vel_over = [] * len(intruder_speeds)
    
    for i, speed in enumerate(intruder_speeds):
        print(f"Evaluating Intruder speed {speed:d} kts")
        rr_calcs(speed, i, eng)

    eng.quit()

