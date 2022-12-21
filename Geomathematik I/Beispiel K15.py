from math import cos, radians
from libsphere import SphereCoords, SphereTriangle
from libgeo import fmt_gon, from_gon

phi1 = from_gon(17, 34, 9.14)
lam1 = from_gon(52, 18, 37.11)

phi2 = from_gon(18, 4, 15.42)
lam2 = from_gon(52, 27, 11.41)

a13 = from_gon(57, 5, 2.8)
a23 = from_gon(120, 46, 21.76)

P1 = SphereCoords(phi1, lam1)
P2 = SphereCoords(phi2, lam2)

T1 = SphereTriangle.sws(
    a=lam2 - lam1,
    b=phi1,
    gamma=radians(90),
)
T2 = SphereTriangle.sws(
    a=(lam2 - lam1) * cos(phi1),
    b=phi1,
    gamma=radians(90),
)
T3 = SphereTriangle.sws(
    a=phi2 - phi1,
    b=T2.a,
    gamma=radians(90),
)

T4 = SphereTriangle.wsw(
    alpha=a23,
    beta=a13,
    c=T3.c,
)

P3 = P1.ha1(T4.a, radians(90) - (T3.alpha + T4.beta))

print(f"P3 = {P3}")
print(f"exzess = {T4.excess}")
