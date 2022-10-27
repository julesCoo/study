from __future__ import annotations
from lib import Point, Line, Angle, Plot, HA2, gon, HA1

A = Point(-94.10, -85.66)
B = Point(120.95, 115.25)
C = Point(38.14, 151.63)

nuAB, sAB = HA2(A, B)
nuBC, sBC = HA2(B, C)

nuBA = nuAB.reverse()

# Satz des Thales
gamma = gon(100)

# Beta zwischen BA und BA
beta = nuBA - nuBC

# Delta von Winkelsumme
delta = gon(200) - gamma - beta

# Sinussatz:
# sBD / sBC = sin(gamma) / sin(delta)
sBD = sBC * gamma.sin() / delta.sin()

# M ist die Mitte zwischen B und D
sBM = sBD / 2

# M und D liegen auf der Gerade AB
nuBD = nuBA
nuBM = nuBA

D = HA1(B, nuBD, sBD)
M = HA1(B, nuBM, sBM)

p = Plot(Point(-200, -200), Point(200, 200))
p.add_point(A, "A")
p.add_point(B, "B")
p.add_point(C, "C")
p.add_point(M, "M")
p.add_point(D, "D")
p.add_line(Line.from_points(A, B))
p.add_circle(M, M.distance_to(D))
p.save("Geomathematik1/Beispiel 6.png")


print("nuAB =", nuAB)
print("nuBC =", nuBC)
print("nuBA =", nuBA)
print("nuBD =", nuBD)
print("nuBM =", nuBM)
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
