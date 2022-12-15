import math
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple
from lib2d.Point import Point
from lib.Angle import Angle, rad, gon


# Aus einem Punkt, einer Richtung und einer Länge, ergibt den nächsten Punkt
def HA1(
    P: Point,
    s: float,
    v: Angle,
) -> Point:
    return Point(
        P.x + s * v.cos(),
        P.y + s * v.sin(),
    )


# Aus zwei Punkten, ergibt die Länge und die Richtung des Verbindungsvektors
def HA2(
    A: Point,
    B: Point,
) -> Tuple[float, Angle]:
    dist = A.distance_to(B)
    angle = A.oriented_angle_to(B)
    return dist, angle


# Aus 3 Längen eines Dreiecks, ergibt die 3 (gegenüberliegenden) Winkel dieses Dreiecks
def Halbwinkelsatz(
    a: float,
    b: float,
    c: float,
) -> Tuple[Angle, Angle, Angle]:
    s = (a + b + c) / 2
    alpha = rad(2 * math.atan(math.sqrt((s - b) * (s - c) / (s * (s - a)))))
    beta = rad(2 * math.atan(math.sqrt((s - c) * (s - a) / (s * (s - b)))))
    gamma = rad(2 * math.atan(math.sqrt((s - a) * (s - b) / (s * (s - c)))))
    return (alpha, beta, gamma)


# Aus zwei Punkten (A, B) und den Längen ausgehend von diesen Punkten,
# ergibt den Schnittpunkt (C) zweier Kreise mit diesen Radien.
# Achtung: ABC ist im Uhrzeigersinn. Tauscht man A und B, gäbe es noch eine andere Lösung.
def Bogenschnitt(
    A: Point,
    B: Point,
    sAC: float,
    sBC: float,
) -> Point:
    sAB, vAB = HA2(A, B)
    alpha, beta, gamma = Halbwinkelsatz(sBC, sAC, sAB)

    vAC = vAB + alpha
    C = HA1(A, sAC, vAC)

    # Alternativ:
    # vBC = vAB + (gon(200) - beta)
    # C = HA1(B, sBC, vBC)

    return C


# Aus zwei Punkten und den orientierten Richtungen ausgehend von diesen Punkten, ergibt
# den Schnittpunkt dieser Geraden.
def Vorwärtsschnitt_Richtung(
    A: Point,
    B: Point,
    vAC: Angle,
    vBC: Angle,
) -> Point:
    sAB, vAB = HA2(A, B)

    sAC = sAB * (vBC - vAB).sin() / (vBC - vAC).sin()
    C = HA1(A, sAC, vAC)

    # Alternative:
    # sBC = sAB * (vAC - vAB).sin() / (vBC - vAC).sin()
    # C = HA1(B, sBC, vBC)

    return C


# Aus zwei Punkten und den unorientierten Richtungen ausgehend von diesen Punkten, ergibt
# den Schnittpunkt C dieser Geraden.
# A, B, C sind im Uhrzeigersinn.
def Vorwärtsschnitt_Winkel(
    A: Point,
    B: Point,
    alpha: Angle,
    beta: Angle,
) -> Point:
    sAB, vAB = HA2(A, B)

    sAC = sAB * beta.sin() / (alpha + beta).sin()
    vAC = vAB + alpha
    C = HA1(A, sAC, vAC)

    # Alternative:
    # sBC = sAB * alpha.sin() / (alpha + beta).sin()
    # vBC = vAB + (gon(200) - beta)
    # C = HA1(B, sBC, vBC)
    return C


# Aus 3 Punkten (L, M, R), und zwei Winkeln von N zu den drei Punkten,
# berechne den Punkt N.
def Rückwärtsschnitt(
    L: Point,
    M: Point,
    R: Point,
    rNL: Angle,
    rNM: Angle,
    rNR: Angle,
) -> Point:
    alpha = rNM - rNL
    beta = rNR - rNM

    sML, vML = HA2(M, L)
    sMR, vMR = HA2(M, R)

    a = alpha.sin() / sML
    b = -beta.sin() / sMR

    va = vMR - beta
    vb = vML + alpha
    base = (vML - vMR + alpha + beta).sin()
    gamma = (a * va.cos() - b * vb.cos()) / base
    mu = (a * va.sin() - b * vb.sin()) / base

    sMN_sq = 1 / (gamma**2 + mu**2)

    return Point(
        M.x + sMN_sq * gamma,
        M.y + sMN_sq * mu,
    )


# Peripheriewinkelsatz!!
def Rückwärtsschnitt_Collins(
    L: Point,
    M: Point,
    R: Point,
    rNL: Angle,
    rNM: Angle,
    rNR: Angle,
) -> Point:
    alpha = rNM - rNL
    beta = rNR - rNM

    H = Vorwärtsschnitt_Winkel(R, L, alpha, beta)
    sHL, vHL = HA2(H, L)
    sHM, vHM = HA2(H, M)
    sHR, vHR = HA2(H, R)

    gamma = vHM - vHR
    delta = vHL - vHM

    N = Vorwärtsschnitt_Winkel(L, R, gamma, delta)
    return N


@dataclass
class CoordinateTransformation:
    scale: float
    rotation: Angle
    translation: Point

    def __str__(self) -> str:
        return f"scale={self.scale}, rotation={self.rotation}, translation={self.translation}"

    def transform(self, point: Point) -> Point:
        point = point - self.translation
        point = point * self.scale

        point = Point(
            point.x * self.rotation.cos() - point.y * self.rotation.sin(),
            point.x * self.rotation.sin() + point.y * self.rotation.cos(),
        )

        return point


# Given a pair of points in the coordinate system 1, and a pair of points in the coordinate system 2,
# returns the transformation from cs1 -> cs2.
def HelmertTransform(
    points_cs1: Tuple[Point, Point],
    points_cs2: Tuple[Point, Point],
) -> CoordinateTransformation:
    x1 = points_cs1[0].x
    y1 = points_cs1[0].y
    x2 = points_cs1[1].x
    y2 = points_cs1[1].y
    x1_ = points_cs2[0].x
    y1_ = points_cs2[0].y
    x2_ = points_cs2[1].x
    y2_ = points_cs2[1].y

    [a, b, c, d] = np.linalg.solve(
        [
            [x1_, -y1_, 1, 0],
            [y1_, x1_, 0, 1],
            [x2_, -y2_, 1, 0],
            [y2_, x2_, 0, 1],
        ],
        [x1, y1, x2, y2],
    )

    mu = 1 / (a**2 + b**2) ** 0.5
    phi = math.acos(a * mu)
    dx = c
    dy = d

    return CoordinateTransformation(
        scale=mu,
        rotation=rad(phi),
        translation=Point(dx, dy),
    )
