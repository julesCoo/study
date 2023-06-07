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


# Anfangsbedingung
delta_0 = pi / 4
lamda_0 = pi / 3
alpha_0 = pi / 3
s = 0.1

# Erste Ordnung
E = surface.E
G = surface.G
E_lamda = diff(E, lamda)
G_delta = diff(G, delta)

delta_s = 1 / sqrt(E) * cos(alpha_0)
lamda_s = 1 / sqrt(G) * sin(alpha_0)
alpha_s = 1 / (2 * sqrt(E * G)) * (E_lamda * delta_s - G_delta * lamda_s)

# Zweite Ordnung
delta_ss = (4 + cos(delta)) * (-sin(delta)) * lamda_s**2
lamda_ss = 2 * sin(delta) / (4 + cos(delta)) * delta_s * lamda_s

# Dritte Ordnung
delta_sss = diff(delta_ss, delta) + diff(delta_ss, lamda)
lamda_sss = diff(lamda_ss, delta) + diff(lamda_ss, lamda)

# Taylorreihe auswerten
delta_1 = delta_0 + s * delta_s + s**2 / 2 * delta_ss + s**3 / 6 * delta_sss
lamda_1 = lamda_0 + s * lamda_s + s**2 / 2 * lamda_ss + s**3 / 6 * lamda_sss

print(
    delta_1.subs({delta: delta_0, lamda: lamda_0}),
    lamda_1.subs({delta: delta_0, lamda: lamda_0}),
)

# %%
setup_plot((-4, 4), (-4, 4), (-4, 4))
surface.plot(
    u_range=(0, pi, 45),
    v_range=(0, 2 * pi, 45),
)

# %%
