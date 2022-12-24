from math import sqrt, pi


m = 0.436  # kg
k = 5  # N/m
b = 2.5  # Ns/m

# Natural frequency of the undampened spring-mass system:
f = sqrt(k / m) / (2 * pi)

# Frequency with damping:
f_damp = sqrt((k - b**2 / (4 * m)) / m) / (2 * pi)

# Converted into radians/s:
omega = 2 * pi * f_damp
print(omega)
