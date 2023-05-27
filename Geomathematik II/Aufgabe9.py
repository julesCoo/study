# %%
from sympy import *
from lib import *

x, y, z, p, q = symbols("x y z p q", real=True)
a, b = symbols("a b", real=True, positive=True)

# gegeben die Formel für ein Ellipsoid
ellipsoid = Eq(b * x**2 + a * y**2, 2 * a * b * z)

# dort kann x mit a * p und y mit b * q ersetzt werden
f = ellipsoid
f = f.subs(x, a * p)
f = f.subs(y, b * q)

# das ergibt dann die Vektorform der Fläche
F = Matrix(
    [
        a * p,
        b * q,
        solve(f, z)[0],
    ]
)
display("Raumkurve", F)

# die Ableitungen nach p und q ergeben die Tangentenvektoren
F_p = F.diff(p)
F_q = F.diff(q)

# Der Winkel zwischen den Tangentenvektoren ist dann
angle = acos(F_p.dot(F_q) / (F_p.norm() * F_q.norm()))
display("Winkel zwischen Tangenvektoren", angle.simplify())

# %% Plot the function assuming a=1 and b=3


f = ellipsoid
f = f.subs(a, 1)
f = f.subs(b, 3)
f_z = solve(f, z)[0]

f_surf = Matrix(
    [
        x,
        y,
        f_z,
    ]
)


setup_plot()
plot_surface(
    lambdify((x, y), f_surf),
    u_range=(-1, 1),
    v_range=(-1, 1),
)


plt.show()


# %%
