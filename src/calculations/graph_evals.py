import numpy as np
from multiprocessing import Process, Queue
from data_classes import CurrentData

def per_speed_graph_evals(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, fov, daa_range):
    FAIL_COLOUR = "red"
    PASS_COLOUR = "green"
    numberOfAzimuthEvaluated = 0
    numberOfAzimuthsPassed = 0
    azimuth_array = np.array([])
    rmin_array = np.array([])
    colour_array = np.array([])
    
    i = 0
    for i in range(len(azimuthDegOncoming)):
        if not np.isnan(RminOncoming[i]):
            azimuth_array = np.append(azimuth_array, azimuthDegOncoming[i]*np.pi/180)
            rmin_array = np.append(rmin_array, RminOncoming[i])
            
            if abs(azimuthDegOncoming[i]) <= fov/2 and RminOncoming[i] < daa_range:
                numberOfAzimuthsPassed += 1
                colour_array = np.append(colour_array, PASS_COLOUR)
            else:
                colour_array = np.append(colour_array, FAIL_COLOUR)
            
            numberOfAzimuthEvaluated += 1
            
    if not (azimuthOvertake.size == 0):    
        for i in range(len(azimuthOvertake)):
            if not np.isnan(RminOvertake[i]):
                azimuth_array = np.append(azimuth_array, azimuthOvertake[i]*np.pi/180)
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

def calc_worker(intruder_speed, rpas_speed, azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, fov, daa_range, q: Queue):
    q.cancel_join_thread()
    results = per_speed_graph_evals.convert_data(azimuthDegOncoming, RminOncoming, azimuthOvertake, RminOvertake, fov, daa_range)
    q.put([intruder_speed, rpas_speed] + results)

def calculate_for_intruder_speed(intruder_speed):
    data = CurrentData()
    processes = []
    q = Queue()
    
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
                continue
                
        if not exists:
            p = Process(taget = calc_worker, args=(intruder_speed, rpas_speed, azimuth_array, r_min[intruder_speed][rpas_speed], azimuth_array, r_min_overtake[intruder_speed][rpas_speed], fov, daa_range, q))
            processes.append(p)
            
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    while not q.empty():
        results = q.get()
        data.rr_val[results[0]][results[1]] = results[2]
        data.points[results[0]][results[1]] = results[3]
    
    
    
def calculate_for_rpas_speed(rpas_speed):
    data = CurrentData()
    processes = []
    q = Queue()
    
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
                continue
                
        if not exists:
            p = Process(taget = calc_worker, args=(intruder_speed, rpas_speed, azimuth_array, r_min[intruder_speed][rpas_speed], azimuth_array, r_min_overtake[intruder_speed][rpas_speed], fov, daa_range, q))
            processes.append(p)
            
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
        
    while not q.empty():
        results = q.get()
        data.rr_val[results[0]][results[1]] = results[2]
        data.points[results[0]][results[1]] = results[3]

