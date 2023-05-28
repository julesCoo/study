# %%
from sympy import *
from lib import *
from numpy import pi

delta, lamda = symbols("delta lambda", real=True, nonnegative=True)

surface = Surface(
    (delta, lamda),
    (4 + cos(delta)) * cos(lamda),
    (4 + cos(delta)) * sin(lamda),
    sin(delta),
)

surface.plot(
    u_range=(0, pi),
    v_range=(0, 2 * pi),
    u_count=45,
    v_count=45,
)

# %%
