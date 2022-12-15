from math import radians
from libgeo import Angle
from libsphere import SphereTriangle, SphereCoords


def fmtdeg(rad: float) -> str:
    return Angle.from_rad(rad).to_deg_str()


# P3 to P2
a = Angle.from_deg(5, 41, 16.38).to_rad()

# P3 to P1
b = Angle.from_deg(2, 37, 44.60).to_rad()

# in P3
gamma = Angle.from_deg(86, 19, 21.40).to_rad()

triangle = SphereTriangle.sws(a, b, gamma)

# P2 is at equator and prime meridian
P2 = SphereCoords(0, 0)

# P1 is at equator, in positive longitude direction
P1, _ = P2.ha1(triangle.c, radians(90))

P3, _ = P2.ha1(triangle.a, radians(90) - triangle.beta)
P3_, _ = P1.ha1(triangle.b, radians(270) + triangle.alpha)

print(f"    a = {fmtdeg(triangle.a)}")
print(f"    b = {fmtdeg(triangle.b)}")
print(f"    c = {fmtdeg(triangle.c)}")
print(f"alpha = {fmtdeg(triangle.alpha)}")
print(f" beta = {fmtdeg(triangle.beta)}")
print(f"gamma = {fmtdeg(triangle.gamma)}")
print(f"   P1 = {P1}")
print(f"   P2 = {P2}")
print(f"   P3 = {P3}")
print(f"  P3' = {P3_}")
