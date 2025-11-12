"""
Implements the functionality of the batchRrCalcs script.
"""


from decimal import Decimal
from calculations.rr_calcs import rr_calcs
import calculations.math_util as math_util
from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData
import matlab.engine


def batch_calcs(specs: DaaSpec):
    eng = matlab.engine.start_matlab()
    intruder_speeds = specs.intruder_speeds

    current_data = CurrentData()
    CurrentData().clear()
    current_data.specs = specs
    
    for i in range(len(intruder_speeds)):
        print(f"Evaluating Intruder speed {intruder_speeds[i]:d} kts")
        rr_calcs(intruder_speeds[i], eng)

    eng.quit()

