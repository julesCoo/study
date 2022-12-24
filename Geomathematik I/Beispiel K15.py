from math import cos, radians
from libsphere import SphereCoords, SphereTriangle, ha1
from libgeo import fmt_deg_str, from_deg

phi1 = from_deg(17, 34, 9.14)
lam1 = from_deg(52, 18, 37.11)

phi2 = from_deg(18, 4, 15.42)
lam2 = from_deg(52, 27, 11.41)

a13 = from_deg(57, 5, 2.8)
a23 = from_deg(120, 46, 21.76)

P1 = SphereCoords(phi1, lam1)
P2 = SphereCoords(phi2, lam2)


T1 = SphereTriangle.sws(
    # Meridian going through P2
    a=phi2 - phi1,
    # Circle of latitude going through P1
    b=(lam2 - lam1) * cos(phi1),
    gamma=radians(90),
)

T2 = SphereTriangle.wsw(
    alpha=a23,
    beta=a13,
    c=T1.c,
)

P3, _ = ha1(P1, T2.a, radians(90) - (T1.alpha + T2.beta))

print(f"P3 = {P3}")
print(f"exzess = {fmt_deg_str(T2.excess)}")
