import math
from typing import Optional, Tuple
from lib2d.Point import Point
from lib2d.Angle import Angle, rad, gon


# Aus einem Punkt, einer Richtung und einer Länge, ergibt den nächsten Punkt
def HA1(P: Point, v: Angle, s: float) -> Point:
    return Point(
        P.x + s * v.cos(),
        P.y + s * v.sin(),
    )


# Aus zwei Punkten, ergibt die Länge und die Richtung des Verbindungsvektors
def HA2(A: Point, B: Point) -> Tuple[float, Angle]:
    dist = A.distance_to(B)
    angle = A.oriented_angle_to(B)
    return dist, angle


# Aus 3 Längen eines Dreiecks, ergibt die 3 (gegenüberliegenden) Winkel dieses Dreiecks
def Halbwinkelsatz(a: float, b: float, c: float) -> Tuple[Angle, Angle, Angle]:
    s = (a + b + c) / 2
    alpha = rad(2 * math.atan(math.sqrt((s - b) * (s - c) / (s * (s - a)))))
    beta = rad(2 * math.atan(math.sqrt((s - c) * (s - a) / (s * (s - b)))))
    gamma = rad(2 * math.atan(math.sqrt((s - a) * (s - b) / (s * (s - c)))))
    return (alpha, beta, gamma)


# Aus zwei Punkten (A, B) und den Längen ausgehend von diesen Punkten,
# ergibt den Schnittpunkt (C) zweier Kreise mit diesen Radien.
# Achtung: ABC ist im Uhrzeigersinn. Tauscht man A und B, gäbe es noch eine andere Lösung.
def Bogenschnitt(A: Point, B: Point, sAC: float, sBC: float) -> Point:
    sAB, vAB = HA2(A, B)
    alpha, beta, gamma = Halbwinkelsatz(sBC, sAC, sAB)

    vAC = vAB + alpha
    C = HA1(A, vAC, sAC)

    # Alternativ:
    # vBC = vAB + (gon(200) - beta)
    # C = HA1(B, vBC, sBC)

    return C


# Aus zwei Punkten und den orientierten Richtungen ausgehend von diesen Punkten, ergibt
# den Schnittpunkt dieser Geraden.
def Vorwärtsschnitt_Richtung(A: Point, B: Point, vAC: Angle, vBC: Angle) -> Point:
    sAB, vAB = HA2(A, B)

    sAC = sAB * (vBC - vAB).sin() / (vBC - vAC).sin()
    C = HA1(A, vAC, sAC)

    # Alternative:
    # sBC = sAB * (vAC - vAB).sin() / (vBC - vAC).sin()
    # C = HA1(B, vBC, sBC)

    return C


def Koordinatentransformation(
    point: Point,
    scale: Optional[float] = None,
    rotation: Optional[Angle] = None,
    translation: Optional[Point] = None,
) -> Point:
    if scale is not None:
        point = Point(point.x * scale, point.y * scale)
    if rotation is not None:
        point = Point(
            point.x * rotation.cos() - point.y * rotation.sin(),
            point.x * rotation.sin() + point.y * rotation.cos(),
        )
    if translation is not None:
        point = Point(point.x + translation.x, point.y + translation.y)

    return point


"""
Drehung in 3D:
    Ortsvektor: x
    Drehachse: omega
        Drehachse normalisieren!
    Drehwinkel: alpha
    Drehmatrix: R

    Berechnung der Drehmatrix:
        Projektionsmatrix: PI = omega * omega^T (dyadische Multiplikation)

        Projizierung von x auf die Drehachse: 



"""
