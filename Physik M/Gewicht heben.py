import math

mass = 27
velocity = 8
(x0, y0) = (0, 0)
(x1, y1) = (2, 7)


def friction_force(vx, vy):
    v = (vx**2 + vy**2) ** 0.5
    return (-v * vx, -v * vy)


def gravity_force():
    return (0, -mass * 9.807)


dx = x1 - x0
dy = y1 - y0

d = (dx**2 + dy**2) ** 0.5
dx /= d
dy /= d

step_size = 0.0001
num_steps = int(d / step_size)
work = 0
for step in range(num_steps):
    x = x0 + step * step_size * dx
    y = y0 + step * step_size * dy

    (vx, vy) = (velocity * dx, velocity * dy)
    (fx, fy) = friction_force(vx, vy)
    (gx, gy) = gravity_force()

    # total force
    (ffx, ffy) = (fx + gx, fy + gy)

    dot = ffx * dx + ffy * dy
    work -= dot * step_size

print(work)
