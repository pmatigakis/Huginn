import math

def isclose(number_1, number_2, tolerance):
    d = math.fabs(number_1 - number_2)
    
    if d > tolerance:
        return False
    
    return True