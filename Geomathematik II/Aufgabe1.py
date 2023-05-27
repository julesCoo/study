# %%
from sympy import *
from lib import *


delta, lamda = symbols("delta lambda", real=True, positive=True)

x = ImmutableDenseMatrix(
    [
        (4 + cos(delta)) * cos(lamda),
        (4 + cos(delta)) * sin(lamda),
        sin(delta),
    ]
)

dict = analyse_surface_curve(x, delta, lamda)
display("K", dict["K"])
display("H", dict["H"])
display("R1", dict["R1"])
display("R2", dict["R2"])

# %%

setup_plot()
plot_surface(
    lambdify((delta, lamda), x),
    u_range=(0, 2 * np.pi),
    v_range=(0, 2 * np.pi),
    u_count=40,
    v_count=40,
    close_surface=True,
)

# %%
