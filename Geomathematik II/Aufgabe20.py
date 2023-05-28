"""
Man diskutiere die Normalkrümmung und die geodätische Krümmung für Me-
ridiane und Parallelkreise einer Kugel x = x(φ,λ) mit dem Radius R, berechne
die Hauptkrümmungen und zeige rechnerisch, daß die Kugel ausschließlich aus
Nabelpunkten besteht.
"""
# %%
from sympy import *
from lib import *
from numpy import pi

R = symbols("R", real=True, positive=True)
phi, lamda = symbols("phi lambda", real=True)

f_surf = ImmutableDenseMatrix(
    [
        R * cos(phi) * cos(lamda),
        R * cos(phi) * sin(lamda),
        R * sin(phi),
    ]
)

surf_props = analyze_surface((phi, lamda), f_surf)
display("Hauptkrümmungen Kugel", surf_props["R1"], surf_props["R2"])
# Hauptkrümmungen sind identisch und daher rotationsinvariant -> Nabelpunkte.

phi_props = analyze_curve_on_surface((phi, lamda), f_surf, (phi), f_surf)
display("Normalkrümmung Meridiane", phi_props["kappa_n"])
display("Geodätische Krümmung Meridiane", phi_props["kappa_g"])
# Normalkrümmung ist konstant R, geodätische Krümmung ist 0 -> Meridiane sind Geodäten.

lamda_props = analyze_curve_on_surface((phi, lamda), f_surf, (lamda), f_surf)
display("Normalkrümmung Parallelkreise", lamda_props["kappa_n"])
display("Geodätische Krümmung Parallelkreise", lamda_props["kappa_g"])
# Nur Am Äquator (phi=0) ist die Normalkrümmung R und die geodätische Krümmung 0.

# %%


setup_plot()
plot_surface(
    lambdify((phi, lamda), f_surf.subs(R, 1)),
    u_range=(-pi / 2, pi / 2),
    v_range=(0, 2 * pi),
    u_count=45,
    v_count=45,
)

# %%
