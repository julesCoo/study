from lib.vector import Vec3
from lib.forces import coulomb, electronCharge


r1 = Vec3(5, 4, -3) * 1e-6
q1 = 5e-12

r2 = Vec3(-5, -5, 5) * 1e-6
q2 = -3e-11

rA = Vec3(52, 88, -78) * 1e-6
rB = Vec3(48, 86, -83) * 1e-6
test_charge = 1

potA1 = coulomb(pos1=r1, pos2=rA, charge1=q1, charge2=test_charge)
potA2 = coulomb(pos1=r2, pos2=rA, charge1=q2, charge2=test_charge)
potA = potA1 + potA2

potB1 = coulomb(pos1=r1, pos2=rB, charge1=q1, charge2=test_charge)
potB2 = coulomb(pos1=r2, pos2=rB, charge1=q2, charge2=test_charge)
potB = potB1 + potB2

diff = potA.length() - potB.length()
print(diff)
