"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
from .rr_calcs import rr_calcs
import os
from data_classes.DaaSpec import DaaSpec
from data_classes.CurrentData import CurrentData
from daamsim.UI.ProgressFrameUI import ProgressFrame
import matlab.engine
from time import perf_counter


def batch_calcs(specs: DaaSpec):
    eng = matlab.engine.start_matlab()
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    MEX_PATH = os.path.join(PROJECT_ROOT, "matlab-scripts")
    eng.addpath(MEX_PATH, nargout=0)

    intruder_speeds = specs.intruder_speed_array
    current_data = CurrentData()
    
    pframe:ProgressFrame = ProgressFrame()
    pframe.reset()
    pframe.set_main(len(intruder_speeds), "Speeds Evaluated")

    # reset current_data for new calculation
    current_data.specs = specs
    current_data.azimuth_vect = dict()
    current_data.r_min_m = dict()
    current_data.r_min_over = dict()
    current_data.ground_int_speed = dict()
    current_data.alpha_oncoming_vect = dict()
    current_data.alpha_overtake_vect = dict()
    current_data.clos_vel = dict()
    current_data.clos_vel_over = dict()

    for i, speed in enumerate(intruder_speeds):
        print(f"Evaluating Intruder speed {speed} kts")
        rr_calcs(speed, i, eng)
        pframe.increment_main()

    current_data._sim_state = 1
    eng.quit()