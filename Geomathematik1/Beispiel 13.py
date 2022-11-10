from lib2d.Circle import Circle
from lib2d.Point import Point
from lib2d.Line import Line
from lib2d.Angle import Angle, gon
from lib2d.Plot import Plot
from lib2d.Algorithms import HA1, HA2

P1 = Point(12.76, -10.98)
P2 = Point(-22.04, 15.21)
P3 = Point(8.21, 18.41)

s2n = 32.48

circle = Circle(P2, s2n)
line = Line.from_points(P1, P3)

# Pn liegt auf P1-P3, zwischen 1 und 3
Pn1, Pn2 = circle.intersect_line(line)
Pn = Pn2

p = Plot(Point(-50, -50), Point(50, 50))
p.add_point(P1, "P1")
p.add_point(P2, "P2")
p.add_point(P3, "P3")
p.add_circle(circle)
p.add_line(line)
p.add_point(Pn, "Pn")
p.save("Geomathematik1/Beispiel 13.png")

print("Pn =", Pn)
