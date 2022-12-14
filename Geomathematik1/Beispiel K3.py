from libsphere import SphereCoords
from libgeo import Angle


P1 = SphereCoords.from_phi_lamda(
    phi=Angle.from_deg(-15).to_rad(),
    lam=Angle.from_deg(112).to_rad(),
)

a12 = Angle.from_deg(326).to_rad()
s12 = 0.35

P2, a21 = P1.ha1(s12, a12)
P1_, a12_ = P2.ha1(s12, a21)

print(f"P1 = {P1}")
print(f"P2 = {P2}")
print(f"P1' = {P1_}")
