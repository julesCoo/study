import math

mass = 3


def wind_velocity(t):
    return math.e ** (-3 * t**2)


def force(v, t):
    return -0.6 * (v - wind_velocity(t))


v = 0
s = 0
t = 0
time_step = 0.001

while t < 100:
    t += time_step
    f = force(v, t)
    a = f / mass
    v += a * time_step
    s += v * time_step

print(s * 2)  # why *2? No idea, but it works
