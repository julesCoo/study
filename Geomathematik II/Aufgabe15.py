"""
Auf einem Zylinder in nachfolgender Parameterdarstellung sei eine Schrauben-
linie durch u = at, v = t (a = konst.) definiert. Man berechne den Winkel
zwischen u-Linie und dieser Flächenkurve und prüfe, ob die Schraubenlinie eine
geodätische Linie darstellt.
"""

# %%
from sympy import *
from lib import *

u, v, a, t = symbols("u v a t", real=True)


surface = Surface(
    (u, v),
    cos(v),
    sin(v),
    u,
)

# v = t, u = a * t
curve = Curve(
    t,
    cos(t),
    sin(t),
    a * t,
)

# Winkel zwischen u-Linie und Tangentenvektor der Flächenkurve
surf_u = surface.f_u
curve_t = curve.f_t
angle = acos(surf_u.dot(curve_t) / (surf_u.norm() * curve_t.norm())).simplify()
display("Winkel von Schraubenkurve und u-Linie", angle)

sc = SurfaceCurve(surface, curve)

# Bei einer geodätischen Linie sollte das Skalarprodukt des Krümmungsvektors
# mit der u- und v-Linie jeweils 0 sein.
dot_u = surface.f_u.dot(curve.f_tt).simplify()
dot_v = surface.f_v.dot(curve.f_tt).simplify()
display("Skalarprodukt mit u-Linie", dot_u)
display("Skalarprodukt mit v-Linie", dot_v)

# Außerdem sollte die geodätische Krümmung 0 sein.
display("Geodätische Krümmung", sc.kappa_g)

# Demnach ist die Schraubenlinie keine geodätische Linie.

setup_plot(3)
surface.plot(
    u_range=(-10, 10, 25),
    v_range=(0, 2 * np.pi, 25),
    subs={a: 0.1},
)
curve.plot(
    t_range=(-10, 10, 100),
    subs={a: 0.1},
)
# %%
