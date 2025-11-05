"""
Implements the functionality of the batchRrCalcs script.
"""


from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData


def make_speed_array(min_speed: int, max_speed: int, speed_increment: int) -> list[int]:
    if (min_speed > max_speed):
            raise ValueError("Create Interval Array: Start cannot be greater than end. Start: " + str(min_speed) + "End: " + str(max_speed))
    if (speed_increment <= 0):
        raise ValueError("Create Interval Array: Interval cannot be less than 0: " + str(speed_increment))
    
    intruderSpeedKts = list(range(min_speed, max_speed + speed_increment // 2, speed_increment))
    return intruderSpeedKts

def batch_calcs(specs: DaaSpec):
    intruder_speeds = make_speed_array(specs.min_speed, specs.max_speed, specs.speed_increment)
    CurrentData().clear()
    for i in range(len(intruder_speeds)):
        print(f"Evaluating Intruder speed {intruder_speeds[i]:d} kts")
        # call calculation script

