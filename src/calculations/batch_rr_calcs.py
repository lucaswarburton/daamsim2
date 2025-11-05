"""
Implements the functionality of the batchRrCalcs script.
"""


from data_classes.daa_spec import DaaSpec
from data_classes.current_data import CurrentData


def make_speed_array(min_speed: int, max_speed: int, speed_increment: int) -> list[int]:
    intruderSpeedKts = list(range(min_speed, max_speed + speed_increment // 2, speed_increment))
    return intruderSpeedKts

def batch_calcs(specs: DaaSpec, min_speed: int, max_speed: int, speed_increment: int):
    del CurrentData()
    intruder_speeds = make_speed_array(min_speed, max_speed, speed_increment)

    for i in range(len(intruder_speeds)):
        print(f"Evaluating Intruder speed {intruder_speeds[i]:d} kts")
        # call calculation script

