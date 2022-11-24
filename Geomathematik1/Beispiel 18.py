from lib2d.Circle import Circle
from lib2d.Point import Point
from lib2d.Line import Line
from lib.Angle import Angle, gon
from lib2d.Plot import Plot
from lib2d.Algorithms import HelmertTransform, Vorwärtsschnitt_Winkel
import numpy as np


P1 = Point(5207864.64, -70178.81)
P2 = Point(5208032.30, -70021.36)

# unorientierte Richtungen
rN1P1 = gon(0)
rN1P2 = gon(54.593)
rN1N2 = gon(106.778)

rN2N1 = gon(0)
rN2P1 = gon(22.426)
rN2P2 = gon(71.204)

alpha = rN1P2 - rN1P1
beta = rN1N2 - rN1P2
gamma = rN2P1 - rN2N1
delta = rN2P2 - rN2P1

N1_ = Point(0, 0)
N2_ = Point(0, 100)
P1_ = Vorwärtsschnitt_Winkel(
    A=N2_,
    B=N1_,
    alpha=gamma,
    beta=alpha + beta,
)
P2_ = Vorwärtsschnitt_Winkel(
    A=N2_,
    B=N1_,
    alpha=gamma + delta,
    beta=beta,
)

print("N1' =", N1_)
print("N2' =", N2_)
print("P1' =", P1_)
print("P2' =", P2_)

ct = HelmertTransform((P1_, P2_), (P1, P2))
N1 = ct.transform(N1_)
N2 = ct.transform(N2_)

# Finde N1, N2

p = Plot(Point(5207600, -70200), Point(5208100, -69800))
p.add_point(P1, "P1")
p.add_point(P2, "P2")
p.add_point(N1, "N1")
p.add_point(N2, "N2")
p.save("Geomathematik1/Beispiel 18.png")

print("N1 = ", N1)
print("N2 = ", N2)
