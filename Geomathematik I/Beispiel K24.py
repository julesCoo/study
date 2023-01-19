from math import tau
from libgeo import fmt_deg, fmt_deg_str, from_deg
from libsphere import SphereCoords, SphereTriangle, ha1, ha2

radius = 6370  # km

P1 = SphereCoords(
    phi=from_deg(-48, 32, 3),
    lam=from_deg(15, 43, 48),
)

P2 = SphereCoords(
    phi=from_deg(-7, 15, 46),
    lam=from_deg(-30, 26, 4),
)

s12, a12, a21 = ha2(P1, P2)

s13 = 10500  # km
a23 = from_deg(31, 24, 12)

[T] = SphereTriangle.ssw(
    alpha=a21 - a23,
    a=s13 / radius,
    c=s12,
)

P3, _ = ha1(P2, T.b, a23)

area = SphereTriangle.ppp(P1, P2, P3).area(radius)

print(f"{P3} ({area:,} km²)")
