"""
Aus globalen Vermessungen wurden sphaerische Distancen s in [m] und 
Azimute a in [Grad,Minuten,Sekunden] von drei Festpunkten in der
Naehe von Aberdeen/Schottland, Egersund/Norwegen bzw DenHelder/Holland
zu einer Bohrinsel in der Nordsee (N) abgeleitet. Eine (nur eine!) der
Beobachtungen stellt sich in Relation zu den anderen als grob falsch
heraus.
Durch rechnerische Feststellung und Ausscheiden der falschen Beobachtung
sind die geographischen Koordinaten der Bohrinsel in [Grad,Minuten,Sekunden]
durch Einschneideverfahren in allen gueltigen Kombinationen und einer
anschliessenden Mittelbildung zu bestimmen. Den sphaerischen Berechnungen
ist ein Kugelradius von 6385530 m zugrunde zu legen.

Ausgangskoordinaten: [Grad,Minuten,Sekunden]
P1-Aberdeen:  phi=(57,13,24.56), lambda=( 2, 4,40.76)
P2-Egersund:  phi=(58,23,23.12), lambda=( 6, 5,29.66)
P3-DenHelder: phi=(52,54,24.94), lambda=( 4,42,34.09)

Beobachtungen: [m] bzw. [Grad,Minuten,Sekunden]
s1N= 289520.40
s3N= 427888.35
a2N= (227, 1,54.37)
a3N= (340,59, 4.21)

ALLGEMEINES:

a) Berechnung mit Zwischenergebnissen und durchgreifenden Kontrollen;
b) Dokumentation ausreichend und in sorgfaeltiger Form;
c) Abgabe am 26.1.2023, mit muendlicher Stellungnahme;
d) Abgabe in Umschlagblatt.
"""


from math import radians
from libgeo import from_deg
from libsphere import SphereCoords, SphereTriangle, bgs, ha1, vws, SpherePlot

earth_radius = 6385530

P1 = SphereCoords(from_deg(57, 13, 24.56), from_deg(-2, 4, 40.76))
P2 = SphereCoords(from_deg(58, 23, 23.12), from_deg(6, 5, 29.66))
P3 = SphereCoords(from_deg(52, 54, 24.94), from_deg(4, 42, 34.09))

s1N = 289520.40 / earth_radius
s3N = 427888.35 / earth_radius
a2N = from_deg(227, 1, 54.37)
a3N = from_deg(340, 59, 4.21)

N = bgs(P1, P3, s1N, s3N)

"""
Visualization
"""

plot = SpherePlot(
    # SphereCoords(from_deg(48), from_deg(-8)),
    # SphereCoords(from_deg(62), from_deg(12)),
    ha1(N, 0.002, radians(315))[0],
    ha1(N, 0.002, radians(135))[0],
)


plot.circle(P1, s1N, color="red")
plot.circle(P3, s3N, color="blue")
plot.azimuth(P2, a2N, 1, color="green")
plot.azimuth(P3, a3N, 1, color="blue")

plot.point(P1, marker="^", color="red")
plot.point(P2, marker="^", color="green")
plot.point(P3, marker="^", color="blue")

plot.show()
