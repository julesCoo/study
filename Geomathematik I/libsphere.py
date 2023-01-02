from __future__ import annotations
from math import asin, atan2, cos, radians, sin, pi, sqrt, atan
from lib3d import Vec3
from libgeo import fmt_deg_str

# A spherical triangle is created from the intersection of 3 great circles
# on a unit sphere. All angles and sides are given in radians.
class SphereTriangle:
    alpha: float
    beta: float
    gamma: float
    a: float
    b: float
    c: float

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
        alpha: float,
        beta: float,
        gamma: float,
    ):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def __repr__(self) -> str:
        return f"SphereTriangle({self.a}, {self.b}, {self.c}, {self.alpha}, {self.beta}, {self.gamma})"

    def excess(self) -> float:
        return self.alpha + self.beta + self.gamma - pi

    def area(self, radius=1) -> float:
        return self.excess() * radius**2

    @classmethod
    def ppp(cls, p1: SphereCoords, p2: SphereCoords, p3: SphereCoords):
        s12, _ = ha2(p1, p2)
        s23, _ = ha2(p2, p3)
        s31, _ = ha2(p3, p1)
        return cls.sss(s12, s23, s31)

    @classmethod
    def sws(cls, a: float, b: float, gamma: float) -> SphereTriangle:
        c = cls._sws(a, b, gamma)
        alpha, beta, gamma = cls._sss(a, b, c)
        return cls(a, b, c, alpha, beta, gamma)

    @classmethod
    def wsw(cls, alpha: float, beta: float, c: float) -> SphereTriangle:
        gamma = cls._wsw(c, alpha, beta)
        a, b, c = cls._www(alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma)

    @classmethod
    def ssw(
        cls, a: float, c: float, alpha: float
    ) -> tuple[SphereTriangle, SphereTriangle]:
        gamma1 = asin(sin(c) * sin(alpha) / sin(a))
        b1 = cls._helper(a, c, alpha, gamma1)
        alpha1, beta1, gamma1 = cls._sss(a, b1, c)

        gamma2 = pi - gamma1
        b2 = cls._helper(a, c, alpha, gamma2)
        alpha2, beta2, gamma2 = cls._sss(a, b2, c)

        return (
            cls(a, b1, c, alpha1, beta1, gamma1),
            cls(a, b2, c, alpha2, beta2, gamma2),
        )

    @classmethod
    def wws(
        cls, alpha: float, gamma: float, a: float
    ) -> tuple[SphereTriangle, SphereTriangle]:
        c1 = asin(sin(a) / sin(alpha) * sin(gamma))
        b1 = cls._helper(a, c1, alpha, gamma)
        alpha1, beta1, gamma1 = cls._sss(a, b1, c1)

        c2 = pi - c1
        b2 = cls._helper(a, c2, alpha, gamma)
        alpha2, beta2, gamma2 = cls._sss(a, b2, c2)

        return (
            cls(a, b1, c1, alpha1, beta1, gamma1),
            cls(a, b2, c2, alpha2, beta2, gamma2),
        )

    @classmethod
    def sss(cls, a: float, b: float, c: float) -> SphereTriangle:
        alpha, beta, gamma = cls._sss(a, b, c)
        return cls(a, b, c, alpha, beta, gamma)

    @classmethod
    def www(cls, alpha: float, beta: float, gamma: float) -> SphereTriangle:
        a, b, c = cls._www(alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma)

    # Cosine rule for sides
    # Given 2 sides of a spheric triangle, and the angle between them, calculate the third side.
    def _sws(b: float, c: float, alpha: float):
        sin_a_half = sqrt(sin((b - c) / 2) ** 2 + sin(b) * sin(c) * sin(alpha / 2) ** 2)
        cos_a_half = sqrt(cos((b + c) / 2) ** 2 + sin(b) * sin(c) * cos(alpha / 2) ** 2)
        tan_a_half = sin_a_half / cos_a_half
        a_half = atan(tan_a_half)
        a = 2 * a_half
        return a

    # Cosine rule for angles
    # Given a side of a spheric triangle, and the two angles on this side, calculate the third angle.
    def _wsw(a: float, beta: float, gamma: float):
        sin_alpha_half = sqrt(
            cos((beta + gamma) / 2) ** 2 + sin(beta) * sin(gamma) * sin(a / 2) ** 2
        )
        cos_alpha_half = sqrt(
            sin((beta - gamma) / 2) ** 2 + sin(beta) * sin(gamma) * cos(a / 2) ** 2
        )
        tan_alpha_half = sin_alpha_half / cos_alpha_half
        alpha_half = atan(tan_alpha_half)
        alpha = 2 * alpha_half
        return alpha

    # Half-side formula
    def _www(alpha: float, beta: float, gamma: float):
        rho = (alpha + beta + gamma) / 2
        cr = cos(rho)
        cra = cos(rho - alpha)
        crb = cos(rho - beta)
        crg = cos(rho - gamma)
        a = 2 * atan(1 / sqrt(crb * crg / (-cr * cra)))
        b = 2 * atan(1 / sqrt(cra * crg / (-cr * crb)))
        c = 2 * atan(1 / sqrt(cra * crb / (-cr * crg)))
        return a, b, c

    # Half-angle formula
    def _sss(a: float, b: float, c: float):
        s = (a + b + c) / 2
        ss = sin(s)
        ssa = sin(s - a)
        ssb = sin(s - b)
        ssc = sin(s - c)
        alpha = 2 * atan(sqrt(ssb * ssc / (ss * ssa)))
        beta = 2 * atan(sqrt(ssa * ssc / (ss * ssb)))
        gamma = 2 * atan(sqrt(ssa * ssb / (ss * ssc)))
        return alpha, beta, gamma

    # Unnamed helper method
    def _helper(b: float, c: float, beta: float, gamma: float):
        k = sqrt(1 - sin(b) * sin(c) * sin(beta) * sin(gamma))
        k_sin_a_half = sqrt(
            sin((b - c) / 2) ** 2 + sin(b) * sin(c) * cos((beta + gamma) / 2) ** 2
        )
        k_cos_a_half = sqrt(
            cos((b + c) / 2) ** 2 + sin(b) * sin(c) * sin((beta - gamma) / 2) ** 2
        )
        tan_a_half = k_sin_a_half / k_cos_a_half
        a_half = atan(tan_a_half)
        a = 2 * a_half
        return a


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

    def to_vec3(self):
        phi, lam, r = self
        x = r * cos(phi) * cos(lam)
        y = r * cos(phi) * sin(lam)
        z = r * sin(phi)
        return Vec3(x, y, z)

    @classmethod
    def from_vec3(cls, p: Vec3):
        r = p.normalize()
        x, y, z = p

        # Latitude can also be calculated using any of those:
        #   latitude = acos(x / cos(longitude))
        #   latitude = acos(y / sin(longitude))
        # But since latitude should always be in the range [-pi/2, pi/2], using asin is fine.
        phi = asin(z)
        lam = atan2(y, x)

        return cls(phi, lam, r)


def ha1(p1: SphereCoords, s12: float, a12: float):
    phi1, lam1, r = p1

    if a12 < radians(180):
        triangle = SphereTriangle.sws(
            a=radians(90) - phi1,
            b=s12 / r,
            gamma=a12,
        )
        p2 = SphereCoords(
            phi=radians(90) - triangle.c,
            lam=lam1 + triangle.beta,
            r=r,
        )
        a21 = radians(360) - triangle.alpha

    else:
        triangle = SphereTriangle.sws(
            a=s12 / r,
            b=radians(90) - phi1,
            gamma=radians(360) - a12,
        )
        p2 = SphereCoords(
            phi=radians(90) - triangle.c,
            lam=lam1 - triangle.alpha,
            r=r,
        )
        a21 = triangle.beta

    return p2, a21


def ha2(p1: SphereCoords, p2: SphereCoords):
    phi1, lam1, r1 = p1
    phi2, lam2, r2 = p2
    assert r1 == r2

    # Pole Triangle
    triangle = SphereTriangle.sws(
        a=pi / 2 - phi1,
        b=pi / 2 - phi2,
        gamma=lam2 - lam1,
    )
    distance = triangle.c * r1
    azimuth = triangle.beta

    if lam1 > lam2:
        azimuth = radians(360) - azimuth

    return distance, azimuth


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
    s12, a12 = ha2(P1, P2)
    s21, a21 = ha2(P2, P1)

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
