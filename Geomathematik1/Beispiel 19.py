from lib2d.Segment import Segment
from lib2d.Circle import Circle
from lib2d.Point import Point
from lib2d.Line import Line
from lib.Angle import Angle, gon
from lib2d.Plot import Plot
from lib2d.Algorithms import HA1, HA2, Rückwärtsschnitt

L = Point(1116.01, 900.16)
M = Point(522.89, 801.57)
R = Point(230.53, 350.13)

# unorientierte Richtungen
wNL = gon(0)
wNM = gon(121.6816)
wNR = gon(165.8394)

N = Rückwärtsschnitt(L, M, R, wNL, wNM, wNR)

p = Plot(Point(0, 0), Point(1200, 1000))
p.add_segment(Segment.from_points(N, L))
p.add_segment(Segment.from_points(N, M))
p.add_segment(Segment.from_points(N, R))
p.add_point(L, "L")
p.add_point(M, "M")
p.add_point(R, "R")
p.add_point(N, "N")
p.save("Geomathematik1/Beispiel 19.png")

print("N =", N)
