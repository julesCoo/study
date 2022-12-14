import numpy as np

k = 6  # N/m
mass = 0.352  # kg

y = 0  # m
vy = -0.04  # m/s

friction = -0.5  # dvy/dt

dt = 1e-6
for i in np.arange(0, 3, dt):
    y += vy * dt
    vy += (friction * vy - k * y) / mass * dt

print(y)
