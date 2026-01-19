import math
import cmath

def sqrt_value(x: float):

    if x == 0:
        return 0.0
    if x > 0:
        return math.sqrt(x)
    return cmath.sqrt(x)
