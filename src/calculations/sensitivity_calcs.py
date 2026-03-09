from data_classes.DaaSpec import DaaSpec
from data_classes.CurrentData import CurrentData
from daamsim.UI.ProgressFrameUI import ProgressFrame
from  calculations import graph_evals
import numpy as np
from scipy.interpolate import interp1d

def sensitivity_calcs(specs: DaaSpec, range_increment, fov_increment, max_range):
    # max_bank = specs.rpas_max_bank_deg
    # fov = specs.daa_fov_deg
    # ownsize = specs.rpas_wingspan
    # ownspeed = specs.rpas_speed_array
    current_data = CurrentData()
    fovs = [i * fov_increment for i in range(1, 360 // fov_increment + 1)]
    ranges = [i * range_increment for i in range(1, max_range // range_increment + 1)]
    rr = []

    for fov in fovs:
        fov_rrs = []
        specs.daa_fov_deg = fov
        for range in ranges:
            specs.daa_declaration_range = range
            daa_rr, dsaa_rr = [] * len(specs.intruder_speed_array), [] * len(specs.intruder_speed_array)
            for i in range(len(specs.intruder_speed_array)):
                daa_rr[i], dsaa_rr[i] = daa_rr_w_see_and_avoid(
                    current_data.alpha_oncoming_vect,
                    current_data.r_min_m,
                    current_data.alpha_overtake_vect,
                    current_data.r_min_over,
                    current_data.clos_vel,
                    current_data.clos_vel_over,
                    fov,
                    specs.daa_declaration_range,
                )
            fov_rrs.append(calc_total_rr(daa_rr, dsaa_rr, specs))
        rr.append(fov_rrs)
    
    current_data.sensitivity_rr = rr
            


def daa_rr_w_see_and_avoid(azimuth_deg_oncoming, r_min_oncoming, azimuth_overtake, r_min_overtake, clos_vel_oncoming, clos_vel_overtake, fov, daa_range):
    intruder_maneuver_delay = 12.5
    max_closing_vel = daa_range / intruder_maneuver_delay

    number_of_azimuths_evaluated = 0
    number_of_azimuths_passed = 0

    index_of_oncoming_azimuths_passed = []
    see_and_avoid_oncoming_index = []

    for i in range(len(azimuth_deg_oncoming)):
        if not np.isnan(r_min_oncoming[i]):
            azimuth_array = np.append(azimuth_array, np.deg2rad(azimuth_deg_oncoming[i]) % (2*np.pi))
            rmin_array = np.append(rmin_array, r_min_oncoming[i])
            
            if abs(azimuth_deg_oncoming[i]) <= fov/2 and r_min_oncoming[i] < daa_range:
                number_of_azimuths_passed += 1
                index_of_oncoming_azimuths_passed.append(i)

            if abs(clos_vel_oncoming[i]) < max_closing_vel:
                see_and_avoid_oncoming_index.append(i)
            
            number_of_azimuths_evaluated += 1

    index_of_overtake_azimuths_passed = []
    see_and_avoid_overtake_index = []

    if len(azimuth_overtake) > 0:
        for i in range(len(azimuth_overtake)):
            if not np.isnan(r_min_overtake[i]):
                if abs(azimuth_overtake[i]) <= fov / 2 and r_min_overtake[i] < daa_range:
                    number_of_azimuths_passed += 1
                    index_of_overtake_azimuths_passed.append(i)
                if abs(clos_vel_overtake[i]) < max_closing_vel:
                    see_and_avoid_overtake_index.append(i)
                number_of_azimuths_evaluated += 1

    total_passed_oncoming = list(
        set(index_of_oncoming_azimuths_passed) |
        set(see_and_avoid_oncoming_index)
    )

    total_passed_overtake = list(
        set(index_of_overtake_azimuths_passed) |
        set(see_and_avoid_overtake_index)
    )

    total_passed_detect_and_see_and_avoid = (
        len(total_passed_oncoming) +
        len(total_passed_overtake)
    )

    if number_of_azimuths_evaluated > 0:
        daa_rr = ((number_of_azimuths_evaluated - number_of_azimuths_passed) / number_of_azimuths_evaluated)
        dsaa_rr = ((number_of_azimuths_evaluated - total_passed_detect_and_see_and_avoid) / number_of_azimuths_evaluated)
    else:
        daa_rr = 0
        dsaa_rr = 0

    return daa_rr, dsaa_rr

def calc_total_rr(daa_rr, dsaa_rr, specs):
    speed_bins = np.array(specs.intruder_speed_array)
    distribution = graph_evals.get_normalized_distribution_speeds(specs.dist_file, specs.intruder_speed_array)
    interp = interp1d(speed_bins, distribution, kind="nearest", fill_value="extrapolate")

    pass_height = [0] * len(speed_bins)
    fail_height = [0] * len(speed_bins)
    saa_height = [0] * len(speed_bins)

    for i in range(len(speed_bins)):
        bin_dist = float(interp(speed_bins[i]))

        fail_height_no_see = bin_dist * daa_rr[i]
        pass_height_no_see = bin_dist - fail_height_no_see

        fail_height[i] = bin_dist * dsaa_rr[i]
        saa_height[i] = bin_dist - fail_height[i] - pass_height_no_see
        pass_height[i] = bin_dist - fail_height_no_see

    return np.sum(fail_height)
