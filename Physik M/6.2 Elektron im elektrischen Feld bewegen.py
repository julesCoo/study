from lib.calculus import integrate
from lib.vector import Vec3

"""
Welche Arbeit wird benötigt, um ein Elektron von der Position r1 
zur Position r2 in einem elektrischen Feld E zu bewegen?
Die Kraft auf das Elektron lautet -eE wobei -e = -1.60217662e-19
die Ladung des Eleḱtrons ist. Es wird gefrafgt, welche Arbeit zum 
Bewegen des Elektrons verrichtet wird und nicht, welche Arbeit von 
der Kraft verrichtet wird.
"""

# Electron charge
e = 1.602176487e-19

# Start position of the electron
r1 = Vec3(7, 4, -6)

# End position of the electron
r2 = Vec3(-4, -7, -4)

# Power of the electrical field at the position r
def E(r: Vec3):
    return Vec3(
        8 * r.x,
        8,
        6 * r.z**2,
    )


# Movement vector
dr: Vec3 = r2 - r1
dist = dr.normalize()

# Force on the electron at the position r when moving in dr
def force(r: Vec3) -> float:
    fE = E(r) * e
    return dr @ fE


work = integrate(0, dist, lambda s: force(r1 + dr * s))
print(work)
