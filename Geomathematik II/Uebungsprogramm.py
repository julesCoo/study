"""
Name:
Mat.Nr.:
UEBUNGSPROGRAMM: Geomathematik II, SS2023
Angabe Nr.: 16
HAUPTAUFGABE AUF ALLGEMEINER FLÄCHE
Eine Person befindet sich an einem Punkt (phi,lambda) im Stadtgebiet von Graz
und bewegt sich auf der kürzesten Strecke mit der Distanz s unter dem Azimut alp
fort. Die Bewegung wird hierbei vereinfacht auf einem Rotationsellipsoid (Rotati
dritte Achse) mit den Halbachsen a und b modelliert.
Wählen Sie zur Parameterdarstellung des Rotationsellipsoids die reduzierte Breit
(beta) und entwickeln Sie die geodätische Linie in eine McLaurin Reihe bis zum
vierten Glied (für beta und lambda) und in eine bis zum dritten Glied (für alpha
phi: 47° 4' 39''
lambda: 15° 28' 53''
alpha: 50.90°
s: 229360 m
Referenzellipsoid WGS84 [m]: a = 6378137, b = 6356752.3142
a) Berechnen Sie die Endposition in phi [DMS] und lambda [DMS] und das Azimut [D
Ziel der Person mit den gegebenen Werten.
b) Welchen Fehler in den Koordinaten begeht man, wenn nur die ersten 3 Reihengli
berechnet werden? Geben Sie die Differenz in Sekunden an!
Tipp: tan(beta) = b/a * tan(phi)
ALLGEMEINES:
a) Berechnung mit Zwischenergebnissen (bei Winkel in Bogenmaß) und
durchgreifenden Kontrollen;
b) Dokumentation (inkl. ev. Programmcode) ausreichend und in sorgfältiger Form;
c) Abgabe am 26.06.2023 mit muendlicher Stellungnahme;
"""

# %%
"Imports and helpers"
from sympy import *
from lib import *
from math import pi
import matplotlib.pyplot as plt


def dms(d, m, s):
    "Takes an angle in DMS notation and converts it to radians."
    return (d + m / 60 + s / 3600) * pi / 180


# %%
"Visualisation of different ellipsoids"

phi, lamda, beta = symbols("phi lambda beta", real=True)
a, b = symbols("a b", real=True, positive=True)

X = Matrix(
    [
        a * cos(beta) * cos(lamda),
        a * cos(beta) * sin(lamda),
        b * sin(beta),
    ]
)

# Erste Ableitungen der Parameterlinien (Tangentenvektoren)
X_beta = diff(X, beta)
X_lamda = diff(X, lamda)

# Erste Fundamentalform (Innere Geometrie)
E = X_beta.dot(X_beta)
E = E.replace(sin(lamda) ** 2, 1 - cos(lamda) ** 2).expand()
F = X_beta.dot(X_lamda)
G = X_lamda.dot(X_lamda)


# Ableitungen der Metrik
E_lamda = diff(E, lamda)
G_beta = diff(G, beta)

# %%
"Wird nicht benötigt"


# Flächennormalenvektor
z = X_beta.cross(X_lamda)
z[2] = z[2].factor().replace(sin(lamda) ** 2 + cos(lamda) ** 2, 1)
zz = z.dot(z)
zz = zz.replace(sin(lamda) ** 2, 1 - cos(lamda) ** 2).expand()
z_norm = sqrt(zz)
z = z / z_norm

# Zweite Ableitungen der Parameterlinien (Krümmungsvektoren)
X_beta_beta = diff(X_beta, beta)
X_beta_lamda = diff(X_beta, lamda)
X_lamda_lamda = diff(X_lamda, lamda)

# Zweite Fundamentalform (Äußere Geometrie)
L = X_beta_beta.dot(z)
M = X_beta_lamda.dot(z)
N = X_lamda_lamda.dot(z)
# %%
