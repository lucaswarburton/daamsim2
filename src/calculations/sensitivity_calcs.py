from data_classes.DaaSpec import DaaSpec
from data_classes.CurrentData import CurrentData
from daamsim.UI.ProgressFrameUI import ProgressFrame
from calculations.graph_evals import per_speed_graph_evals

def sensitivity_calcs(specs: DaaSpec, range_increment, fov_increment, max_range):
    # max_bank = specs.rpas_max_bank_deg
    # fov = specs.daa_fov_deg
    # ownsize = specs.rpas_wingspan
    # ownspeed = specs.rpas_speed_array
    fovs = [i * fov_increment for i in range(1, 360 // fov_increment + 1)]
    ranges = [i * range_increment for i in range(1, max_range // range_increment + 1)]

    for fov in fovs:
        specs.daa_fov_deg = fov
        for range in ranges:
            specs.daa_declaration_range = range

