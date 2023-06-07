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

surface = Surface(
    (phi, lamda),
    R * cos(phi) * cos(lamda),
    R * cos(phi) * sin(lamda),
    R * sin(phi),
)

display("Hauptkrümmungen Kugel", surface.R1, surface.R2)
# Hauptkrümmungen sind identisch und daher rotationsinvariant -> Nabelpunkte.

meridian = SurfaceCurve(
    surface,
    Curve(
        (phi),
        R * cos(phi) * cos(lamda),
        R * cos(phi) * sin(lamda),
        R * sin(phi),
    ),
)

display("Normalkrümmung Meridiane", meridian.kappa_n)
display("Geodätische Krümmung Meridiane", meridian.kappa_g)
# Normalkrümmung ist konstant R, geodätische Krümmung ist 0 -> Meridiane sind Geodäten.

parallel = SurfaceCurve(
    surface,
    Curve(
        (lamda),
        R * cos(phi) * cos(lamda),
        R * cos(phi) * sin(lamda),
        R * sin(phi),
    ),
)
display("Normalkrümmung Parallelkreise", parallel.kappa_n)
display("Geodätische Krümmung Parallelkreise", parallel.kappa_g)
# Nur Am Äquator (phi=0) ist die Normalkrümmung R und die geodätische Krümmung 0.

setup_plot()
surface.plot(
    u_range=(-pi / 2, pi / 2, 45),
    v_range=(0, 2 * pi, 45),
    subs={R: 1},
)

# %%
