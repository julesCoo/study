from libgeo import from_deg
from libsphere import SphereTriangle, SphereCoords, ha1, ha2

P1 = SphereCoords(from_deg(43, 41, 1), from_deg(15, 56, 58))
P2 = SphereCoords(from_deg(43, 41, 1), from_deg(13, 30, 5))

s12, a12, _ = ha2(P1, P2)
