from libsphere import SphereCoords, bgs, ha1, ha2
from libgeo import from_deg

earth_radius = 6371221  # m
travel_speed = 20 * 1852  # m/h (20 knots)

# The ship starts from here
P1 = SphereCoords(
    phi=from_deg(26, 12, 43),
    lam=from_deg(-79, 30, 19),
)

# This is a reference position
P2 = SphereCoords(
    phi=from_deg(25, 50, 21),
    lam=from_deg(-73, 42, 30),
)

# After 10 hours, the ship traveled some distance s13 and is now at P3.
# The distance is downscaled to be on a unit sphere.
s13 = 10 * travel_speed / earth_radius

# At P3, the distance to the reference position is measured as 439844 m.
# This distance is also downscaled to be on a unit sphere.
s23 = 439844 / earth_radius

# Given this information, we can calculate the position of the ship at P3.
P3 = bgs(P1, P2, s13, s23)

# This also gives us the movement direction of the ship, as azimuth a13.
s13_, a13 = ha2(P1, P3)

# If the ship moves for another 10 hours, it will travel the double distance at the same azimuth,
# finally reaching P4.
P4, _ = ha1(P1, 2 * s13, a13)

print(P4)
