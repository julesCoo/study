"""
Man bestimme die Hauptkrümmungsradien des nachfolgenden Rotationsellip-
soides am Äquator und am Pol.
"""
# %%
from sympy import *
from lib import *
from numpy import pi

a, b = symbols("a b", real=True, positive=True)
beta, lamda = symbols("beta lambda", real=True)
Q
surface = Surface(
    (beta, lamda),
    a * cos(beta) * cos(lamda),
    a * cos(beta) * sin(lamda),
    b * sin(beta),
)

R1 = surface.R1
R2 = surface.R2
display("Hauptkrümmungen", R1, R2)

R1_equator = R1.subs(beta, 0).simplify()
R2_equator = R2.subs(beta, 0).simplify()
display("Hauptkrümmungen am Äquator", R1_equator, R2_equator)
# (maybe) simplifies to a

R1_pole = R1.subs(beta, pi / 2).simplify()
R2_pole = R2.subs(beta, pi / 2).simplify()
display("Hauptkrümmungen am Pol", R1_pole, R2_pole)
# simplifies to a**2 / b

surface.plot(
    u_range=(-pi / 2, pi / 2, 45),
    v_range=(0, 2 * pi, 45),
    subs={a: 1, b: 2},
)

# %%
