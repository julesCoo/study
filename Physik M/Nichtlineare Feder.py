mass = 0.482


def F(x):
    return -7 * x - 7 * x**3


x = -0.18
v = 0

dt = 1e-4


max_v = 0
for i in range(1000000):
    f = F(x)
    a = f / mass
    v += a * dt
    x += v * dt
    max_v = max(max_v, abs(v))

print(max_v)


# 0.400000	-0.00503196	0.691225
