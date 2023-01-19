from math import cos, sin
from libgeo import fmt_deg_str, from_deg
from libsphere import SphereTriangle, SphereCoords, ha1, ha2

P1 = SphereCoords(from_deg(43, 41, 1), from_deg(15, 56, 58))
P2 = SphereCoords(from_deg(43, 41, 1), from_deg(13, 30, 5))

s12, a12, _ = ha2(P1, P2)
print(fmt_deg_str(s12))
print(fmt_deg_str(a12))

earth_radius = 6379  # km


so = s12 * earth_radius
sl = (P1.lam - P2.lam) * earth_radius * cos(P1.phi)
print(so)
print(sl)
print(sl - so)
print(sl / so)
