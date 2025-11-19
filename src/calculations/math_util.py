from decimal import Decimal
import math
import numpy as np


def cosd(x: float) -> float:
    return math.cos(math.radians(x))

def sind(x: float) -> float:
    return math.sin(math.radians(x))

def tand(x: float) -> float:
     return math.tan(math.radians(x))

def make_array(min: Decimal, max: Decimal, increment: Decimal) -> list[Decimal]:
    if (min > max):
            raise ValueError("Create Array: Start cannot be greater than end. Start: " + str(min) + "End: " + str(max))
    if (increment <= 0):
        raise ValueError("Create Array: Interval cannot be less than 0: " + str(increment))
    
    #Use this instead of range because range does not allow Decimal and we may want to generate an array with Decimal
    lst = list()
    i = min
    while i < max:
        lst.append(i)
        i += increment
    lst.append(max)
    return np.array(lst)

def createCustArray(inputStr: str):
        str_lst = inputStr.split(",")
        dec_lst = []
        for item in str_lst:
            item.strip()
            dec_lst.append(Decimal(item))
        return np.array(dec_lst)