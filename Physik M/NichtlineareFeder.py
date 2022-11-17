mass = 2
start_velocity = -3
start_position = 0


def F_Feder(x):
    return -3 * x * abs(x)


def F_drag(v):
    return -0.3 * v


x = start_position
v = start_velocity
t = 0
dt = 1e-5

max_f = 0
max_f_t = 0

for i in range(100000):
    t += dt
    f = F_Feder(x) + F_drag(v)
    a = f / mass
    v += a * dt
    x += v * dt

    if abs(f) > max_f:
        max_f = abs(f)
        max_f_t = t
        
print("t=", max_f_t)
print("max_f=", max_f)
