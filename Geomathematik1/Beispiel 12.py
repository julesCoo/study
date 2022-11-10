from lib2d.Point import Point
from lib2d.Line import Line
from lib2d.Circle import Circle
from lib2d.Angle import Angle, gon
from lib2d.Plot import Plot
from lib2d.Algorithms import HA1, HA2, Bogenschnitt

A = Point(2825.31, 4538.20)
B = Point(2887.49, 4561.47)

sA1 = 47.43
sA2 = 57.54

sB1 = 53.95
sB2 = 46.09

# A,N1,B,N2 im Uhrzeigersinn!
N1 = Bogenschnitt(B, A, sB1, sA1)
N2 = Bogenschnitt(A, B, sA2, sB2)

p = Plot(Point(2700, 4400), Point(3000, 4700))
p.add_point(A, "A")
p.add_point(B, "B")
p.add_circle(Circle(A, sA1))
p.add_circle(Circle(A, sA2))
p.add_circle(Circle(B, sB1))
p.add_circle(Circle(B, sB2))
p.add_point(N1, "N1")
p.add_point(N2, "N2")
p.save("Geomathematik1/Beispiel 12.png")

print("N1 =", N1)
print("N2 =", N2)
