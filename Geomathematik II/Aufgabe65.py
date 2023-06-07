# Abgabe am 26.06.

from sympy import *
from lib import *
from math import radians

beta.lamda = symbols("beta lambda", real=True, nonnegative=True)

surface = Surface(
    (beta, lamda),
    3 * cos(beta) * cos(lamda),
    3 * cos(beta) * sin(lamda),
    sin(beta),
)

beta0 = radians(30)
s = 0.015

# Rechnen bis 4. Ordnung
# Kurzer technischer Bericht
