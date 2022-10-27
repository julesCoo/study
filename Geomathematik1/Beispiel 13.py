from lib import Point, Line, Angle, Plot, HA2, gon, HA1

P1 = Point(12.76, -10.98)
P2 = Point(-22.04, 15.21)
P3 = Point(8.21, 18.41)

s2n = 32.48

# TODO: finde Pn
# N liegt auf P1-P3, zwischen 1 und 3

p = Plot(Point(-25, -25), Point(25, 25))
p.add_point(P1, "P1")
p.add_point(P2, "P2")
p.add_point(P3, "P3")
p.add_circle(P2, s2n)
p.add_line(Line.from_points(P1, P3))
p.save("Geomathematik1/Beispiel 13.png")
