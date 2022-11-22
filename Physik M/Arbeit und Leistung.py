import math

m = 0.550
v = 0.03

dz = 1
dx = 4

alpha = math.atan2(dz, dx)


def F_drag(v):
    return -v


L = 0.16
W_drag = F_drag(v) * L

F_gravity = m * -9.807 * math.sin(alpha)
W_gravity = F_gravity * L

W = W_drag + W_gravity
print(W)
print(W_drag, W_gravity)

F = F_drag(v) + F_gravity
print(F * v)
