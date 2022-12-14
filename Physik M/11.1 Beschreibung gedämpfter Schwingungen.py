import numpy as np

mass = 2
x = 0.02
v = 0


def f_spring(x):
    return -2 * x * abs(x)


def f_friction(v):
    return -0.02 * v**3


dt = 1e-6
for t in np.arange(0, 3, dt):
    x += dt * v
    v += dt * (f_spring(x) + f_friction(v)) / mass

print(x)
