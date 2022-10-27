from lib import Point, Line, Angle, Plot, HA2, gon, HA1

A = Point(2825.31, 4538.20)
B = Point(2887.49, 4561.47)

sA1 = 47.43
sA2 = 57.54

sB1 = 53.95
sB2 = 46.09

# TODO: finde N1 und N2
# A,N1,B,N2 im Uhrzeigersinn!

p = Plot(Point(2700, 4400), Point(3000, 4700))
p.add_point(A, "A")
p.add_point(B, "B")
p.add_circle(A, sA1)
p.add_circle(A, sA2)
p.add_circle(B, sB1)
p.add_circle(B, sB2)
p.save("Geomathematik1/Beispiel 12.png")
