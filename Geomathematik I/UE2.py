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

from math import degrees, tau

import numpy as np
from libgeo import from_deg, clamp_rad
from libsphere import (
    SphereCoords,
    SphereTriangle,
    ha1,
    ha2,
    plot_angle,
    plot_azimuth,
    plot_circle,
    plot_line,
    plot_point,
    vws,
)

earth_radius = 6385530

P1 = SphereCoords(from_deg(57, 13, 24.56), from_deg(-2, 4, 40.76))
P2 = SphereCoords(from_deg(58, 23, 23.12), from_deg(6, 5, 29.66))
P3 = SphereCoords(from_deg(52, 54, 24.94), from_deg(4, 42, 34.09))

s1N = 289520.40 / earth_radius
s3N = 427888.35 / earth_radius
a2N = from_deg(227, 1, 54.37)
a3N = from_deg(340, 59, 4.21)

s12, a12, a21 = ha2(P1, P2)
s23, a23, a32 = ha2(P2, P3)
s31, a31, a13 = ha2(P3, P1)


w2N1 = clamp_rad(a21 - a2N)
w23N = clamp_rad(a2N - a23)
w3N2 = clamp_rad(a32 - a3N)
w31N = clamp_rad(a3N - a31)

solutions = []

# I
for T in SphereTriangle.ssw(a=s1N, c=s12, alpha=w2N1):
    solutions.append(
        (
            (s1N, s12, w2N1),
            ha1(P1, s1N, a12 + T.beta)[0],
            ha1(P2, T.b, a21 - T.alpha)[0],
        )
    )

# II
for T in SphereTriangle.ssw(a=s3N, c=s23, alpha=w23N):
    solutions.append(
        (
            (s3N, s23, w23N),
            ha1(P2, T.b, a23 + T.alpha)[0],
            ha1(P3, s3N, a32 - T.beta)[0],
        )
    )

# III
T = SphereTriangle.sws(a=s23, b=s3N, gamma=w3N2)
solutions.append(
    (
        (s3N, s23, w3N2),
        ha1(P2, T.c, a23 + T.beta)[0],
        ha1(P3, T.b, a32 - T.gamma)[0],
    )
)

# IV
T = SphereTriangle.wsw(alpha=w23N, beta=w3N2, c=s23)
solutions.append(
    (
        (s23, w23N, w3N2),
        ha1(P2, T.b, a23 + T.alpha)[0],
        ha1(P3, T.a, a32 - T.beta)[0],
    )
)

# V
T = SphereTriangle.sss(a=s1N, b=s3N, c=s31)
solutions.append(
    (
        (s1N, s3N, s31),
        ha1(P1, T.a, a13 - T.beta)[0],
        ha1(P3, T.b, a31 + T.alpha)[0],
    )
)

# VI
for T in SphereTriangle.ssw(a=s1N, c=s31, alpha=w31N):
    solutions.append(
        (
            (s1N, s31, w31N),
            ha1(P1, T.a, a13 - T.beta)[0],
            ha1(P3, T.b, a31 + T.alpha)[0],
        )
    )

# VII
T = SphereTriangle.sws(a=s3N, b=s31, gamma=w31N)
solutions.append(
    (
        (s3N, s31, w31N),
        ha1(P1, T.c, a13 - T.alpha)[0],
        ha1(P3, T.a, a31 + T.gamma)[0],
    )
)

# VIII
for T in SphereTriangle.ssw(a=s1N, c=s3N, alpha=w31N):
    solutions.append(
        (
            (s1N, s3N, w31N),
            ha1(P1, T.a, a13 - T.gamma)[0],
            ha1(P3, T.c, a31 + T.alpha)[0],
        )
    )

# IX
for T in SphereTriangle.wws(alpha=w23N, gamma=w3N2, a=s3N):
    solutions.append(
        (
            (s3N, w23N, w3N2),
            ha1(P2, T.c, a23 + T.alpha)[0],
            ha1(P3, T.a, a32 - T.gamma)[0],
        )
    )


coordinates = []
for inputs, p1, p2 in solutions:
    if s3N in inputs:
        continue
    coordinates.append(p1)
    coordinates.append(p2)

# get the median phi and lam of coordinats
phi = np.median([p.phi for p in coordinates])
lam = np.median([p.lam for p in coordinates])
centroid = SphereCoords(phi, lam)
distances = [p.geodesic_distance_to(centroid) for p in coordinates]

N = vws(P2, P3, a2N, a3N)
N = centroid


"""Visualization"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# remove distances > 0.01
distances = [d for d in distances if d < 0.01]

plt.hist(distances, bins=20)
plt.show()
plt.clf()


def add_mercator_subplot(pos, title):
    ax = plt.subplot(pos, projection=ccrs.Mercator())
    ax.set_title(title, fontsize=16)
    ax.set_extent([-3.5, 8, 52, 60], ccrs.PlateCarree())
    ax.set_aspect(1 / 1)
    ax.coastlines(alpha=0.2)
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        xlocs=[0, 4],
        ylocs=[50, 54, 58],
        linewidth=0.25,
    )
    gl.top_labels = False
    gl.right_labels = False
    return ax


plt.figure(figsize=(10, 4))

add_mercator_subplot(131, "Beobachtungen")
plot_azimuth(P2, a2N, 1, color="green")
plot_azimuth(P3, a3N, 1, color="blue")
plot_circle(P1, s1N, color="red")
plot_circle(P3, s3N, color="blue")
plot_point(P1, marker="^", color="red", text="P1")
plot_point(P2, marker="^", color="green", text="P2")
plot_point(P3, marker="^", color="blue", text="P3")

add_mercator_subplot(132, "Dreiecke")
plot_angle(N, P1, P2, color="red")
plot_angle(N, P2, P3, color="red")
plot_angle(N, P3, P1, color="red")
plot_angle(P1, N, P3, color="red")
plot_angle(P1, P2, N, color="red")
plot_angle(P2, N, P1, color="green")
plot_angle(P2, P3, N, color="green")
plot_angle(P3, N, P2, color="green")
plot_angle(P3, P1, N, color="green")
plot_azimuth(P2, a2N, color="green", linewidth=0.5)
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_circle(P1, s1N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(P1, N, color="green")
plot_line(P1, P2, color="green")
plot_line(P2, N, color="red")
plot_line(P2, P3, color="green")
plot_line(P3, N, color="green")
plot_line(P3, P1, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P1, marker="^", color="green", text="P1")
plot_point(P2, marker="^", color="green", text="P2")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(133, "Lösungen")
plot_azimuth(P2, a2N, 1, color="gray", alpha=0.25)
plot_azimuth(P3, a3N, 1, color="gray", alpha=0.25)
plot_circle(P1, s1N, color="gray", alpha=0.25)
plot_circle(P3, s3N, color="gray", alpha=0.25)

for inputs, p1, p2 in solutions:
    if s3N in inputs:
        pass

    for p in (p1, p2):
        plot_point(p, marker="+", color="green", markersize=10, alpha=0.25)

plt.savefig("Übersicht.png", bbox_inches="tight", dpi=300)
plt.clf()

exit()


plt.figure(figsize=(10, 12))

add_mercator_subplot(331, "I")
plot_angle(N, P1, P2, color="red")
plot_angle(P1, P2, N, color="red")
plot_angle(P2, N, P1, color="green")
plot_azimuth(P2, a2N, color="green", linewidth=0.5)
plot_circle(P1, s1N, color="green", linewidth=0.5)
plot_line(N, P1, color="green")
plot_line(P1, P2, color="green")
plot_line(P2, N, color="red")
plot_point(N, marker="o", color="red", text="N")
plot_point(P1, marker="^", color="green", text="P1")
plot_point(P2, marker="^", color="green", text="P2")

add_mercator_subplot(332, "II")
plot_angle(N, P2, P3, color="red")
plot_angle(P2, P3, N, color="green")
plot_angle(P3, N, P2, color="red")
plot_azimuth(P2, a2N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(N, P2, color="red")
plot_line(P2, P3, color="green")
plot_line(P3, N, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P2, marker="^", color="green", text="P2")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(333, "III")
plot_angle(N, P2, P3, color="red")
plot_angle(P2, P3, N, color="red")
plot_angle(P3, N, P2, color="green")
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(N, P2, color="red")
plot_line(P2, P3, color="green")
plot_line(P3, N, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P2, marker="^", color="green", text="P2")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(334, "IV")
plot_angle(N, P2, P3, color="red")
plot_angle(P2, P3, N, color="green")
plot_angle(P3, N, P2, color="green")
plot_azimuth(P2, a2N, color="green", linewidth=0.5)
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_line(N, P2, color="red")
plot_line(P2, P3, color="green")
plot_line(P3, N, color="red")
plot_point(N, marker="o", color="red", text="N")
plot_point(P2, marker="^", color="green", text="P2")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(335, "V")
plot_angle(N, P3, P1, color="red")
plot_angle(P1, N, P3, color="red")
plot_angle(P3, P1, N, color="red")
plot_circle(P1, s1N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(N, P3, color="green")
plot_line(P1, N, color="green")
plot_line(P3, P1, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P1, marker="^", color="green", text="P1")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(336, "VI")
plot_angle(N, P3, P1, color="red")
plot_angle(P1, N, P3, color="red")
plot_angle(P3, P1, N, color="green")
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_circle(P1, s1N, color="green", linewidth=0.5)
plot_line(N, P3, color="red")
plot_line(P1, N, color="green")
plot_line(P3, P1, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P1, marker="^", color="green", text="P1")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(337, "VII")
plot_angle(N, P3, P1, color="red")
plot_angle(P1, N, P3, color="red")
plot_angle(P3, P1, N, color="green")
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(N, P3, color="green")
plot_line(P1, N, color="red")
plot_line(P3, P1, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P1, marker="^", color="green", text="P1")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(338, "VIII")
plot_angle(N, P3, P1, color="red")
plot_angle(P1, N, P3, color="red")
plot_angle(P3, P1, N, color="green")
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_circle(P1, s1N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(N, P3, color="green")
plot_line(P1, N, color="green")
plot_line(P3, P1, color="red")
plot_point(N, marker="o", color="red", text="N")
plot_point(P1, marker="^", color="green", text="P1")
plot_point(P3, marker="^", color="green", text="P3")

add_mercator_subplot(339, "IX")
plot_angle(N, P2, P3, color="red")
plot_angle(P2, P3, N, color="green")
plot_angle(P3, N, P2, color="green")
plot_azimuth(P2, a2N, color="green", linewidth=0.5)
plot_azimuth(P3, a3N, color="green", linewidth=0.5)
plot_circle(P3, s3N, color="green", linewidth=0.5)
plot_line(N, P2, color="red")
plot_line(P2, P3, color="red")
plot_line(P3, N, color="green")
plot_point(N, marker="o", color="red", text="N")
plot_point(P2, marker="^", color="green", text="P2")
plot_point(P3, marker="^", color="green", text="P3")

plt.savefig("Dreiecksauflösung.png", bbox_inches="tight", dpi=300)
