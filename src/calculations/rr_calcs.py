from decimal import Decimal
import math

from calculations import math_util
from data_classes.current_data import CurrentData
import numpy as np
import matlab.engine

def rr_calcs(intruder_speed: Decimal, eng: object):
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

    azimuth_vect = CurrentData.specs.azimuths
    
    sensor_rate = CurrentData.specs.sensor_rate # seconds, time per scan
    scans_track = CurrentData.specs.scans_track # scans needed to establish track after detection
    t_track = sensor_rate * scans_track # seconds, time needed to establish track after detection
    t_warn = CurrentData.specs.t_warn # seconds, time pilot needs to begin executing CA maneuver
    t_delta = t_track + t_warn # seconds, time from detection to maneuver starting

    vx_w = wind_speed * math_util.sind(wind_dir) # m/s, x component of wind speed
    vy_w = wind_speed * math_util.cosd(wind_dir) # m/s, y component of wind speed

    n = len(azimuth_vect)

    r_min_m = np.full(n, np.nan)
    r_min_m_over = np.full(n, np.nan)

    alpha_oncoming_vect = np.zeros(n)
    alpha_overtake_vect = np.zeros(n)
    
    # for ii=1:length(ground_speed_h_vect)
    # daamsim has loop here but round_speed_h_vect is a scalar. Opportunity to make it a list, multiple calculations?
    ground_speed_h = ground_speed_h_vect

    for k in range(n):
        array_size = (t_sim + post_col) / time_resol

        y_h = np.zeros(array_size)
        y_i = np.zeros(array_size)
        x_h = np.zeros(array_size)
        x_i = np.zeros(array_size)

        vy_h = np.zeros(array_size)
        vy_i = np.zeros(array_size)
        vx_h = np.zeros(array_size)
        vx_i = np.zeros(array_size)

        bank_angle = np.zeros(1, array_size)

        # calculate collision alpha
        alpha = round(eng.calculate_alpha(ground_speed_h, ground_int_speed, azimuth_vect[k]), num_decimals)
        alpha_oncoming_vect[k] = alpha

        tolerance = 0.5 / (10 ** num_decimals)
        if abs(alpha) > tolerance and abs(alpha - 180) > tolerance and abs(alpha + 180) > tolerance:
            # calculate the Beta angle
            beta = 180-alpha
            if beta > 180:
               beta = beta - 360
            elif beta < -180:
               beta = beta + 360
               
            psi_i = ((360 - alpha) * math.pi / 180) % (2 * math.pi) # intruder heading in rads
            psi_h = 0 # ownship going north
            beta_rad = beta * math.pi / 180

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

            turn_angles, cutoff, t2, t2_miss_dist, azimuth, infov = eng.avoidSimplified(
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

            # the next block is needed to establish minimim range
            # requirements
            host_vel = np.array([vx_h[0], vy_h[0]]) # vector, ownship velocity
            intr_vel = np.array([vx_i[0], vy_i[0]]) # vector, intruder velocity
            vel_rel = host_vel - intr_vel # vector, relative velocity
            host_pos = np.array([x_h[0], y_h[0]]) # vector, ownship position
            intr_pos = np.array([x_i[0], y_i[0]]) # vector, intruder position
            pos_rel = host_pos - intr_pos # relative position

            vvel = np.dot(vel_rel, vel_rel) # magnitude of relative velocity squared

            posvel = np.dot(pos_rel, vel_rel) # positive if ships are growing further

            Tcpa = 0
            if vvel > 0: # what is the purpose of this? it should always be positive (x dot x = |x|^2)
                Tcpa = -posvel/vvel
