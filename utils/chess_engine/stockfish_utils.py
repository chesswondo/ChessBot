import math

def find_nearest_power_of_two(number: int) -> int:
    '''
    Finds the nearest number that is a power of two
    and less than specified.

    : param number: (int) - current number.

    : return: (int) - the neares power of two.
    '''
    power = math.log(number, 2)
    return 2**(int(power))