import scipy.io
import array
import numpy as np
import sys
import os
import math


print(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "src"))
    
from data_classes.CurrentData import CurrentData

#% acceptable range for pass between values
ACCEPTABLE_MARGIN = 0.01
rpas_speed = np.float64(60.0)

def test_framework_per_speed(matlabfilename, jsonfilename):
    matlab_data = load_matlab_file(matlabfilename)
    cur_data = loadjsonfile(jsonfilename)
    
    print("Comparing Alpha Oncoming:")
    results = compare_array_and_dict(matlab_data["AlphaOncoming"], cur_data.alpha_oncoming_vect, rpas_speed)
    print("    Total Comparisons: " + str(results[3]))
    print("    Total Passes: " + str(results[0]))
    print("    Total Fails: " + str(results[1]))
    print("    Total Missing: " + str(results[2]))
    print("    Pass Rate: " + str(results[0]/results[3] * 100) + "%")
    print("    Missing Rate: " + str(results[2]/results[3] * 100) + "%")
    
    print("Comparing Alpha Overtake:")
    results = compare_array_and_dict(matlab_data["AlphaOvertake"], cur_data.alpha_overtake_vect, rpas_speed)
    print("    Total Comparisons: " + str(results[3]))
    print("    Total Passes: " + str(results[0]))
    print("    Total Fails: " + str(results[1]))
    print("    Total Missing: " + str(results[2]))
    print("    Pass Rate: " + str(results[0]/results[3] * 100) + "%")
    print("    Missing Rate: " + str(results[2]/results[3] * 100) + "%")
    
    print("Comparing Rmin close:")
    results = compare_array_and_dict(matlab_data["R_min_close"], cur_data.r_min_m, rpas_speed)
    print("    Total Comparisons: " + str(results[3]))
    print("    Total Passes: " + str(results[0]))
    print("    Total Fails: " + str(results[1]))
    print("    Total Missing: " + str(results[2]))
    print("    Pass Rate: " + str(results[0]/results[3] * 100) + "%")
    print("    Missing Rate: " + str(results[2]/results[3] * 100) + "%")

    print("Comparing Rmin over:")
    results = compare_array_and_dict(matlab_data["R_min_over"], cur_data.r_min_over, rpas_speed)
    print("    Total Comparisons: " + str(results[3]))
    print("    Total Passes: " + str(results[0]))
    print("    Total Fails: " + str(results[1]))
    print("    Total Missing: " + str(results[2]))
    print("    Pass Rate: " + str(results[0]/results[3] * 100) + "%")
    print("    Missing Rate: " + str(results[2]/results[3] * 100) + "%")
    
    print("Comparing Close Velocity:")
    results = compare_array_and_dict(matlab_data["VcloseOncoming"], cur_data.clos_vel, rpas_speed)
    print("    Total Comparisons: " + str(results[3]))
    print("    Total Passes: " + str(results[0]))
    print("    Total Fails: " + str(results[1]))
    print("    Total Missing: " + str(results[2]))
    print("    Pass Rate: " + str(results[0]/results[3] * 100) + "%")
    print("    Missing Rate: " + str(results[2]/results[3] * 100) + "%")
    
    print("Comparing Close Velocity Overtake:")
    results = compare_array_and_dict(matlab_data["VcloseOvertake"], cur_data.clos_vel_over, rpas_speed)
    print("    Total Comparisons: " + str(results[3]))
    print("    Total Passes: " + str(results[0]))
    print("    Total Fails: " + str(results[1]))
    print("    Total Missing: " + str(results[2]))
    print("    Pass Rate: " + str(results[0]/results[3] * 100) + "%")
    print("    Missing Rate: " + str(results[2]/results[3] * 100) + "%")
    
    
def compare_array_and_dict(a: array.array, d: dict, rpas_speed_key):
    passes = 0
    fails = 0
    missing = 0
    total = 0
    
    arranged_keys = sorted(d.keys())
    i=0
    while i <  len(a):
        if i < len(arranged_keys):
            results = compare_array_float_npfloat(a[i], d[arranged_keys[i]][rpas_speed_key])
            passes += results[0]
            fails += results[1]
            missing += results[2]
            total += results[3]
        else: 
            print("Missing one or more arrays!")
            missing += len(a[i])
            fails += len(a[i])
            total += len(a[i])
        i += 1
            
    while i < len(arranged_keys):
        missing += len(d[arranged_keys[i]])
        fails += len(d[arranged_keys[i]])
        total += len(d[arranged_keys[i]])
        i += 1
        
    return [passes, fails, missing, total]

def compare_array_float_npfloat(af, anpf):
    passes = 0
    fails = 0
    missing = 0
    total = 0
    
    i = 0
    while i <  len(af):
        if i < len(anpf):    
            if math.isnan(af[i]) or math.isnan(anpf[i]):
                if math.isnan(af[i]) and math.isnan(anpf[i]):
                    passes += 1
                else:
                    fails += 1
            elif (anpf[i].item() <= (af[i] + abs(af[i]*ACCEPTABLE_MARGIN/100))) and (anpf[i].item() >= (af[i] - abs(af[i]*ACCEPTABLE_MARGIN/100))):
                passes += 1
            else:
                fails += 1
        else: 
            fails += 1
            missing += 1
        total += 1
        i += 1
    
    if i < len(anpf):
        fails += len(anpf) - i
        missing += len(anpf) - i
        total += len(anpf) - i
            
    return [passes, fails, missing, total]
    
    
    

def load_matlab_file(filename) -> dict: 
    dictionary = dict()
    scipy.io.loadmat(file_name=filename, mdict=dictionary)
    return dictionary

def loadjsonfile(filename):
    data:CurrentData = CurrentData()
    with open(filename) as f:
        json_string = f.read()
        data.from_json(json_string)
    return data
    
    
if __name__ == "__main__":

    test_framework_per_speed("tests/test.mat", "tests/test_compare_speed_only.json")
    