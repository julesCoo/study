from lib.vector import Vec3
import numpy as np

eps_r = 10
eps_0 = 8.854187817e-12
eps = eps_r * eps_0


def charge_density(r: Vec3) -> float:
    if r.z < -0.3e-6:
        return 0
    elif r.z > 0.3e-6:
        return 0
    else:
        return 7e10 * r.z


r = Vec3(0.8, 0.2, 0.7) * 1e-6


z0 = -0.3e-6
z1 = 0.3e-6
d = 1e-9

E = 0
for z in np.arange(z0, z1, d):
    rho = charge_density(Vec3(0, 0, z))
    E += (rho / eps) * d

print(E)


"""
Die Kraft eines Körpers ist proportional zu seiner Ladung q, und dem Elektrischen Feld E, in dem er sich befindet.
Das Feld ist eine Vektorgröße, die Ladung ist eine Skalargröße.
    F = q*E

Das Elektrische Feld E ist der Gradient des elektrischen Potentials phi.
Zu beachten ist hier, dass es in die Richtung des negativen Potentials zeigt!
    E = -grad(phi)

Das elektrische Potential phi ist die Energie des elektrischen Felds an einem bestimmten Ort.
Je größer das Potential, desto mehr Arbeit kann von dem Feld verrichtet werden.
Eine Ladung in einem elektrischen Feld ist vergleichbar zu einer Masse in einem Gravitationsfeld.

Das Potential entsteht durch die Arbeit, die nötig ist, eine Ladung in einem Elektrischen Feld an einen Ort zu bewegen.
Diese Arbeit wirkt der Coloumbkraft entgegen, welche die Ladung von dem Feld abstößt (vgl. zur Hubarbeit).
    phi = q / (4*pi*eps0) * 1/r


Die Ladungsdichte rho misst die Ladung pro Raumvolumen oder Fläche.
    rho = q / V

Der Zusammenhang von Ladungsdichte und elektrischem Potential ist:
    rho = -grad(phi)
    phi = -1/(4*pi*eps0) * int(rho dr)
"""


#
