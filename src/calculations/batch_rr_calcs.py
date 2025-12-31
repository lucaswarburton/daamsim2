"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
from .rr_calcs import rr_calcs

from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData
from daamsim.UI.ProgressFrameUI import Progress_Frame
import matlab.engine
from time import perf_counter
from multiprocessing import Pool, Manager
from queue import Empty

def pool_worker(args):
        i, intruder_speed, specs, progress_queue = args
        result = rr_calcs(i, intruder_speed, specs)
        progress_queue.put(1)  # signal progress
        return result

def batch_calcs(specs: DaaSpec):
    intruder_speeds = specs.intruder_speed_array
    current_data = CurrentData()
    
    pframe = Progress_Frame.getinstance()
    pframe.reset()
    pframe.setMain(len(intruder_speeds), "Speeds Evaluated")
    
    manager = Manager()
    progress_queue = manager.Queue()
    results = []

    worker_args = [(i, speed, specs, progress_queue) for i, speed in enumerate(intruder_speeds)]

    with Pool() as p:
        for speed, data in p.imap_unordered(pool_worker, worker_args):
            results.append((speed, data))
            try:
                while True:
                    progress_queue.get_nowait()
                    pframe.increment_main()
            except Empty:
                pass

    # save results
    current_data.clear()
    current_data.specs = specs

    for intruder_speed, rtas_data in results:
        speed_key = round(intruder_speed, 3)
        current_data.azimuth_vect[speed_key] = {}
        current_data.r_min_m[speed_key] = {}
        current_data.r_min_over[speed_key] = {}
        current_data.ground_int_speed[speed_key] = {}
        current_data.alpha_oncoming_vect[speed_key] = {}
        current_data.alpha_overtake_vect[speed_key] = {}
        current_data.clos_vel[speed_key] = {}
        current_data.clos_vel_over[speed_key] = {}

        for rtas_speed, data in rtas_data.items():
            rtas_key = round(rtas_speed, 3)
            current_data.azimuth_vect[speed_key][rtas_key] = data["azimuth_vect"]
            current_data.r_min_m[speed_key][rtas_key] = data["r_min_m"]
            current_data.r_min_over[speed_key][rtas_key] = data["r_min_over"]
            current_data.ground_int_speed[speed_key][rtas_key] = data["ground_int_speed"]
            current_data.alpha_oncoming_vect[speed_key][rtas_key] = data["alpha_oncoming_vect"]
            current_data.alpha_overtake_vect[speed_key][rtas_key] = data["alpha_overtake_vect"]
            current_data.clos_vel[speed_key][rtas_key] = data["clos_vel"]
            current_data.clos_vel_over[speed_key][rtas_key] = data["clos_vel_over"]


    current_data._sim_state = 1