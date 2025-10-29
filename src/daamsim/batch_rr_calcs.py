"""
Implements the functionality of the batchRrCalcs script.
"""


from daamsim.structs import daa_spec


def make_speed_array(min_speed: int, max_speed: int, speed_increment: int) -> list[int]:
    intruderSpeedKts = list(range(min_speed, max_speed + speed_increment // 2, speed_increment))
    return intruderSpeedKts

def batch_calcs(specs: daa_spec, min_speed: int, max_speed: int, speed_increment: int):
    intruder_speeds = make_speed_array(min_speed, max_speed, speed_increment)

    for i in range(len(intruder_speeds)):
        print(f"Evaluating Intruder speed {intruder_speeds[i]:d} kts")
        # call calculation script

