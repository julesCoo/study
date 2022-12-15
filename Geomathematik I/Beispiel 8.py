from lib2d.Point import Point
from lib2d.Line import Line
from lib.Angle import Angle, gon
from lib2d.Plot import Plot
from lib2d.Algorithms import HA1, HA2

P1 = Point(12.21, -11.35)
P2 = Point(5.20, 40.93)
P3 = Point(-21.64, 15.27)

v3n = gon(23.2456)

line3N = Line(P3, v3n)
line12 = Line.from_points(P1, P2)

Pn = line3N.intersection(line12)

p = Plot(Point(-50, -50), Point(50, 50))
p.add_point(P1, "P1")
p.add_point(P2, "P2")
p.add_point(P3, "P3")
p.add_line(line3N)
p.add_line(line12)
p.add_point(Pn, "Pn")
p.save("Geomathematik1/Beispiel 8.png")

print("Pn =", Pn)
