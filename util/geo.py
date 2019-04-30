# Used to convert GPS from degrees to decimal
def deg_to_decimal(direction, degrees, minutes, seconds):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/3600

    if direction == 'S' or direction == 'W':
        dd *= -1

    return dd
