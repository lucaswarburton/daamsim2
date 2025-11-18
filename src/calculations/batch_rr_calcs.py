"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
from calculations.rr_calcs import rr_calcs
import calculations.math_util as math_util
from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData


def batch_calcs(specs: DaaSpec):
    intruder_speeds = specs.intruder_speed_array

    current_data = CurrentData()
    CurrentData().clear()
    current_data.specs = specs
    
    for i in range(len(intruder_speeds)):
        print(f"Evaluating Intruder speed {intruder_speeds[i]:d} kts")
        rr_calcs(intruder_speeds[i])

