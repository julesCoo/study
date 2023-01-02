from math import radians
from libgeo import from_deg, fmt_deg
from libsphere import SphereTriangle, SphereCoords

# P3 to P2
a = from_deg(5, 41, 16.38)

# P3 to P1
b = from_deg(2, 37, 44.60)

# in P3
gamma = from_deg(86, 19, 21.40)

triangle = SphereTriangle.sws(a, b, gamma)

# P2 is at equator and prime meridian
P2 = SphereCoords(0, 0)

# P1 is at equator, in positive longitude direction
P1, _ = P2.ha1(triangle.c, radians(90))

P3, _ = P2.ha1(triangle.a, radians(90) - triangle.beta)
P3_, _ = P1.ha1(triangle.b, radians(270) + triangle.alpha)

print(f"    a = {fmt_deg(triangle.a)}")
print(f"    b = {fmt_deg(triangle.b)}")
print(f"    c = {fmt_deg(triangle.c)}")
print(f"alpha = {fmt_deg(triangle.alpha)}")
print(f" beta = {fmt_deg(triangle.beta)}")
print(f"gamma = {fmt_deg(triangle.gamma)}")
print(f"   P1 = {P1}")
print(f"   P2 = {P2}")
print(f"   P3 = {P3}")
print(f"  P3' = {P3_}")
