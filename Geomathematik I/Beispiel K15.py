from libsphere import SphereCoords, SphereTriangle, ha1, ha2, vws
from libgeo import fmt_deg_str, from_deg

phi1 = from_deg(17, 34, 9.14)
lam1 = from_deg(52, 18, 37.11)

phi2 = from_deg(18, 4, 15.42)
lam2 = from_deg(52, 27, 13.41)

a13 = from_deg(57, 5, 2.8)
a23 = from_deg(120, 46, 21.76)

P1 = SphereCoords(phi1, lam1)
P2 = SphereCoords(phi2, lam2)
P3 = vws(P1, P2, a13, a23)

T = SphereTriangle.ppp(P1, P2, P3)

print(f"P3 = {P3}")
print(f"exzess = {fmt_deg_str(T.excess())}")
