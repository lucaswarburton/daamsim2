from dataclasses import dataclass
from decimal import Decimal

@dataclass
class daa_spec:
    #ROV Params
    max_bank: Decimal # degrees
    range: Decimal # meters
    FOV: Decimal # degrees
    ownsize: Decimal # meters
    ownspeed: Decimal # knots
    max_roll_rate: Decimal # degrees/second
    
    #Intruder Params
    azimuth_vector_array: list[Decimal]
    intruder_speed_array: list[Decimal]
    
    #Simulation Params
    sigma_al: Decimal
    signma_cross: Decimal
    DMOD: Decimal
    t_sim: Decimal
    post_col: Decimal
    wind_speed: Decimal
    wind_dir: Decimal
    NDecimals: int
    sensor_rate: int
    scans_track: int
    t_warn: int
    
    @staticmethod
    def createIntervalArray(start:Decimal, end: Decimal, interval: Decimal):
        lst = list(range(start, end, interval))
        return lst + start
    
    @staticmethod
    def createCustArray(inputStr: str):
        str_lst = inputStr.split(",")
        dec_lst = []
        for item in str_lst:
            item.strip()
            dec_lst.append(Decimal(item))
        return dec_lst
    
    