import math
from lib.vector import Vec2


def v(t):
    return Vec2(
        12 * math.cos(12 * t),
        13 * math.sin(13 * t),
    )


dt = 1e-5
pos = Vec2(0, 0)
t = 0

while t < 7:
    pos += v(t) * dt
    t += dt

print(pos.x, pos.y)
