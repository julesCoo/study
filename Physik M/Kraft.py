from lib.forces import lorentz
from lib.vector import Vec3

# Geschwindigkeit in x (m/s)
v = Vec3(-5e5, 8e5, -4e5)

# Elektrisches Feld (V/m)
E = Vec3(-7e3, -4e3, 4e3)

B = Vec3(-5, -5, 3)

print(lorentz(E, B, v))
