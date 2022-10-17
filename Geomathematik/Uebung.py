from Coordinates import *

A = CartesianCoordinate(9.64, 40.24)
B = CartesianCoordinate(32.69, 22.25)

P1 = Segment(A, B).rotate(gon(152.236 - 75.235)).setLength(62.24).endCoord
P2 = Segment(P1, A).rotate(gon(122.901)).setLength(46.35).endCoord

print(P1)
print(P2)
