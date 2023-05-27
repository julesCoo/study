# %%
import numpy as np
from sympy import Matrix, cos, diff, lambdify, sin, symbols, sqrt

# Die verwendeten Variablen und ihr Wertebereich
u, v = symbols("u v", real=True)
u_min, u_max = 0, 1
v_min, v_max = 0, 2 * np.pi

# Die Gleichung der Raumkurve
x = Matrix(
    [
        3 * u * cos(v),
        2 * u * sin(v),
        u**2,
    ]
)

# Länge eines Kurvenstücks
x_norm = x.norm().simplify()

# Ableitungen
x_u = diff(x, u)
x_uu = diff(x_u, u)
x_v = diff(x, v)
x_vv = diff(x_v, v)
x_uv = diff(x_u, v)

# Flächennormalenvektor
z = x_u.cross(x_v)
z = z / z.norm()

# Erste Fundamentalform
E = x_u.dot(x_u)
F = x_u.dot(x_v)
G = x_v.dot(x_v)

# Zweite Fundamentalform
L = x_uu.dot(z)
M = x_uv.dot(z)
N = x_vv.dot(z)

# Krümmungen
H = (E * N - 2 * F * M + G * L) / (E * G - F**2)
K = (L * N - M**2) / (E * G - F**2)
R1 = H + sqrt(H**2 - K)
R2 = H - sqrt(H**2 - K)

"""Evaluation an Punkt"""
u_val, v_val = 0.5, np.pi

# u- und v-Linien (und ihre Ableitungen) an dem Punkt
U = x.subs({v: v_val})
V = x.subs({u: u_val})

U_u = diff(U, u)
V_v = diff(V, v)

# Tangentenvektor an dem Punkt
x_x = x_u.dot(U_u) + x_v.dot(V_v)


"""Plotting"""
import matplotlib.pyplot as plt


# Raumkurve plotten
uu, vv = np.meshgrid(
    np.linspace(u_min, u_max, 50),
    np.linspace(v_min, v_max, 50),
)
x_callable = lambdify((u, v), x, modules="numpy")
xs = x_callable(uu, vv).reshape(3, 50, 50)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_wireframe(xs[0], xs[1], xs[2], color="black", alpha=0.1)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# %%

"Task 9"
"Task 11"
"Task 1c,d"
