# %%
from sympy import *
from lib import *

nu, lam, t = symbols("nu lambda t", real=True)

# Gleichungen der Parameterlinien
f_nu = pi / 2 - t
f_lam = ln(cot(pi / 4 - t / 2))

# Vektorform der Fläche (Einheitskugel)
f_sphere = ImmutableDenseMatrix(
    [
        sin(nu) * cos(lam),
        sin(nu) * sin(lam),
        cos(nu),
    ]
)

# Vektorform der Parameterlinie
f_line = f_sphere.subs(
    [
        (nu, f_nu),
        (lam, f_lam),
    ]
)

tangent = diff(f_line, t).simplify()
f_sphere_nu = diff(f_sphere, nu).simplify()


# %%


setup_plot()
plot_surface(
    lambdify((nu, lam), f_sphere),
    u_range=(0, np.pi, 20),
    v_range=(0, 2 * np.pi, 40),
)
plot_line(
    lambdify((t), f_line),
    t_range=(-np.pi / 2, np.pi / 2, 100),
    t_count=100,
)

plt.show()

# %%
