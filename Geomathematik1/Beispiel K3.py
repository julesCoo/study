from libsphere import SphereCoords
from math import degrees, radians

P1 = SphereCoords.from_phi_lamda(
    phi=radians(-15),
    lam=radians(112),
)

a12 = radians(326)
s12 = 0.35

P2, a21 = P1.ha1(s12, a12)
P1_, a12_ = P2.ha1(s12, a21)

s12_, a12_ = P1.ha2(P2)

print(f"P1 = {P1}")
print(f"P2 = {P2}")
print(f"P1'= {P1_}")

print(f"s12' = {s12}")
print(f"a12' = {degrees(a12_)}")
