import numpy as np
import multiprocessing as mp
import csv
from data_classes.CurrentData import CurrentData

def per_speed_graph_evals(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, fov, daa_range):
    FAIL_COLOUR = "red"
    PASS_COLOUR = "green"
    numberOfAzimuthEvaluated = 0
    numberOfAzimuthsPassed = 0
    azimuth_array = np.array([])
    rmin_array = np.array([])
    colour_array = np.array([])
    
    #Check Oncoming Points
    i = 0
    for i in range(len(azimuthDegOncoming)):
        if not np.isnan(RminOncoming[i]):
            azimuth_array = np.append(azimuth_array, np.deg2rad(azimuthDegOncoming[i]) % (2*np.pi))
            rmin_array = np.append(rmin_array, RminOncoming[i])
            
            if abs(azimuthDegOncoming[i]) <= fov/2 and RminOncoming[i] < daa_range:
                numberOfAzimuthsPassed += 1
                colour_array = np.append(colour_array, PASS_COLOUR)
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
                else:
                    colour_array = np.append(colour_array, FAIL_COLOUR)
            
                numberOfAzimuthEvaluated += 1
        
  

    rr = get_daa_rr(numberOfAzimuthEvaluated, numberOfAzimuthsPassed)
    points = (azimuth_array, rmin_array, colour_array)
    return (rr, points)
                

def get_daa_rr(num_az_eval, num_az_pass):
    if num_az_eval == 0:
        return 0.0
    return float((num_az_eval-num_az_pass)/num_az_eval)

class WorkerData:
    def __init__(self, intruder_speed, rpas_speed, azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, fov, daa_range):
        self.intruder_speed = intruder_speed
        self.rpas_speed = rpas_speed
        self.azimuthDegOncoming = azimuthDegOncoming
        self.RminOncoming = RminOncoming
        self.azimuthOvertake = azimuthOvertake
        self.RminOvertake = RminOvertake
        self.fov = fov
        self.daa_range = daa_range
    

def calc_worker(data: WorkerData):
    results = per_speed_graph_evals(data.azimuthDegOncoming, data.RminOncoming, data.azimuthOvertake, data.RminOvertake, data.fov, data.daa_range)
    return tuple([data.intruder_speed, data.rpas_speed] + list(results))

def calculate_rr_points_for_intruder_speed(intruder_speed):
    data = CurrentData()
    queued_data = []
    results = []
    
    daa_spec = data.specs
    r_min = data.r_min_m
    r_min_overtake = data.r_min_over
    azimuth_array = daa_spec.encounter_azimuth_array
    fov = daa_spec.daa_fov_deg
    daa_range = daa_spec.daa_declaration_range
    rpas_speeds = daa_spec.rpas_speed_array
    
    for rpas_speed in rpas_speeds:
        exists = False
        if intruder_speed in data.rr_val.keys():
            if rpas_speed in data.rr_val[intruder_speed].keys():
                exists = True
                continue
                
        if not exists:
            new_data = WorkerData(intruder_speed, rpas_speed, azimuth_array, r_min[intruder_speed][rpas_speed], azimuth_array, r_min_overtake[intruder_speed][rpas_speed], fov, daa_range)            
            queued_data.append(new_data)
            
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(calc_worker, queued_data)
        
    
    for result in results: 
        if result[0] not in data.rr_val.keys():
            data.rr_val[result[0]] = dict()
            
        if result[0] not in data.points.keys():
            data.points[result[0]] = dict()
        
        data.rr_val[result[0]][result[1]] = result[2]
        data.points[result[0]][result[1]] = result[3]

        
    
        
    
    
    
def calculate_rr_points_for_rpas_speed(rpas_speed):
    data = CurrentData()
    queued_data = []
    results = []
    
    daa_spec = data.specs
    r_min = data.r_min_m
    r_min_overtake = data.r_min_over
    azimuth_array = daa_spec.encounter_azimuth_array
    fov = daa_spec.daa_fov_deg
    daa_range = daa_spec.daa_declaration_range
    intruder_speeds = daa_spec.intruder_speed_array
    
    for intruder_speed in intruder_speeds:
        exists = False
        if intruder_speed in data.rr_val.keys():
            if rpas_speed in data.rr_val[intruder_speed].keys():
                exists = True
                continue
                
        if not exists:
            new_data = WorkerData(intruder_speed, rpas_speed, azimuth_array, r_min[intruder_speed][rpas_speed], azimuth_array, r_min_overtake[intruder_speed][rpas_speed], fov, daa_range)            
            queued_data.append(new_data)
            
    with mp.Pool(mp.cpu_count()) as p:
        results = p.map(calc_worker, queued_data)
        
    
    for result in results: 
        if result[0] not in data.rr_val.keys():
            data.rr_val[result[0]] = dict()
            
        if result[0] not in data.points.keys():
            data.points[result[0]] = dict()
        
        data.rr_val[result[0]][result[1]] = result[2]
        data.points[result[0]][result[1]] = result[3]

#For a given set of vals, get normalized probability distribution that any plane will have that params given a dataset of known params and count of planes flying with that param.
def get_normalized_distribution(params, dataset_params, dataset_counts):
    #If we want to increase the floor of our distribution by a percentage of the max value (to deal with 0 ranges), uncomment below:
    # dataset_counts = dataset_counts + (np.max(dataset_counts) * 0.01)
    result_dist = np.interp(params, dataset_params, dataset_counts)
    
    result_sum = np.sum(result_dist)
    
    return result_dist/result_sum

#For a set of speeds, gets the normal distribution based on the first set of speeds in a csv file with name filename
def get_normalized_distribution_speeds(filename, speeds):
    with open(filename, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        speed_row = None
        count_row = None

        for row in csv_reader:
            row_name:str = row[0]
            #Check this is 
            if row_name.lower().startswith("speed") and row_name.lower().endswith("min_bound (incl)") and speed_row is not None:
                speed_row = np.array(row[1:])
            if row_name.lower().startswith("speed") and row_name.lower().endswith("values") and count_row is not None:
                count_row = np.array(row[1:])
            
            if speed_row is not None and count_row is not None:
                break
        
        if speed_row is not None and count_row is not None:
            return get_normalized_distribution(speeds, speed_row, count_row)
        else:
            return None
        
def normalize_rr(rr, norm_dist):
    failHeights = rr*norm_dist
    passHeights = norm_dist - failHeights
    
    return (passHeights, failHeights
            )
    
        
        
    