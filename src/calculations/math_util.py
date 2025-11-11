from decimal import Decimal
import math


def cosd(x: Decimal) -> Decimal:
    return Decimal(math.cos(math.radians(x)))

def make_array(min: Decimal, max: Decimal, increment: Decimal) -> list[Decimal]:
    if (min > max):
            raise ValueError("Create Array: Start cannot be greater than end. Start: " + str(min) + "End: " + str(max))
    if (increment <= 0):
        raise ValueError("Create Array: Interval cannot be less than 0: " + str(increment))
    
    array = [
        min + i * increment
        for i in range(int((max - min) / increment) + 1)
    ]
    return array