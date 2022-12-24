from libsphere import SphereCoords
from libgeo import from_deg

earth_radius = 6371221  # m


# A ship moves from Miami (P1) roughly northeast.
P1 = SphereCoords(from_deg(26, 12, 43), from_deg(-79, 30, 19), earth_radius)

# It moves for 10 hours at a speed of 20 knots.
distance_traveled = 20 * 1852 * 10  # m

# There is a second ship at P2, which now has a given distance d to the first ship.
P2 = SphereCoords(from_deg(25, 50, 21), from_deg(-73, 42, 30), earth_radius)
d = 439844  # m

# The first ship continues on its course for another 10 hours.
# Where is it?

import numpy as np
import matplotlib.pyplot as plt


def plot_earth():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.set_xlim(-earth_radius, earth_radius)
    ax.set_ylim(-earth_radius, earth_radius)
    ax.set_zlim(-earth_radius, earth_radius)
    ax.set_aspect("equal")

    phi_min, phi_max, phi_steps = from_deg(-90), from_deg(+90), 45
    lam_min, lam_max, lam_steps = from_deg(-180), from_deg(+180), 90

    phi, lam = np.meshgrid(
        np.linspace(phi_min, phi_max, phi_steps),
        np.linspace(lam_min, lam_max, lam_steps),
    )

    x = earth_radius * np.cos(phi) * np.cos(lam)
    y = earth_radius * np.cos(phi) * np.sin(lam)
    z = earth_radius * np.sin(phi)
    ax.plot_wireframe(x, y, z, color="black", alpha=0.1)

    # draw equator
    phi = 0
    lam = np.linspace(lam_min, lam_max, lam_steps)
    x = earth_radius * np.cos(phi) * np.cos(lam)
    y = earth_radius * np.cos(phi) * np.sin(lam)
    z = earth_radius * np.sin(phi)
    ax.plot(x, y, z, color="black", alpha=0.5)

    # draw prime meridian
    phi = np.linspace(phi_min, phi_max, phi_steps)
    lam = 0
    x = earth_radius * np.cos(phi) * np.cos(lam)
    y = earth_radius * np.cos(phi) * np.sin(lam)
    z = earth_radius * np.sin(phi)
    ax.plot(x, y, z, color="black", alpha=0.5)

    return ax


earth = plot_earth()

x1, y1, z1 = P1.to_vec3()
x2, y2, z2 = P2.to_vec3()

earth.plot(x1, y1, z1, "o", color="red")
earth.plot(x2, y2, z2, "o", color="blue")

plt.show()
