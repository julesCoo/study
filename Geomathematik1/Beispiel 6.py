from lib.Circle import Circle
from lib.Point import Point
from lib.Line import Line
from lib.Angle import Angle, gon
from lib.Plot import Plot
from lib.Algorithms import HA1, HA2

A = Point(-94.10, -85.66)
B = Point(120.95, 115.25)
C = Point(38.14, 151.63)

sAB, vAB = HA2(A, B)
sBC, vBC = HA2(B, C)

vBA = vAB.flip()

# Satz des Thales
gamma = gon(100)

# Beta zwischen BA und BA
beta = vBA - vBC

# Delta von Winkelsumme
delta = gon(200) - gamma - beta

# Sinussatz:
# sBD / sBC = sin(gamma) / sin(delta)
sBD = sBC * gamma.sin() / delta.sin()

# M ist die Mitte zwischen B und D
sBM = sBD / 2

# M und D liegen auf der Gerade AB
vBD = vBA
vBM = vBA

D = HA1(B, vBD, sBD)
M = HA1(B, vBM, sBM)

p = Plot(Point(-200, -200), Point(200, 200))
p.add_point(A, "A")
p.add_point(B, "B")
p.add_point(C, "C")
p.add_point(M, "M")
p.add_point(D, "D")
p.add_line(Line.from_points(A, B))
p.add_circle(Circle(M, M.distance_to(D)))
p.save("Geomathematik1/Beispiel 6.png")


print("vAB =", vAB)
print("vBC =", vBC)
print("vBA =", vBA)
print("vBD =", vBD)
print("vBM =", vBM)
print("sAB =", sAB)
print("sBC =", sBC)
print("sBD =", sBD)
print("sBM =", sBM)
print("D =", D)
print("M =", M)

print("Sanity check...")
print(M.distance_to(D))
print(M.distance_to(B))
print(M.distance_to(C))
