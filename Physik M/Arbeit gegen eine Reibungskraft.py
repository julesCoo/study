from math import cos, sin, pi
import numpy as np


def pos(t):
    x = 7 * cos(4 * t)
    y = 4 * sin(7 * t)
    return (x, y)


def friction(vx, vy):
    v = (vx**2 + vy**2) ** 0.5
    return (-v * vx, -v * vy)


t0 = 0
t1 = 6
step_size = 0.0001

work = 0
for t in np.arange(t0, t1, step_size):
    (x1, y1) = pos(t)
    (x2, y2) = pos(t + step_size)

    # Distance traveled
    d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # normalized direction
    (dx, dy) = ((x2 - x1) / d, (y2 - y1) / d)

    # denormalized velocity
    (vx, vy) = (dx * d / step_size, dy * d / step_size)

    (fx, fy) = friction(vx, vy)
    dot = fx * dx + fy * dy

    work -= dot * d

print(work)
