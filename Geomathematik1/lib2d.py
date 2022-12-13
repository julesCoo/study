from __future__ import annotations
from math import acos, atan2, sqrt, cos, sin, atan
from typing import Tuple

import numpy as np


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f})"

    def distance_to(self, other: Point) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def oriented_angle_to(self, other: Point) -> float:
        return atan2(other.y - self.y, other.x - self.x)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scale: float) -> Point:
        return Point(self.x * scale, self.y * scale)

    def ha1(self, s: float, v: float):
        return Point(
            self.x + s * cos(v),
            self.y + s * sin(v),
        )

    def ha2(self, other: Point):
        s = self.distance_to(other)
        v = self.oriented_angle_to(other)
        return s, v


# Aus 3 Längen eines Dreiecks, ergibt die 3 (gegenüberliegenden) Winkel dieses Dreiecks
def Halbwinkelsatz(
    a: float,
    b: float,
    c: float,
):
    s = (a + b + c) / 2
    alpha = 2 * atan(sqrt((s - b) * (s - c) / (s * (s - a))))
    beta = 2 * atan(sqrt((s - c) * (s - a) / (s * (s - b))))
    gamma = 2 * atan(sqrt((s - a) * (s - b) / (s * (s - c))))
    return alpha, beta, gamma


# Bogenschnitt
# Aus zwei Punkten (A, B) und den Längen ausgehend von diesen Punkten,
# ergibt den Schnittpunkt (C) zweier Kreise mit diesen Radien.
# Achtung: ABC ist im Uhrzeigersinn. Tauscht man A und B, gäbe es noch eine andere Lösung.
def Bogenschnitt(
    A: Point,
    B: Point,
    sAC: float,
    sBC: float,
) -> Point:
    sAB, vAB = A.ha2(B)
    alpha, beta, gamma = Halbwinkelsatz(sBC, sAC, sAB)

    vAC = vAB + alpha
    C = A.ha1(sAC, vAC)

    # Alternativ:
    # vBC = vAB + (gon(200) - beta)
    # C = B.ha1(sBC, vBC)

    return C


# Aus zwei Punkten und den orientierten Richtungen ausgehend von diesen Punkten, ergibt
# den Schnittpunkt dieser Geraden.
def Vorwärtsschnitt_Richtung(
    A: Point,
    B: Point,
    vAC: float,
    vBC: float,
) -> Point:
    sAB, vAB = A.ha2(B)

    sAC = sAB * sin(vBC - vAB) / sin(vBC - vAC)
    C = A.ha1(sAC, vAC)

    # Alternative:
    # sBC = sAB * sin(vAC - vAB) / sin(vBC - vAC)
    # C = B.ha1(sBC, vBC)

    return C


# Aus zwei Punkten und den unorientierten Richtungen ausgehend von diesen Punkten, ergibt
# den Schnittpunkt C dieser Geraden.
# A, B, C sind im Uhrzeigersinn.
def Vorwärtsschnitt_Winkel(
    A: Point,
    B: Point,
    alpha: float,
    beta: float,
) -> Point:

    sAB, vAB = A.ha2(B)
    sAC = sAB * sin(beta) / sin(alpha + beta)
    sBC = sAB * sin(alpha) / sin(alpha + beta)

    vAC = vAB + alpha
    C = A.ha1(sAC, vAC)

    # Alternative:
    # vBC = vAB + (pi - beta)
    # C = B.ha1(sBC, vBC)

    return C


# Aus 3 Punkten (L, M, R), und zwei Winkeln von N zu den drei Punkten,
# berechne den Punkt N.
def Rückwärtsschnitt(
    L: Point,
    M: Point,
    R: Point,
    rNL: float,
    rNM: float,
    rNR: float,
) -> Point:
    alpha = rNM - rNL
    beta = rNR - rNM

    sML, vML = M.ha2(L)
    sMR, vMR = M.ha2(R)

    a = sin(alpha) / sML
    b = sin(-beta) / sMR

    va = vMR - beta
    vb = vML + alpha
    base = sin(vML - vMR + alpha + beta)
    gamma = (a * cos(va) - b * cos(vb)) / base
    mu = (a * sin(va) - b * sin(vb)) / base

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
    rNL: float,
    rNM: float,
    rNR: float,
) -> Point:
    alpha = rNM - rNL
    beta = rNR - rNM

    H = Vorwärtsschnitt_Winkel(R, L, alpha, beta)
    sHL, vHL = H.ha2(L)
    sHM, vHM = H.ha2(M)
    sHR, vHR = H.ha2(R)

    gamma = vHM - vHR
    delta = vHL - vHM

    N = Vorwärtsschnitt_Winkel(L, R, gamma, delta)
    return N


class CoordinateTransformation:
    scale: float
    rotation: float
    translation: Point

    def __str__(self) -> str:
        return f"scale={self.scale}, rotation={self.rotation}, translation={self.translation}"

    def transform(self, point: Point) -> Point:
        point = point - self.translation
        point = point * self.scale

        point = Point(
            point.x * cos(self.rotation) - point.y * sin(self.rotation),
            point.x * sin(self.rotation) + point.y * cos(self.rotation),
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
    phi = acos(a * mu)
    dx = c
    dy = d

    return CoordinateTransformation(
        scale=mu,
        rotation=phi,
        translation=Point(dx, dy),
    )
