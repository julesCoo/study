from __future__ import annotations
from dataclasses import dataclass
from math import asin, atan2, cos, degrees, radians, sin, pi, sqrt, atan, tau
from lib3d import Vec3
from libgeo import fmt_deg_str, clamp_rad


def _cosineRuleForSides(a: float, b: float, gamma: float):
    """
    Cosine rule for sides

    Given 2 sides of a spheric triangle, and the angle between them, calculate the third side.
    """
    return 2 * atan(
        sqrt(sin((a - b) / 2) ** 2 + sin(a) * sin(b) * sin(gamma / 2) ** 2)
        / sqrt(cos((a + b) / 2) ** 2 + sin(a) * sin(b) * cos(gamma / 2) ** 2)
    )


def _cosineRuleForAngles(c: float, alpha: float, beta: float):
    """
    Cosine rule for angles

    Given a side of a spheric triangle, and the two angles on this side, calculate the third angle.
    """
    return 2 * atan(
        sqrt(cos((alpha + beta) / 2) ** 2 + sin(alpha) * sin(beta) * sin(c / 2) ** 2)
        / sqrt(sin((alpha - beta) / 2) ** 2 + sin(alpha) * sin(beta) * cos(c / 2) ** 2)
    )


def _halfSideFormula(alpha: float, beta: float, gamma: float):
    """
    Half-side formula

    Given 3 angles of a spheric triangle, calculate the sides between them.
    """
    rho = (alpha + beta + gamma) / 2
    cr = cos(rho)
    cra = cos(rho - alpha)
    crb = cos(rho - beta)
    crg = cos(rho - gamma)
    a = 2 * atan(1 / sqrt(crb * crg / (-cr * cra)))
    b = 2 * atan(1 / sqrt(cra * crg / (-cr * crb)))
    c = 2 * atan(1 / sqrt(cra * crb / (-cr * crg)))
    return a, b, c


def _halfAngleFormula(a: float, b: float, c: float):
    """
    Half-angle formula

    Given 3 sides of a spheric triangle, calculate the angles between them.
    """
    s = (a + b + c) / 2
    if a > s or b > s or c > s:
        raise ValueError(
            "Triangle inequality violated: One side is longer than the other two combined!"
        )

    ss = sin(s)
    ssa = sin(s - a)
    ssb = sin(s - b)
    ssc = sin(s - c)

    if ssa == 0:
        alpha = pi
    else:
        alpha = 2 * atan(sqrt(ssb * ssc / (ss * ssa)))

    if ssb == 0:
        beta = pi
    else:
        beta = 2 * atan(sqrt(ssa * ssc / (ss * ssb)))

    if ssc == 0:
        gamma = pi
    else:
        gamma = 2 * atan(sqrt(ssa * ssb / (ss * ssc)))

    return alpha, beta, gamma


def _helper(a: float, c: float, alpha: float, gamma: float):
    """
    Unnamed helper method

    Given two sides and two angles, calculate the third angle.
    """
    return 2 * atan(
        sqrt(sin((a - c) / 2) ** 2 + sin(a) * sin(c) * cos((alpha + gamma) / 2) ** 2)
        / sqrt(cos((a + c) / 2) ** 2 + sin(a) * sin(c) * sin((alpha - gamma) / 2) ** 2)
    )


# A spherical triangle is created from the intersection of 3 great circles
# on a unit sphere. All angles and sides are given in radians.
@dataclass
class SphereTriangle:
    a: float
    b: float
    c: float
    alpha: float
    beta: float
    gamma: float

    def excess(self) -> float:
        return self.alpha + self.beta + self.gamma - pi

    def area(self, radius=1) -> float:
        return self.excess() * radius**2

    @classmethod
    def ppp(
        SphereTriangle,
        p1: SphereCoords,
        p2: SphereCoords,
        p3: SphereCoords,
    ) -> SphereTriangle:
        a, _, _ = ha2(p1, p2)
        b, _, _ = ha2(p2, p3)
        c, _, _ = ha2(p3, p1)
        return SphereTriangle.sss(a, b, c)

    @classmethod
    def sws(
        SphereTriangle,
        a: float,
        b: float,
        gamma: float,
    ) -> SphereTriangle:
        c = _cosineRuleForSides(a, b, gamma)
        alpha, beta, _ = _halfAngleFormula(a, b, c)
        return SphereTriangle(a, b, c, alpha, beta, gamma)

    @classmethod
    def wsw(
        SphereTriangle,
        alpha: float,
        beta: float,
        c: float,
    ) -> SphereTriangle:
        gamma = _cosineRuleForAngles(c, alpha, beta)
        a, b, _ = _halfSideFormula(alpha, beta, gamma)
        return SphereTriangle(a, b, c, alpha, beta, gamma)

    @classmethod
    def ssw(
        SphereTriangle,
        a: float,
        c: float,
        alpha: float,
    ) -> list[SphereTriangle]:
        solutions = []

        # Half Angle Formula could produce angles that do not match the input.
        # In this case, we need to discard the solution.
        def is_valid(w1, w2):
            return abs(w1 - w2) < 1e-2

        # First solution
        gamma = asin(sin(c) * sin(alpha) / sin(a))
        b = _helper(a, c, alpha, gamma)
        alpha_, beta, gamma_ = _halfAngleFormula(a, b, c)
        if is_valid(alpha, alpha_) and is_valid(gamma, gamma_):
            solutions.append(SphereTriangle(a, b, c, alpha, beta, gamma))

        # Second solution
        gamma = pi - gamma
        b = _helper(a, c, alpha, gamma)
        alpha_, beta, gamma_ = _halfAngleFormula(a, b, c)
        if is_valid(alpha, alpha_) and is_valid(gamma, gamma_):
            solutions.append(SphereTriangle(a, b, c, alpha, beta, gamma))

        return solutions

    @classmethod
    def wws(
        SphereTriangle,
        alpha: float,
        gamma: float,
        a: float,
    ) -> list[SphereTriangle]:
        solutions = []

        # Half Angle Formula could produce angles that do not match the input.
        # In this case, we need to discard the solution.
        def is_valid(w1, w2):
            return abs(w1 - w2) < 1e-6

        # First solution
        c = asin(sin(a) / sin(alpha) * sin(gamma))
        b = _helper(a, c, alpha, gamma)
        alpha1, beta, gamma1 = _halfAngleFormula(a, b, c)
        if is_valid(alpha1, alpha) and is_valid(gamma1, gamma):
            solutions.append(SphereTriangle(a, b, c, alpha, beta, gamma))

        # Second solution
        c = pi - c
        b = _helper(a, c, alpha, gamma)
        alpha2, beta, gamma2 = _halfAngleFormula(a, b, c)
        if is_valid(alpha2, alpha) and is_valid(gamma2, gamma):
            solutions.append(SphereTriangle(a, b, c, alpha, beta, gamma))

        return solutions

    @classmethod
    def sss(
        SphereTriangle,
        a: float,
        b: float,
        c: float,
    ) -> SphereTriangle:
        alpha, beta, gamma = _halfAngleFormula(a, b, c)
        return SphereTriangle(a, b, c, alpha, beta, gamma)

    @classmethod
    def www(
        SphereTriangle,
        alpha: float,
        beta: float,
        gamma: float,
    ) -> SphereTriangle:
        a, b, c = _halfSideFormula(alpha, beta, gamma)
        return SphereTriangle(a, b, c, alpha, beta, gamma)


# Holds spherical coordinates as latitude and longitude.
# Can convert to and from Vec3.
class SphereCoords:
    phi: float  # aka latitude
    lam: float  # aka longitude
    r: float  # radius

    def __init__(self, phi: float, lam: float, r: float = 1):
        self.phi = phi
        self.lam = lam
        self.r = r

    def __repr__(self) -> str:
        return self.fmt()

    def fmt(self, precision=3):
        phi = fmt_deg_str(self.phi, precision)
        lam = fmt_deg_str(self.lam, precision)

        if self.r == 1:
            return f"(ϕ: {phi}, λ: {lam})"
        else:
            return f"(ϕ: {phi}, λ: {lam}, r: {self.r})"

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.phi
        if index == 1:
            return self.lam
        if index == 2:
            return self.r
        raise IndexError("index out of range")

    def lat(self) -> float:
        return degrees(self.phi)

    def lon(self) -> float:
        return degrees(self.lam)

    def to_vec3(self) -> Vec3:
        phi, lam, r = self
        x = r * cos(phi) * cos(lam)
        y = r * cos(phi) * sin(lam)
        z = r * sin(phi)
        return Vec3(x, y, z)

    def geodesic_distance_to(self, other: SphereCoords) -> float:
        return ha2(self, other)[0]

    @classmethod
    def from_vec3(SphereCoords, p: Vec3):
        r = p.normalize()
        x, y, z = p

        # Latitude can also be calculated using any of those:
        #   latitude = acos(x / cos(longitude))
        #   latitude = acos(y / sin(longitude))
        # But since latitude should always be in the range [-pi/2, pi/2], using asin is fine.
        phi = asin(z)
        lam = atan2(y, x)

        return SphereCoords(phi, lam, r)

    @classmethod
    def centroid(SphereCoords, points: list[SphereCoords]):
        p = Vec3(0, 0, 0)

        for point in points:
            p += point.to_vec3()

        p /= len(points)

        return SphereCoords.from_vec3(p)


def ha1(p1: SphereCoords, s12: float, a12: float):
    phi1, lam1, r = p1

    a12 = clamp_rad(a12)

    if a12 == 0:
        p2 = SphereCoords(
            phi=phi1 + s12,
            lam=lam1,
            r=r,
        )
        a21 = pi

    elif a12 == pi:
        p2 = SphereCoords(
            phi=phi1 - s12,
            lam=lam1,
            r=r,
        )
        a21 = 0

    elif a12 < pi:
        triangle = SphereTriangle.sws(
            a=pi / 2 - phi1,
            b=s12 / r,
            gamma=a12,
        )
        p2 = SphereCoords(
            phi=pi / 2 - triangle.c,
            lam=lam1 + triangle.beta,
            r=r,
        )
        a21 = tau - triangle.alpha

    else:
        triangle = SphereTriangle.sws(
            a=s12 / r,
            b=pi / 2 - phi1,
            gamma=tau - a12,
        )
        p2 = SphereCoords(
            phi=pi / 2 - triangle.c,
            lam=lam1 - triangle.alpha,
            r=r,
        )
        a21 = triangle.beta

    return p2, a21


def ha2(p1: SphereCoords, p2: SphereCoords):
    phi1, lam1, r1 = p1
    phi2, lam2, r2 = p2
    assert r1 == r2

    if lam1 == lam2:
        distance = abs(phi1 - phi2) * r1
        if phi1 < phi2:
            azimuth = 0
            reverse_azimuth = pi
        else:
            azimuth = pi
            reverse_azimuth = 0
    else:
        # Pole Triangle
        T = SphereTriangle.sws(
            a=pi / 2 - phi1,
            b=pi / 2 - phi2,
            gamma=lam2 - lam1,
        )
        distance = T.c * r1

        if lam1 < lam2:
            azimuth = T.beta
            reverse_azimuth = tau - T.alpha
        else:
            azimuth = tau - T.beta
            reverse_azimuth = T.alpha

    return distance, azimuth, reverse_azimuth


# Given two positions and their azimuths towards a third position, calculate the third position.
def vws(
    P1: SphereCoords,
    P2: SphereCoords,
    a13: float,
    a23: float,
):
    # Create a triangle containing P1, P2, P3.
    # At P1 is alpha, at P2 is beta. c is the distance between P1 and P2.

    # We already know P1 and P2, so we can calculate their distance and their azimuth towards each other.
    s12, a12, a21 = ha2(P1, P2)

    if a12 > a13:
        # P3 is "over" P1 and P2.
        T = SphereTriangle.wsw(
            alpha=a12 - a13,
            beta=a23 - a21,
            c=s12,
        )
    else:
        # P3 is "under" P1 and P2.
        T = SphereTriangle.wsw(
            alpha=a13 - a12,
            beta=a21 - a23,
            c=s12,
        )
    s13 = T.b
    P3, _ = ha1(P1, s13, a13)
    # or:
    # s23 = T.a
    # P3 = ha1(P2, s23, a23)
    return P3


# Given two positions and their distance towards a third position, calculate the third position.
def bgs(
    P1: SphereCoords,
    P2: SphereCoords,
    s13: float,
    s23: float,
):
    s12, a12 = ha2(P1, P2)
    s21, a21 = ha2(P2, P1)

    T = SphereTriangle.sss(a=s12, b=s13, c=s23)

    # Assuming P3 is "over" P1 and P2.
    a13 = a12 - T.gamma
    P3, _ = ha1(P1, s13, a13)

    # Alternative:
    # a23 = a21 + T.beta
    # P3, _ = ha1(P2, s23, a23)

    return P3


import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def plot_point(point: SphereCoords, text: str = None, **kwargs):
    """Draw a spherical coordinate as a point on the map."""
    x, y = plt.gca().projection.transform_point(
        point.lon(), point.lat(), ccrs.PlateCarree()
    )

    plt.plot(x, y, **kwargs)
    if text is not None:
        plt.annotate(
            text,
            (x, y - 1.2e5),
            color="black",
            ha="center",
            fontweight="bold",
        )


def plot_line(p1: SphereCoords, p2: SphereCoords, **kwargs):
    """Draw a geodesic line between two points, which will be curved by the projection."""
    # Calculate the distance and azimuth between the two points.
    max_dist, azimuth, _ = ha2(p1, p2)

    # Interpolate a number of positions between the two points and calculate their spherical coordinates.
    granularity = 0.01
    num_points = int(max_dist / granularity)

    coordinates = [p1]
    for dist in np.linspace(0, max_dist, num_points):
        p, _ = ha1(p1, dist, azimuth)
        coordinates.append(p)

    # Connect the points with a line.
    plt.plot(
        list(map(lambda p: p.lon(), coordinates)),
        list(map(lambda p: p.lat(), coordinates)),
        transform=ccrs.PlateCarree(),
        **kwargs,
    )


def plot_circle(center: SphereCoords, radius: float, **kwargs):
    """Draw a geodesic circle around a point, which be squashed by the projection."""
    # Interpolate a number of positions around the point in the given distance,
    # and calculate their spherical coordinates.
    coordinates: list[SphereCoords] = []
    for azimuth in np.linspace(0, 2 * pi, 72):
        p, _ = ha1(center, radius, azimuth)
        coordinates.append(p)

    # Connect the points with a line.
    plt.plot(
        list(map(lambda p: p.lon(), coordinates)),
        list(map(lambda p: p.lat(), coordinates)),
        transform=ccrs.PlateCarree(),
        **kwargs,
    )


def plot_azimuth(point: SphereCoords, azimuth: float, length: float = 0, **kwargs):
    """Draw an azimuth line from a point, which will be curved by the projection. Also draws the angle into the map."""

    north_dist = 0.02
    angle_dist = 0.01
    angle_granularity = 0.2

    # Get a point to the north of the given point, and draw an indication line to it.
    pn, _ = ha1(point, north_dist, 0)
    plot_line(point, pn, color="gray", linestyle="dotted")

    # Draw the angle from the north direction to the given azimuth.
    coordinates: list[SphereCoords] = []
    for azimuth in np.linspace(0, azimuth, int(azimuth / angle_granularity)):
        p, _ = ha1(point, angle_dist, azimuth)
        coordinates.append(p)
    plt.plot(
        list(map(lambda p: p.lon(), coordinates)),
        list(map(lambda p: p.lat(), coordinates)),
        transform=ccrs.PlateCarree(),
        **kwargs,
    )

    # Draw the azimuth line from the point.
    pa, _ = ha1(point, length, azimuth)
    plot_line(point, pa, **kwargs)


def plot_angle(p1: SphereCoords, p2: SphereCoords, p3: SphereCoords, **kwargs):
    """Draw an angle between the two rays p1p2 and p2p3"""

    _, a12, _ = ha2(p1, p2)
    _, a13, _ = ha2(p1, p3)

    dist = 0.01
    granularity = 0.1

    if a13 < a12:
        a13 += tau

    coordinates = []
    for azimuth in np.linspace(a12, a13, int(abs((a13 - a12) / granularity))):
        p, _ = ha1(p1, dist, azimuth % tau)
        coordinates.append(p)

    plt.plot(
        list(map(lambda p: p.lon(), coordinates)),
        list(map(lambda p: p.lat(), coordinates)),
        transform=ccrs.PlateCarree(),
        **kwargs,
    )
