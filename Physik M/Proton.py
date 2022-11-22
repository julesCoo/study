from lib.vector import Vec3

E = Vec3(5, 6, 2)

pos1 = Vec3(3, 8, 8) * 1e-6
pos2 = Vec3(0, 0, 0)

protonCharge = 1.602176487e-19
protonMass = 1.672621777e-27

Fx = E.x * protonCharge
Fy = E.y * protonCharge
Fz = E.z * protonCharge

dx = pos2.x - pos1.x
dy = pos2.y - pos1.y
dz = pos2.z - pos1.z

Wx = Fx * dx
Wy = Fy * dy
Wz = Fz * dz
W = Wx + Wy + Wz
print(W)
