from lib2d.Circle import Circle
from lib2d.Point import Point
from lib2d.Line import Line
from lib2d.Plot import Plot

A = Point(-96.01, -86.86)
B = Point(127.05, 113.75)
C = Point(37.86, 149.26)
D = Point(107.22, -32.01)

lineAB = Line.from_points(A, B)
circleBCD = Circle.from_points(B, C, D)
P1, P2 = circleBCD.intersect_line(lineAB)
E = P2

p = Plot(Point(-200, -200), Point(200, 200))
p.add_line(lineAB)
p.add_circle(circleBCD)
p.add_point(A, "A")
p.add_point(B, "B")
p.add_point(C, "C")
p.add_point(D, "D")
p.add_point(E, "E")
p.save("Geomathematik1/Beispiel 22.png")

print(f"Circle center: {circleBCD.center}")
print(f"E = {E}")


# Kann auch mit Collins gelöst werden
# Andere Übungen: 20-25
