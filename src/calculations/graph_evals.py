import numpy as np

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
        
  
    print(numberOfAzimuthEvaluated)
    rr = get_daa_rr(numberOfAzimuthEvaluated, numberOfAzimuthsPassed)
    points = (azimuth_array, rmin_array, colour_array)
    return (rr, points)
                

def get_daa_rr(num_az_eval, num_az_pass):
    return float((num_az_eval-num_az_pass)/num_az_eval)

