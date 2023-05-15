# %%
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sin, cos, Matrix, diff, lambdify

u, v = symbols("u v", real=True)
u_range = (0, 1)
v_range = (0, 2 * np.pi)

# Die Raumkurve selbst
x = Matrix(
    [
        3 * u * cos(v),
        2 * u * sin(v),
        u**2,
    ]
)

# Bogenlänge
x_norm = x.norm().simplify()

# Erste Ableitungen nach u, v und uv
x_u = diff(x, u)
x_v = diff(x, v)Q
x_u_v = diff(x_u, v)

# Erste Fundamentalform
E = x_u.dot(x_u)
F = x_u.dot(x_v)
G = x_v.dot(x_v)

# Raumkurve plotten
uu, vv = np.meshgrid(
    np.linspace(u_range[0], u_range[1], 50),
    np.linspace(v_range[0], v_range[1], 50),
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
