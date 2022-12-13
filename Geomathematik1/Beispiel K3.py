from libsphere import SphereTriangle, SphereCoords
from libgeo import Angle

P1 = SphereCoords.from_phi_lamda(
    phi=Angle.from_deg(-15).to_rad(),
    lam=Angle.from_deg(112).to_rad(),
)

alpha12 = Angle.from_deg(326).to_rad()
s12 = 0.35

P2, alpha21 = P1.ha1(alpha12, s12)
P1_, alpha12_ = P2.ha1(alpha21, s12)

print(f"P1 = {P1}")
print(f"P2 = {P2}")
print(f"P1' = {P1_}")
