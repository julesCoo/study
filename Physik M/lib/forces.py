import math
from lib.vector import Vec3


gravitationalConstant = 6.674e-11  # G

# Returns the gravitational force being applied the object at pos1
def gravity(mass1: float, mass2: float, pos1: Vec3, pos2: Vec3) -> Vec3:
    r21 = -pos2 + pos1
    force = gravitationalConstant * mass1 * mass2 / r21.length() ** 2
    return r21.normalized() * force
