from decimal import Decimal
import math

from . import math_util
from data_classes.current_data import CurrentData
import numpy as np
import matlab.engine

def rr_calcs(intruder_speed: float, i: int, eng: object):

    current_data = CurrentData()
    specs = current_data.specs

    current_data.azimuth_vect[round(intruder_speed, 3)] = dict()
    current_data.r_min_m[round(intruder_speed, 3)] = dict()
    current_data.r_min_over[round(intruder_speed, 3)] = dict()
    current_data.ground_int_speed[round(intruder_speed, 3)] = dict()
    current_data.alpha_oncoming_vect[round(intruder_speed, 3)] = dict()
    current_data.alpha_overtake_vect[round(intruder_speed, 3)] = dict()
    current_data.clos_vel[round(intruder_speed, 3)] = dict()
    current_data.clos_vel_over[round(intruder_speed, 3)] = dict()


    # unpack specs
    # RPAS characteristics
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

    r_min_m = np.full(n, np.nan)
    r_min_m_over = np.full(n, np.nan)

    alpha_oncoming_vect = np.zeros(n)
    alpha_overtake_vect = np.zeros(n)
    
    # for ii=1:length(ground_speed_h_vect)
    # make ground_speed_h_vect an array, loop over it here
    for rpas_speed in specs.rpas_speed_array:
        ground_speed_h = rpas_speed * 0.514444
        
        tm = np.full(n, np.nan)
        clos_vel = np.full(n, np.nan)
        clos_vel_over = np.full(n, np.nan)
        delta_hdg_r = np.full(n, np.nan)
        delta_hdg_l = np.full(n, np.nan)
        azim_r = np.full(n, np.nan)
        azim_l = np.full(n, np.nan)

        def simulate_alpha(isOvertake: bool):
            if alpha not in [0, 180, -180]:
                # calculate the Beta angle
                beta = math_util.wrapTo180(180-alpha)
                
                psi_i = np.deg2rad((360 - alpha) % 360) # intruder heading in rads
                psi_h = 0 # ownship going north
                beta_rad = np.deg2rad(beta)

                # ownship initial conditions
                vx_h[0] = ground_speed_h * math.sin(psi_h)
                vy_h[0] = ground_speed_h * math.cos(psi_h)
                x_h[0] = 0
                y_h[0] = -ground_speed_h * t_sim

                bank_angle[0] = 0

                # intruder initial conditions
                vx_i[0] = ground_int_speed * math.sin(psi_i)
                vy_i[0] = ground_int_speed * math.cos(psi_i)
                x_i[0] = ground_int_speed * t_sim * math.sin(beta_rad)
                y_i[0] = ground_int_speed * t_sim * math.cos(beta_rad)

                turn_angles, _, t2, _, _, _ = eng.avoidSimplified(
                    float(x_h[0]), float(y_h[0]), float(vx_h[0]), float(vy_h[0]),
                    float(x_i[0]), float(y_i[0]), float(vx_i[0]), float(vy_i[0]),
                    float(sigma_al), float(sigma_cross), float(time_resol), float(nz),
                    float(DMOD), float(vx_w), float(vy_w), float(max_bank), float(max_roll_rate),
                    nargout=6
                ) 

                turn_angles = np.array(turn_angles).flatten()
                t2 = np.array(t2).flatten()

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
                
                tm[k] = Taumod - pref_man_time

                if isOvertake:
                    r_min_m_over[k] = tm[k] * math.sqrt(vvel)
                    clos_vel_over[k] = math.sqrt(vvel)
                else:
                    r_min_m[k] = tm[k] * math.sqrt(vvel)
                    clos_vel[k] = math.sqrt(vvel)

                if pref_man_turn >= 0:
                    delta_hdg_r[k] = pref_man_turn
                    azim_r[k] = azimuth_vect[k]
                else:
                    delta_hdg_l[k] = pref_man_turn
                    azim_l[k] = azimuth_vect[k]
                
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
                        track = math_util.wrapTo180(math.atan2(vx_h[time - 1], vy_h[time - 1]) * 180 / math.pi)

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
                                R = air_speed_h ( air_speed_h / (g * math.sqrt(nz * nz - 1.0)))
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
            else: # alpha is 0 or 180 or -180
                r_min_m[k] = np.nan
                tm[k] = np.nan
                delta_hdg_r[k] = np.nan
                azim_r[k] = np.nan
                delta_hdg_l[k] = np.nan
                azim_l[k] = np.nan
                clos_vel[k] = np.nan
        # end function

        for k in range(n):
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

            # calculate collision alpha
            alpha = round(eng.calculate_alpha(ground_speed_h, ground_int_speed, azimuth_vect[k]), num_decimals)
            alpha_oncoming_vect[k] = alpha
            simulate_alpha(False)
            

            # calculate collision alpha for overtake
            alpha = round(eng.calculate_alpha_ov(ground_speed_h, ground_int_speed, azimuth_vect[k]), num_decimals)
            alpha_overtake_vect[k] = alpha
            simulate_alpha(True)

        # save data
        current_data.azimuth_vect[round(intruder_speed, 3)][round(rpas_speed, 3)] = azimuth_vect
        current_data.r_min_m[round(intruder_speed, 3)][round(rpas_speed, 3)]  = r_min_m
        current_data.r_min_over[round(intruder_speed, 3)][round(rpas_speed, 3)]  = r_min_m_over
        current_data.ground_int_speed[round(intruder_speed, 3)][round(rpas_speed, 3)] = ground_int_speed
        current_data.alpha_oncoming_vect[round(intruder_speed, 3)][round(rpas_speed, 3)] = alpha_oncoming_vect
        current_data.alpha_overtake_vect[round(intruder_speed, 3)][round(rpas_speed, 3)] = alpha_overtake_vect
        current_data.clos_vel[round(intruder_speed, 3)][round(rpas_speed, 3)] = clos_vel
        current_data.clos_vel_over[round(intruder_speed, 3)][round(rpas_speed, 3)] = clos_vel_over

