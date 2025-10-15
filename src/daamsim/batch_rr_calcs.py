def batch_rr_calcs(min_speed: int, max_speed: int, speed_increment: int):
    intruderSpeedKts = list(range(min_speed, max_speed + speed_increment / 2, speed_increment))
    return intruderSpeedKts
