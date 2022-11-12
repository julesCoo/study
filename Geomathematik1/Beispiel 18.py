from lib2d.Circle import Circle
from lib2d.Point import Point
from lib2d.Line import Line
from lib.Angle import Angle, gon
from lib2d.Plot import Plot
from lib2d.Algorithms import HA1, HA2

P1 = Point(5207864.64, -70178.81)
P2 = Point(5208032.30, -70021.36)

# unorientierte Richtungen
N1P1 = gon(0)
N1P2 = gon(54.593)
N1N2 = gon(106.778)

N2N1 = gon(0)
N2P1 = gon(22.426)
N2P2 = gon(71.204)


# Finde N1, N2

p = Plot(Point(5207800, -70200), Point(5208100, -70000))
p.add_point(P1, "P1")
p.add_point(P2, "P2")
p.save("Geomathematik1/Beispiel 18.png")
