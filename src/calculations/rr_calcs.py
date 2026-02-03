from decimal import Decimal
import math
import os
from data_classes.current_data import CurrentData
from data_classes.simulation_params import SimulationParams
from data_classes.initial_conditions import InitialConditions
from . import math_util
import numpy as np
import matlab.engine
from time import perf_counter

def rr_calcs(intruder_speed: float, i: int, eng: object):
    current_data = CurrentData()
    specs = current_data.specs

    # unpack specs
    # rpas characteristics
    max_bank = specs.rpas_max_bank_deg # deg
    max_roll_rate = specs.rpas_max_roll_rate # deg/s
    ground_speed_h_vect = specs.rpas_speed_array * 0.514444 # Convert to m/s

    # Intruder characteristics
    ground_int_speed = float(intruder_speed) * 0.514444 # Convert to m/s

    # DAA characteristics
    declaration_range = specs.daa_declaration_range # m
    daa_fov_deg = specs.daa_fov_deg # deg
    sensor_rate = specs.rate_of_revisit # s, time per scan
    scans_track = specs.scans_track # scans needed to establish track after detection
    
    # Simulation variables
    num_decimals = specs.NDecimals
    time_resol = specs.time_resol # time resolution for approximation
    DMOD = specs.conflict_volume # collision bubble radius
    t_sim = specs.t_sim # simulation time
    post_col = specs.post_col # post-collision time
    wind_speed = specs.wind_speed # m/s
    wind_dir = specs.wind_dir; # direction wind is coming from
    t_warn = specs.human_factor_delay # seconds, time pilot needs to begin executing CA maneuver
    azimuth_vect = specs.encounter_azimuth_array

    # Own UAS with the following characteristics
    nz = 1/math_util.cosd(max_bank) # 1.5g turn considered reasonable for a UAS

    sigma_al = 0
    sigma_cross = 0                

    vx_w = wind_speed * math_util.sind(wind_dir)
    vy_w = wind_speed * math_util.cosd(wind_dir)    
    
    t_track = sensor_rate * scans_track # seconds, time needed to establish track after detection
    t_delta = t_track + t_warn # seconds, time from detection to maneuver starting

    n = len(azimuth_vect)

    simulation_params = SimulationParams(t_sim, post_col, time_resol, 0, ground_int_speed, sigma_al, sigma_cross, nz, DMOD, vx_w, vy_w, max_bank, max_roll_rate, azimuth_vect)
    
    # initialize dicts for data
    int_key = float(round(intruder_speed, 3))
    current_data.azimuth_vect[int_key] = dict()
    current_data.r_min_m[int_key] = dict()
    current_data.r_min_over[int_key] = dict()
    current_data.ground_int_speed[int_key] = dict()
    current_data.alpha_oncoming_vect[int_key] = dict()
    current_data.alpha_overtake_vect[int_key] = dict()
    current_data.clos_vel[int_key] = dict()
    current_data.clos_vel_over[int_key] = dict()
    
    for rpas_speed in specs.rpas_speed_array:
        
        ground_speed_h = rpas_speed * 0.514444
        simulation_params.ground_speed_h = ground_speed_h

        alpha_oncoming_vect = np.zeros(n)
        alpha_overtake_vect = np.zeros(n)

        # calculate collision alphas
        alpha_oncoming_vect, alpha_overtake_vect = eng.calculate_alpha_batch(ground_speed_h, ground_int_speed, matlab.double(azimuth_vect.tolist()), nargout=2)
        alpha_oncoming_vect = np.asarray(alpha_oncoming_vect).flatten()
        alpha_overtake_vect = np.asarray(alpha_overtake_vect).flatten()
        alpha_oncoming_vect = np.round(alpha_oncoming_vect, num_decimals)
        alpha_overtake_vect = np.round(alpha_overtake_vect, num_decimals)

        #prepare initial conditions for all simulations
        initial_conditions = []
        initial_conditions_ov = []
        for k in range(n):
            initial_conditions.append(compute_initial_conditions(alpha_oncoming_vect[k], simulation_params))
            initial_conditions_ov.append(compute_initial_conditions(alpha_overtake_vect[k], simulation_params))
        x_h0  = [ic.x_h if ic != None else 0 for ic in initial_conditions]
        y_h0  = [ic.y_h if ic != None else 0 for ic in initial_conditions]
        vx_h0 = [ic.vx_h if ic != None else 0 for ic in initial_conditions]
        vy_h0 = [ic.vy_h if ic != None else 0 for ic in initial_conditions]
        x_i0  = [ic.x_i if ic != None else 0 for ic in initial_conditions]
        y_i0  = [ic.y_i if ic != None else 0 for ic in initial_conditions]
        vx_i0 = [ic.vx_i if ic != None else 0 for ic in initial_conditions]
        vy_i0 = [ic.vy_i if ic != None else 0 for ic in initial_conditions]

        x_h0_ov  = [ic.x_h if ic != None else 0 for ic in initial_conditions_ov]
        y_h0_ov  = [ic.y_h if ic != None else 0 for ic in initial_conditions_ov]
        vx_h0_ov = [ic.vx_h if ic != None else 0 for ic in initial_conditions_ov]
        vy_h0_ov = [ic.vy_h if ic != None else 0 for ic in initial_conditions_ov]
        x_i0_ov  = [ic.x_i if ic != None else 0 for ic in initial_conditions_ov]
        y_i0_ov  = [ic.y_i if ic != None else 0 for ic in initial_conditions_ov]
        vx_i0_ov = [ic.vx_i if ic != None else 0 for ic in initial_conditions_ov]
        vy_i0_ov = [ic.vy_i if ic != None else 0 for ic in initial_conditions_ov]

        # wrapper for batch matlab call
        turn_angles_arr, t2_arr, turn_angles_ov_arr, t2_ov_arr = avoid_simplified_batch(
            eng,
            x_h0, y_h0, vx_h0, vy_h0,
            x_i0, y_i0, vx_i0, vy_i0,
            x_h0_ov, y_h0_ov, vx_h0_ov, vy_h0_ov,
            x_i0_ov, y_i0_ov, vx_i0_ov, vy_i0_ov,
            simulation_params
        )
        
        #convert data into python format
        turn_angles_arr = np.array(turn_angles_arr)
        t2_arr = np.array(t2_arr)
        turn_angles_ov_arr = np.array(turn_angles_ov_arr)
        t2_ov_arr = np.array(t2_ov_arr)
        turn_angles_arr = turn_angles_arr.T
        t2_arr = t2_arr.T
        turn_angles_ov_arr = turn_angles_ov_arr.T
        t2_ov_arr = t2_ov_arr.T

        # initialize arrays for data
        r_min_m = np.full(n, np.nan)
        r_min_m_over = np.full(n, np.nan)
        tm = np.full(n, np.nan)
        tm_over = np.full(n, np.nan)
        clos_vel = np.full(n, np.nan)
        clos_vel_over = np.full(n, np.nan)
        delta_hdg_r = np.full(n, np.nan)
        delta_hdg_l = np.full(n, np.nan)
        delta_hdg_r_over = np.full(n, np.nan)
        delta_hdg_l_over = np.full(n, np.nan)
        azim_r = np.full(n, np.nan)
        azim_l = np.full(n, np.nan)
        azim_r_over = np.full(n, np.nan)
        azim_l_over = np.full(n, np.nan)
        

        for k in range(n):
            # simulate oncoming collision alpha
            r_min_m[k], clos_vel[k], delta_hdg_l[k], delta_hdg_r[k], azim_l[k], azim_r[k], tm[k] = simulate_alpha(alpha_oncoming_vect[k], False, eng, simulation_params, turn_angles_arr[k], t2_arr[k], initial_conditions[k], k, False)

            # simulate overtake collision alpha
            r_min_m_over[k], clos_vel_over[k], delta_hdg_l_over[k], delta_hdg_r_over[k], azim_l_over[k], azim_r_over[k], tm_over[k] = simulate_alpha(alpha_overtake_vect[k], True, eng, simulation_params, turn_angles_ov_arr[k], t2_ov_arr[k], initial_conditions_ov[k], k, False)
    
        # save data
        rpas_key = float(round(rpas_speed, 3))
        current_data.azimuth_vect[int_key][rpas_key] = azimuth_vect
        current_data.r_min_m[int_key][rpas_key]  = r_min_m
        current_data.r_min_over[int_key][rpas_key]  = r_min_m_over
        current_data.ground_int_speed[int_key][rpas_key] = ground_int_speed
        current_data.alpha_oncoming_vect[int_key][rpas_key] = alpha_oncoming_vect
        current_data.alpha_overtake_vect[int_key][rpas_key] = alpha_overtake_vect
        current_data.clos_vel[int_key][rpas_key] = clos_vel
        current_data.clos_vel_over[int_key][rpas_key] = clos_vel_over


def simulate_alpha(alpha: float, isOvertake: bool, eng: object, params: SimulationParams, turn_angles: np.array, t2: np.array, ic: InitialConditions, k: int, run_extra_simulations: bool):
    if alpha not in [0, 180, -180]:
        # calculate the Beta angle
        beta = math_util.wrapTo180(180-alpha)
        
        psi_i = np.deg2rad((360 - alpha) % 360) # intruder heading in rads
        psi_h = 0 # ownship going north
        beta_rad = np.deg2rad(beta)

        #unpack params
        t_sim = params.t_sim
        post_col = params.post_col
        time_resol = params.time_resol
        ground_int_speed = params.ground_int_speed
        nz = params.nz
        DMOD = params.DMOD
        vx_w = params.vx_w
        vy_w = params.vy_w
        max_bank = params.max_bank
        max_roll_rate = params.max_roll_rate
        azimuth_vect = params.azimuth_vect

        # create vel and pos arrays
        array_size = int((t_sim + post_col) / time_resol)
        x_h = np.zeros(array_size)      # host x position
        y_h = np.zeros(array_size)      # host y position
        vx_h = np.zeros(array_size)     # host x velocity
        vy_h = np.zeros(array_size)     # host y velocity
        x_i = np.zeros(array_size)      # intruder x position
        y_i = np.zeros(array_size)      # intruder y position
        vx_i = np.zeros(array_size)     # intruder x velocity
        vy_i = np.zeros(array_size)     # intruder y velocity
        bank_angle = np.zeros(array_size)  # bank angle

        x_h[0]  = ic.x_h
        y_h[0]  = ic.y_h
        vx_h[0] = ic.vx_h
        vy_h[0] = ic.vy_h
        x_i[0]  = ic.x_i
        y_i[0]  = ic.y_i
        vx_i[0] = ic.vx_i
        vy_i[0] = ic.vy_i
        bank_angle[0] = 0

        pref_man_time = t2[0]
        pref_man_turn = turn_angles[0]

        # the next block is needed to establish minimim range requirements
        host_vel = np.array([vx_h[0], vy_h[0]]) # vector, ownship velocity
        intr_vel = np.array([vx_i[0], vy_i[0]]) # vector, intruder velocity
        vel_rel = host_vel - intr_vel # vector, relative velocity
        host_pos = np.array([x_h[0], y_h[0]]) # vector, ownship position
        intr_pos = np.array([x_i[0], y_i[0]]) # vector, intruder position
        pos_rel = host_pos - intr_pos # relative position

        vvel = np.dot(vel_rel, vel_rel) # magnitude of relative velocity squared

        posvel = np.dot(pos_rel, vel_rel) # positive if ships are growing further

        Tcpa = 0
        if vvel > 0: # if relative velocity is not 0
            Tcpa = -posvel/vvel

        Taumod = -1
        if posvel < 0: # aircraft are converging
            Taumod = (DMOD ** 2 - np.dot(pos_rel, pos_rel)) / np.dot(pos_rel, vel_rel)
        
        if Taumod < 0:
            Taumod = -1
        
        tm = Taumod - pref_man_time

        if isOvertake:
            r_min_m_over = tm * math.sqrt(vvel)
            clos_vel_over = math.sqrt(vvel)
        else:
            r_min_m = tm * math.sqrt(vvel)
            clos_vel = math.sqrt(vvel)

        if pref_man_turn >= 0:
            delta_hdg_r = pref_man_turn
            azim_r = azimuth_vect[k]
            delta_hdg_l = np.nan
            azim_l = np.nan
        else:
            delta_hdg_l = pref_man_turn
            azim_l = azimuth_vect[k]
            delta_hdg_r = np.nan
            azim_r = np.nan
        
        if run_extra_simulations:
            for time in range(1, int((t_sim + post_col) / time_resol)): # start from 1 here because we have value at 0 initialized
                if time < pref_man_time / time_resol: # if maneuver hasn't started yet
                    # update position
                    x_h[time] = x_h[time - 1] + vx_h[time - 1] * time_resol
                    y_h[time] = y_h[time - 1] + vy_h[time - 1] * time_resol

                    # constant speed
                    vx_h[time] = vx_h[time - 1]
                    vy_h[time] = vy_h[time - 1]

                    # update intruder position
                    y_i[time] = y_i[time - 1] + ground_int_speed * math.cos(psi_i) * time_resol
                    x_i[time] = x_i[time - 1] + ground_int_speed * math.sin(psi_i) * time_resol

                    # not turning
                    bank_angle[time] = 0
                else: # maneuver has started
                    track = math_util.wrapTo180(math.degrees(math.atan2(vx_h[time - 1], vy_h[time - 1])))

                    if (abs(track) < abs(math_util.wrapTo180(pref_man_turn + psi_h))): # if maneuver hasn't finished yet
                        g = 9.80665

                        x_airspeed_h = vx_h[time - 1] + vx_w
                        y_airspeed_h = vy_h[time - 1] + vy_w
                        air_speed_h = math.sqrt(x_airspeed_h * x_airspeed_h + y_airspeed_h * y_airspeed_h)
                        R = None

                        if max_roll_rate is not None:
                            bank_angle[time] = min(bank_angle[time - 1] + max_roll_rate * time_resol, max_bank)
                            R = air_speed_h * air_speed_h / (g * math_util.tand(bank_angle[time]))
                        else:
                            R = air_speed_h * air_speed_h / (g * math.sqrt(nz * nz - 1.0))
                        omega = - math.copysign(1, pref_man_turn) * air_speed_h / R

                        # update ownship with turning
                        x_h[time] = x_h[time - 1] + time_resol * vx_h[time - 1] - omega * time_resol * time_resol / 2 * vy_h[time - 1]
                        y_h[time] = y_h[time - 1] + time_resol * vy_h[time - 1] + omega * time_resol * time_resol / 2 * vx_h[time - 1]
                        vx_h[time] = vx_h[time - 1] * (1 - omega * time_resol * omega * time_resol / 2) - omega * time_resol * vy_h[time - 1]
                        vy_h[time] = vy_h[time - 1] * (1 - omega * time_resol * omega * time_resol / 2) + omega * time_resol * vx_h[time - 1]
                        
                        # update intruder
                        y_i[time] = y_i[time - 1] + ground_int_speed * math.cos(psi_i) * time_resol
                        x_i[time] = x_i[time - 1] + ground_int_speed * math.sin(psi_i) * time_resol
                    else: # maneuver has finished
                        # update position
                        x_h[time] = x_h[time - 1] + vx_h[time - 1] * time_resol
                        y_h[time] = y_h[time - 1] + vy_h[time - 1] * time_resol

                        # constant speed
                        vx_h[time] = vx_h[time - 1]
                        vy_h[time] = vy_h[time - 1]

                        # update intruder position
                        y_i[time] = y_i[time - 1] + ground_int_speed * math.cos(psi_i) * time_resol
                        x_i[time] = x_i[time - 1] + ground_int_speed * math.sin(psi_i) * time_resol
        if isOvertake:
            return r_min_m_over, clos_vel_over, delta_hdg_l, delta_hdg_r, azim_l, azim_r, tm
        else:
            return r_min_m, clos_vel, delta_hdg_l, delta_hdg_r, azim_l, azim_r, tm
    else: # alpha is 0 or 180 or -180
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
# end function

def compute_initial_conditions(alpha, params):
    if alpha not in [0, 180, -180]:
        beta = math_util.wrapTo180(180 - alpha)

        psi_i = np.deg2rad((360 - alpha) % 360)
        psi_h = 0.0
        beta_rad = np.deg2rad(beta)

        t_sim = params.t_sim
        gsh = params.ground_speed_h
        gis = params.ground_int_speed

        return InitialConditions(
            x_h = 0.0,
            y_h = -gsh * t_sim,
            vx_h = gsh * math.sin(psi_h),
            vy_h = gsh * math.cos(psi_h),
            x_i = gis * t_sim * math.sin(beta_rad),
            y_i = gis * t_sim * math.cos(beta_rad),
            vx_i = gis * math.sin(psi_i),
            vy_i = gis * math.cos(psi_i),
        )
    return None


def avoid_simplified_batch(
    eng,
    x_h0, y_h0, vx_h0, vy_h0,
    x_i0, y_i0, vx_i0, vy_i0,
    x_h0_ov, y_h0_ov, vx_h0_ov, vy_h0_ov,
    x_i0_ov, y_i0_ov, vx_i0_ov, vy_i0_ov,
    simulation_params
):
    def prepare_array(arr):
        arr = np.array(arr).flatten()
        return matlab.double(arr.reshape(-1, 1).tolist())

    return eng.avoid_simplified_batch(
            prepare_array(x_h0), prepare_array(y_h0), prepare_array(vx_h0), prepare_array(vy_h0),
            prepare_array(x_i0), prepare_array(y_i0), prepare_array(vx_i0), prepare_array(vy_i0),
            prepare_array(x_h0_ov), prepare_array(y_h0_ov), prepare_array(vx_h0_ov), prepare_array(vy_h0_ov),
            prepare_array(x_i0_ov), prepare_array(y_i0_ov), prepare_array(vx_i0_ov), prepare_array(vy_i0_ov),
            float(simulation_params.sigma_al), float(simulation_params.sigma_cross),
            float(simulation_params.time_resol), float(simulation_params.nz),
            float(simulation_params.DMOD), float(simulation_params.vx_w),
            float(simulation_params.vy_w), float(simulation_params.max_bank),
            float(simulation_params.max_roll_rate), nargout=4
        )


