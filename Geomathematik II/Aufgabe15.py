# %%
from sympy import *
from lib import *

u, v, a, t = symbols("u v a t", real=True)

f_u = a * t
f_v = t

#
f_line = ImmutableDenseMatrix(
    [
        cos(v),
        sin(v),
        u,
    ]
)

f_line2 = f_line.subs(
    [
        (u, f_u),
        (v, f_v),
        (a, 1),
    ]
)

setup_plot()
plot_line(
    lambdify((t), f_line2),
    t_range=(-10, 10),
    t_count=100,
)

# %%
