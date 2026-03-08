import numpy as np
import multiprocessing as mp
import csv
from data_classes.CurrentData import CurrentData

def evaluate_dataset_for_rr_and_graph_points(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, close_vel, close_vel_over, fov, daa_range, rpa_size, intruder_detection_threshold, manuever_delay):
    FAIL_COLOUR = "red"
    PASS_COLOUR = "green"
    numberOfAzimuthEvaluated = 0
    numberOfAzimuthsPassed = 0
    numOfSeeAndAvoidOnlyMitigated = 0
    azimuth_array = np.array([])
    rmin_array = np.array([])
    colour_array = np.array([])
    
    temp = calculateSeeAndAvoidForRpaSizeAndIntruderManeuverDelay(rpa_size, intruder_detection_threshold, manuever_delay)
    detection_range = temp[0]
    max_close_vel = temp[1]
    
    #Check Oncoming Points
    i = 0
    for i in range(len(azimuthDegOncoming)):
        if not np.isnan(RminOncoming[i]):
            azimuth_array = np.append(azimuth_array, np.deg2rad(azimuthDegOncoming[i]) % (2*np.pi))
            rmin_array = np.append(rmin_array, RminOncoming[i])
            
            if abs(azimuthDegOncoming[i]) <= fov/2 and RminOncoming[i] < daa_range:
                numberOfAzimuthsPassed += 1
                colour_array = np.append(colour_array, PASS_COLOUR)
            elif abs(close_vel[i]) < max_close_vel:
                numOfSeeAndAvoidOnlyMitigated += 1
                colour_array = np.append(colour_array, FAIL_COLOUR)
            else:
                colour_array = np.append(colour_array, FAIL_COLOUR)
            
            numberOfAzimuthEvaluated += 1
    
    #Check Overtake Points
    if not (azimuthOvertake.size == 0):    
        for i in range(len(azimuthOvertake)):
            if not np.isnan(RminOvertake[i]):
                azimuth_array = np.append(azimuth_array, np.deg2rad(azimuthDegOncoming[i]) % (2*np.pi))
                rmin_array = np.append(rmin_array, RminOvertake[i])
            
                if abs(azimuthOvertake[i]) <= fov/2 and RminOvertake[i] < daa_range:
                    numberOfAzimuthsPassed += 1
                    colour_array = np.append(colour_array, PASS_COLOUR)
                elif abs(close_vel_over[i]) < max_close_vel:
                    numOfSeeAndAvoidOnlyMitigated += 1
                    colour_array = np.append(colour_array, FAIL_COLOUR)
                else:
                    colour_array = np.append(colour_array, FAIL_COLOUR)
            
                numberOfAzimuthEvaluated += 1
        
  

    daarr = get_daa_rr(numberOfAzimuthEvaluated, numberOfAzimuthsPassed)
    dsaarr = get_dsaa_rr(numberOfAzimuthEvaluated, numberOfAzimuthsPassed, numOfSeeAndAvoidOnlyMitigated)
    points = (azimuth_array, rmin_array, colour_array)
    return (daarr, points, dsaarr)
                

def get_daa_rr(num_az_eval, num_az_pass):
    if num_az_eval == 0:
        return 0.0
    return float((num_az_eval-num_az_pass)/num_az_eval)

def get_dsaa_rr(num_az_eval, num_az_pass, num_mit):
    if num_az_eval == 0:
        return 0.0
    return float((num_az_eval-(num_az_pass+num_mit))/num_az_eval)

class WorkerData:
    def __init__(self, intruder_speed, rpas_speed, azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, fov, daa_range, close_vel, close_vel_over, rpa_size, intruder_detection_threshold, manuever_delay):
        self.intruder_speed = intruder_speed
        self.rpas_speed = rpas_speed
        self.azimuthDegOncoming = azimuthDegOncoming
        self.RminOncoming = RminOncoming
        self.azimuthOvertake = azimuthOvertake
        self.RminOvertake = RminOvertake
        self.fov = fov
        self.daa_range = daa_range
        self.close_vel = close_vel
        self.close_vel_over = close_vel_over
        self.rpa_size = rpa_size
        self.intruder_detection_threshold = intruder_detection_threshold
        self.manuever_delay = manuever_delay
        
    

def calc_worker(data: WorkerData):
    results = evaluate_dataset_for_rr_and_graph_points(data.azimuthDegOncoming, data.RminOncoming, data.azimuthOvertake, data.RminOvertake, data.close_vel, data.close_vel_over, data.fov, data.daa_range, data.rpa_size, data.intruder_detection_threshold, data.manuever_delay)
    return tuple([data.intruder_speed, data.rpas_speed] + list(results))

def calculate_rr_points_for_intruder_speed(intruder_speed):
    data = CurrentData()
    queued_data = []
    results = []
    
    daa_spec = data.specs
    r_min = data.r_min_m
    r_min_overtake = data.r_min_over
    close_vel = data.close_vel
    close_vel_over = data.close_vel_over
    azimuth_array = daa_spec.encounter_azimuth_array
    fov = daa_spec.daa_fov_deg
    daa_range = daa_spec.daa_declaration_range
    rpas_speeds = daa_spec.rpas_speed_array
    rpa_size = daa_spec.rpas_wingspan
    intruder_detection_threshold = daa_spec.intruder_detection_thresh_arc_min
    intruder_maneuver_delay = daa_spec.intruder_maneuver_delay
    
    
    for rpas_speed in rpas_speeds:
        exists = False
        if intruder_speed in data.rr_val.keys():
            if rpas_speed in data.rr_val[intruder_speed].keys():
                exists = True
                continue
                
        if not exists:
            new_data = WorkerData(
                intruder_speed = intruder_speed, \
                rpas_speed = rpas_speed, \
                azimuthDegOncoming = azimuth_array, \
                RminOncoming = r_min[intruder_speed][rpas_speed], \
                azimuthOvertake= azimuth_array, \
                RminOvertake = r_min_overtake[intruder_speed][rpas_speed], \
                close_vel = close_vel[intruder_speed][rpas_speed], \
                close_vel_over = close_vel_over[intruder_speed][rpas_speed],
                fov = fov,\
                daa_range = daa_range, \
                rpa_size = rpa_size, \
                intruder_detection_threshold = intruder_detection_threshold, \
                manuever_delay = intruder_maneuver_delay)            
            queued_data.append(new_data)
            
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(calc_worker, queued_data)
        
    
    for result in results: 
        if result[0] not in data.rr_val.keys():
            data.rr_val[result[0]] = dict()
            
        if result[0] not in data.points.keys():
            data.points[result[0]] = dict()
        
        if result[0] not in data.srr_val.keys():
            data.srr_val[result[0]] = dict()
                    
        data.rr_val[result[0]][result[1]] = result[2]
        data.points[result[0]][result[1]] = result[3]
        data.srr_val[result[0]][result[1]] = result[4]

        
    
def calculate_rr_points_for_rpas_speed(rpas_speed):
    data = CurrentData()
    queued_data = []
    results = []
    
    daa_spec = data.specs
    r_min = data.r_min_m
    r_min_overtake = data.r_min_over
    close_vel = data.close_vel
    close_vel_over = data.close_vel_over
    azimuth_array = daa_spec.encounter_azimuth_array
    fov = daa_spec.daa_fov_deg
    daa_range = daa_spec.daa_declaration_range
    intruder_speeds = daa_spec.intruder_speed_array
    rpa_size = daa_spec.rpas_wingspan
    intruder_detection_threshold = daa_spec.intruder_detection_thresh_arc_min
    intruder_maneuver_delay = daa_spec.intruder_maneuver_delay
    
    for intruder_speed in intruder_speeds:
        exists = False
        if intruder_speed in data.rr_val.keys():
            if rpas_speed in data.rr_val[intruder_speed].keys():
                exists = True
                continue
                
        if not exists:
            new_data = WorkerData(intruder_speed = intruder_speed, \
                rpas_speed = rpas_speed, \
                azimuthDegOncoming = azimuth_array, \
                RminOncoming = r_min[intruder_speed][rpas_speed], \
                azimuthOvertake= azimuth_array, \
                RminOvertake = r_min_overtake[intruder_speed][rpas_speed], \
                close_vel = close_vel[intruder_speed][rpas_speed], \
                close_vel_over = close_vel_over[intruder_speed][rpas_speed],
                fov = fov,\
                daa_range = daa_range, \
                rpa_size = rpa_size, \
                intruder_detection_threshold = intruder_detection_threshold, \
                manuever_delay = intruder_maneuver_delay)                    
            queued_data.append(new_data)
            
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(calc_worker, queued_data)
        
    
    for result in results: 
        if result[0] not in data.rr_val.keys():
            data.rr_val[result[0]] = dict()
            
        if result[0] not in data.points.keys():
            data.points[result[0]] = dict()
        
        if result[0] not in data.srr_val.keys():
            data.srr_val[result[0]] = dict()
                    
        data.rr_val[result[0]][result[1]] = result[2]
        data.points[result[0]][result[1]] = result[3]
        data.srr_val[result[0]][result[1]] = result[4]

#For a given set of vals, get normalized probability distribution that any plane will have that params given a dataset of known params and count of planes flying with that param.
def get_normalized_distribution(params, dataset_params, dataset_counts):
    #If we want to increase the floor of our distribution by a percentage of the max value (to deal with 0 ranges), uncomment below: (ASK Dr. Borchshova ABOUT THIS)
    # dataset_counts = dataset_counts + (np.max(dataset_counts) * 0.01)
    result_dist = np.interp(params, dataset_params, dataset_counts)
    
    #Take sum of array with max of 1 for edge case where sum is 0
    result_sum = max(np.sum(result_dist), 1)
    
    return result_dist/result_sum

#For a set of speeds, gets the normal distribution based on the first set of speeds in a csv file with name filename
def get_normalized_distribution_speeds(filename, speeds):
    with open(filename, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        speed_row = None
        count_row = None

        for row in csv_reader:
            row_name:str = row[0]
            #Check this is a row of interest
            if row_name.strip().lower().startswith("speed") and row_name.strip().lower().endswith("min_bound (incl)") and (speed_row is None):
                speed_row = np.array(row[1:])
                speed_row = speed_row.astype(float)
            if row_name.lower().startswith("speed") and row_name.lower().endswith("values") and (count_row is None):
                count_row = np.array(row[1:])
                count_row = count_row.astype(float)
            
            if speed_row is not None and count_row is not None:
                break
        
        if speed_row is not None and count_row is not None:
            return get_normalized_distribution(speeds, speed_row, count_row)
        else:
            return None
        
def normalize_rr(rr, norm_dist):
    fail_heights = rr*norm_dist
    pass_heights = norm_dist - fail_heights
    
    return (pass_heights, fail_heights)

def get_cumulative_rr(rr, norm_dist):
    norm_rr = normalize_rr(rr, norm_dist)
    
    passes = norm_rr[0]
    fails = norm_rr[1]
    
    cumulative_pass = np.cumsum(passes)
    cumulative_fail = np.cumsum(fails)
    
    return (cumulative_pass, cumulative_fail)

def normalize_saa(rr, srr, norm_dist):
    no_see_fail_heights = rr*norm_dist
    pass_heights = norm_dist - no_see_fail_heights
    
    fail_heights = srr*norm_dist
    saa_heights = norm_dist - fail_heights - pass_heights
    
    return (pass_heights, fail_heights, saa_heights)

def get_cumulative_saa(rr, srr, norm_dist):
    norm_saa = normalize_saa(rr, srr, norm_dist)
    
    passes = norm_saa[0]
    fails = norm_saa[1]
    passes_see = norm_saa[2]
    
    cumulative_pass = np.cumsum(passes)
    cumulative_fail = np.cumsum(fails)
    cumulative_passes_see = np.cumsum(passes_see)
    
    return (cumulative_pass, cumulative_fail, cumulative_passes_see)

def calculateSeeAndAvoidForRpaSizeAndIntruderManeuverDelay(rpa_size, intruder_detection_threshold, manuever_delay):
    #convert to radians
    detectionThreshRad = np.deg2rad(intruder_detection_threshold/60)
    detectionRange = rpa_size/2*(1/np.tan(detectionThreshRad/2))
    maxClosingVelocityForSeeAndAvoid = detectionRange/manuever_delay
    
    return (detectionRange, maxClosingVelocityForSeeAndAvoid)
    
    
    
    
        
        
    