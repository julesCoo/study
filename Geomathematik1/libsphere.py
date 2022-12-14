from __future__ import annotations
from math import asin, atan2, cos, degrees, radians, sin, pi, tau, sqrt, atan
from libgeo import Angle
from lib3d import Vec3

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
        cot_a_half = sqrt(
            cos(rho - beta) * cos(rho - gamma) / (-cos(rho) * cos(rho - alpha))
        )
        cot_b_half = sqrt(
            cos(rho - alpha) * cos(rho - gamma) / (-cos(rho) * cos(rho - beta))
        )
        cot_c_half = sqrt(
            cos(rho - alpha) * cos(rho - beta) / (-cos(rho) * cos(rho - gamma))
        )
        a_half = atan(cot_a_half)
        b_half = atan(cot_b_half)
        c_half = atan(cot_c_half)
        a = 2 * a_half
        b = 2 * b_half
        c = 2 * c_half
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
    lat: float  # phi
    lon: float  # lambda
    r: float  # radius

    def __init__(self, lat: float, lon: float, r: float = 1):
        self.lat = lat
        self.lon = lon
        self.r = r

    def __repr__(self) -> str:
        phi = Angle.from_rad(self.lat).to_deg_str()
        lam = Angle.from_rad(self.lon).to_deg_str()

        if self.r == 1:
            return f"(ϕ: {phi}, λ: {lam})"
        else:
            return f"(ϕ: {phi}, λ: {lam}, r: {self.r})"

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.lat
        if index == 1:
            return self.lon
        if index == 2:
            return self.r
        raise IndexError("index out of range")

    def to_vec3(self):
        lat, lon, r = self
        x = r * cos(lat) * cos(lon)
        y = r * cos(lat) * sin(lon)
        z = r * sin(lat)
        return Vec3(x, y, z)

    def ha1(self, s12: float, a12: float):
        phi1, lam1, r = self

        if a12 < radians(180):
            triangle = SphereTriangle.sws(
                a=radians(90) - phi1,
                b=s12,
                gamma=a12,
            )
            p2 = SphereCoords.from_phi_lamda(
                phi=radians(90) - triangle.c,
                lam=lam1 + triangle.beta,
                r=r,
            )
            a21 = radians(360) - triangle.alpha

        else:
            triangle = SphereTriangle.sws(
                a=s12,
                b=radians(90) - phi1,
                gamma=radians(360) - a12,
            )
            p2 = SphereCoords.from_phi_lamda(
                phi=radians(90) - triangle.c,
                lam=lam1 - triangle.alpha,
                r=r,
            )
            a21 = triangle.beta

        return p2, a21

    def ha2(self, other: SphereCoords):
        phi1, lam1, r1 = self
        phi2, lam2, r2 = other
        assert r1 == r2

        triangle = SphereTriangle.sws(
            a=pi / 2 - phi1,
            b=pi / 2 - phi2,
            gamma=lam2 - lam1,
        )
        dist = triangle.c * r1
        angle = triangle.beta

        return dist, angle

    @classmethod
    def from_phi_lamda(cls, phi: float, lam: float, r: float = 1):
        return cls(phi, lam, r)

    @classmethod
    def from_vec3(cls, p: Vec3):
        r = p.normalize()
        x, y, z = p

        # Latitude can also be calculated using any of those:
        #   latitude = acos(x / cos(longitude))
        #   latitude = acos(y / sin(longitude))
        # But since latitude should always be in the range [-pi/2, pi/2], using asin is fine.
        lat = asin(z)
        lon = atan2(y, x)

        return cls(lat, lon, r)
