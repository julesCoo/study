from math import cos


m = 3  # kg
k = 4  # N/m
b = 0.7  # Ns/m
t1 = 6

# def f_drive(t):
#     return 0.07 * cos(7 * t)


# def f_spring(x):
#     return -k * x


# def f_drag(v):
#     return -b * v


# x = 0
# v = 0
# dt = 1e-4
# t = 0

# while t < t1:
#     a = (f_spring(x) + f_drag(v) + f_drive(t)) / m
#     x += v * dt
#     v += a * dt
#     t += dt

# print(x)
