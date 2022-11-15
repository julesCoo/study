from lib.vector import Vec3
from lib.forces import coulomb, electronCharge


test_pos = Vec3(80, 83, -57) * 1e-6
test_charge = 1

q1_pos = Vec3(3, -4, -4) * 1e-6
q1_charge = 9e-12

q2_pos = Vec3(4, 2, -5) * 1e-6
q2_charge = -9e-11

f1 = coulomb(
    pos1=q1_pos,
    charge1=q1_charge,
    pos2=test_pos,
    charge2=test_charge,
)

f2 = coulomb(
    pos1=q2_pos,
    charge1=q2_charge,
    pos2=test_pos,
    charge2=test_charge,
)

field = -(f1 + f2) * (1 / test_charge)
print(field)
