from __future__ import annotations
from math import asin, sin, cos, sqrt, atan, pi

# Sinussatz
# Given 2 sides of a spheric triangle, and the angle between them,
# calculate the third side.
def _sws(b: float, c: float, alpha: float):
    sin_a_half = sqrt(sin((b - c) / 2) ** 2 + sin(b) + sin(c) + sin(alpha / 2) ** 2)
    cos_a_half = sqrt(cos((b + c) / 2) ** 2 + sin(b) * sin(c) * cos(alpha / 2) ** 2)
    tan_a_half = sin_a_half / cos_a_half
    a_half = atan(tan_a_half)
    a = 2 * a_half
    return a


# Kosinussatz
# Give a side of a spheric triangle, and the two angles on this side,
# calculate the third angle.
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


# Halbseitensatz
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


# Halbwinkelsatz
def _sss(a: float, b: float, c: float):
    s = (a + b + c) / 2
    tan_alpha_half = sqrt(sin(s - b) * sin(s - c) / (sin(s) * sin(s - a)))
    tan_beta_half = sqrt(sin(s - a) * sin(s - c) / (sin(s) * sin(s - b)))
    tan_gamma_half = sqrt(sin(s - a) * sin(s - b) / (sin(s) * sin(s - c)))
    alpha_half = atan(tan_alpha_half)
    beta_half = atan(tan_beta_half)
    gamma_half = atan(tan_gamma_half)
    alpha = 2 * alpha_half
    beta = 2 * beta_half
    gamma = 2 * gamma_half
    return alpha, beta, gamma


# Hilfsformel
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


class Triangle:
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

    @classmethod
    def sws(cls, a: float, b: float, gamma: float) -> Triangle:
        c = _sws(a, b, gamma)
        alpha, beta, gamma = _sss(a, b, c)
        return cls(a, b, c, alpha, beta, gamma)

    @classmethod
    def wsw(cls, alpha: float, beta: float, c: float) -> Triangle:
        gamma = _wsw(c, alpha, beta)
        a, b, c = _www(alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma)

    @classmethod
    def ssw(cls, a: float, c: float, alpha: float) -> tuple[Triangle, Triangle]:
        gamma1 = asin(sin(c) * sin(alpha) / sin(a))
        b1 = _helper(a, c, alpha, gamma1)
        alpha1, beta1, gamma1 = _sss(a, b1, c)

        gamma2 = pi - gamma1
        b2 = _helper(a, c, alpha, gamma2)
        alpha2, beta2, gamma2 = _sss(a, b2, c)

        return (
            cls(a, b1, c, alpha1, beta1, gamma1),
            cls(a, b2, c, alpha2, beta2, gamma2),
        )

    @classmethod
    def wws(cls, alpha: float, gamma: float, a: float) -> tuple[Triangle, Triangle]:
        c1 = asin(sin(a) / sin(alpha) * sin(gamma))
        b1 = _helper(a, c1, alpha, gamma)
        alpha1, beta1, gamma1 = _sss(a, b1, c1)

        c2 = pi - c1
        b2 = _helper(a, c2, alpha, gamma)
        alpha2, beta2, gamma2 = _sss(a, b2, c2)

        return (
            cls(a, b1, c1, alpha1, beta1, gamma1),
            cls(a, b2, c2, alpha2, beta2, gamma2),
        )

    @classmethod
    def sss(cls, a: float, b: float, c: float) -> Triangle:
        alpha, beta, gamma = _sss(a, b, c)
        return cls(a, b, c, alpha, beta, gamma)

    @classmethod
    def www(cls, alpha: float, beta: float, gamma: float) -> Triangle:
        a, b, c = _www(alpha, beta, gamma)
        return cls(a, b, c, alpha, beta, gamma)
