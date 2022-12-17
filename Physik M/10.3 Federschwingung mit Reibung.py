import numpy as np

k = 6  # N/m
mass = 0.352  # kg

y = 0  # m
vy = -0.04  # m/s

friction = -0.5  # dvy/dt

dt = 1e-6
for _ in np.arange(0, 3, dt):
    f_friction = friction * vy
    f_spring = -k * y
    ay = (f_friction + f_spring) / mass
    vy += ay * dt
    y += vy * dt

print(y)
