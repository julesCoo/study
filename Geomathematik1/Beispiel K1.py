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

# P1 is at equator and prime meridian
P2 = SphereCoords(0, 0)

# P1 is at equator, in positive longitude direction
P1, _ = P2.ha1(radians(90), triangle.c)

P3, _ = P2.ha1(radians(90) - triangle.beta, triangle.a)
P3_, _ = P1.ha1(radians(270) + triangle.alpha, triangle.b)

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

s13, v13 = P1.ha2(P3)
s23, v23 = P2.ha2(P3)
s21, v21 = P2.ha2(P1)

s32, v32 = P3_.ha2(P2)
s31, v31 = P3_.ha2(P1)


print(f"s13 = {fmtdeg(s13)}")
print(f"s23 = {fmtdeg(s23)}")
print(f"s21 = {fmtdeg(s21)}")
print(f"v13 = {fmtdeg(v13)}")
print(f"v23 = {fmtdeg(v23)}")
print(f"v21 = {fmtdeg(v21)}")
print(f"beta = {fmtdeg(v21-v23)}")
print(f"gamma = {fmtdeg(v32-v31)}")
