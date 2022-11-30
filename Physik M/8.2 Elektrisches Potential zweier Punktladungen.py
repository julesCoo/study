from lib.vector import Vec3
from lib.electrostatic import ElectricField

f = ElectricField()
f.add_point_charge(2e-12, Vec3(4, -5, 2) * 1e-6)
f.add_point_charge(-5e-11, Vec3(-2, 4, 4) * 1e-6)

rA = Vec3(91, 63, -81) * 1e-6
rB = Vec3(95, 59, -77) * 1e-6

voltage = f.get_potential(rA) - f.get_potential(rB)
print(voltage)
