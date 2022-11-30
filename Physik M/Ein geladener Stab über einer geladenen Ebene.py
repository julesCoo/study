from lib.vector import Vec3
import numpy as np


"""
Ein gleichmäßig geladener Stab hat eine Ladungsdichte von 200 nC/cm und ist parallel zur x-Achse bei y = 0, z = 2 cm.
Der Stab befindet sich über einer gleichmäßig geladenen Ebene bei z = 0 mit einer Ladungsdichte von 6 nC/cm².
Wie groß ist das elektrische Feld an Position r = 4x - 5y - 4z [cm]?
"""

rho_rod = 400 * 1e-9 / 1e-2
rho_plane = 5 * 1e-9 / 1e-4

r = Vec3(8e-2, -2e-2, -4e-2)


def r_rod(x):
    return Vec3(x, 0, 2e-2)


def r_plane(x, y):
    return Vec3(x, y, 0)


eps0 = 8.854187817e-12

# Vector dr (r to rod) - x is variable, but is set to 0 here
x = r_rod(0)
y = r.y - r_rod(x).y
z = r.z - r_rod(x).z

E_rod = (
    Vec3(
        # Integration of dr / |dr|**3 over x in [-inf, inf]
        0,
        2 * y / (y**2 + z**2),
        2 * z / (y**2 + z**2),
    )
    * rho_rod
    / (4 * np.pi * eps0)
)

# Vector dr (r to plane) - x and y are variable, but are set to 0 here
x = r_plane(0, 0).x
y = r_plane(x, 0).y
z = r.z - r_plane(x, y).z

E_plane = (
    Vec3(
        # Integration of dr / |dr|**3 over x and y in [-inf, inf]
        0,
        0,
        (2 * np.pi * z) / (z**2) ** 0.5,
    )
    * rho_plane
    / (4 * np.pi * eps0)
)


print(E_rod + E_plane)
