from libsphere import SphereCoords, ha1, ha2
from math import degrees, radians

P1 = SphereCoords(
    phi=radians(-15),
    lam=radians(112),
)

a12 = radians(326)
s12 = 0.35

P2, a21 = ha1(P1, s12, a12)
P1_, a12_ = ha1(P2, s12, a21)

s12_, a12_ = ha2(P1, P2)

print(f"P1 = {P1}")
print(f"P2 = {P2}")
print(f"P1'= {P1_}")

print(f"s12' = {s12}")
print(f"a12' = {degrees(a12_)}")
