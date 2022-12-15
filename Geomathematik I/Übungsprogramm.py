from libgeo import fmt_gon_str, from_gon
from lib3d import Mat3
from libsphere import SphereCoords

"""

Measurement Data

"""

# Positions of three measurement stations using latitude/longitude (given in gradians, converted to radians here).
#   P1: Fort Davis, TX
#   P2: Mammoth Lakes, CA
#   P3: Columbus, OH
P1_lat = from_gon(30, 38)
P1_lon = from_gon(-103, 57)

P2_lat = from_gon(37, 38)
P2_lon = from_gon(-118, 56)

P3_lat = from_gon(40)
P3_lon = from_gon(-83)

# Displacements of the original positions have been measured for the first two stations, given as delta latitude/longitude.
P1_lat_delta = from_gon(0, 0, -0.02033)
P1_lon_delta = from_gon(0, 0, 0.01034)

P2_lat_delta = from_gon(0, 0, -0.02506)
P2_lon_delta = from_gon(0, 0, 0.01119)


"""

Data Processing

"""

# Convert the lat/lon positions into cartesian coordinates.
#   P: position before rotation
#   Q: position after rotation

P1 = SphereCoords(P1_lat, P1_lon).to_vec3()
P2 = SphereCoords(P2_lat, P2_lon).to_vec3()
P3 = SphereCoords(P3_lat, P3_lon).to_vec3()

Q1 = SphereCoords(P1_lat + P1_lat_delta, P1_lon + P1_lon_delta).to_vec3()
Q2 = SphereCoords(P2_lat + P2_lat_delta, P2_lon + P2_lon_delta).to_vec3()

# Calculate displacement vectors of the two stations within the rotational plane.
h1 = Q1 - P1
h2 = Q2 - P2

# Calculate the rotational axis as the perpendicular of the two displacement vectors.
rotation_axis = h1.cross(h2).normalized()

# Project the points onto the rotation axis to find the center of rotation.
# Since the two measurement stations might not be inside the same rotational plane (e.g.
# they are on different heights along the rotational axis), we have to calculate different
# centers for each point.
center1 = P1.projected_on(rotation_axis)
center2 = P2.projected_on(rotation_axis)

# Also project the rotated points onto the axis for scrutiny. They should be identical to the
# center of the non-rotated point!
center1_ = Q1.projected_on(rotation_axis)
center2_ = Q2.projected_on(rotation_axis)
assert (center1 - center1_).length() < 1e-6
assert (center2 - center2_).length() < 1e-6

# Using two vectors going from the center to the two point position (original and reported),
# we can find the angle of rotation as the angle between these two vectors.
cp1 = P1 - center1
cp1_ = Q1 - center1
angle1 = cp1.angle_between(cp1_)

# To check that the rotation is the same for both points (which we expect if the rotating body
# is rigid), calculate the angle for the second point and compare.
cp2 = P2 - center2
cp2_ = Q2 - center2
angle2 = cp2.angle_between(cp2_)
assert abs(angle1 - angle2) < 1e-6

# Now that we know the rotation over the span of 5 years, we can extrapolate it into the future.
angle_per_year = angle1 / 5
angle_5y = angle_per_year * 5
angle_10y = angle_per_year * 10
angle_15y = angle_per_year * 15

# Check how far Columbus would move in 10 years
R = Mat3.from_axis_and_angle(rotation_axis, angle_10y)
Q3 = R * P3

# This gives us the 3D coordinates of Columbus in 10 years.
# Transform them back into spherical coordinates.
Q3_lat, Q3_lon, _ = SphereCoords.from_vec3(Q3)

# Calculate the difference between the original and the predicted position,
# and output it in gradians.
P3_lat_delta = Q3_lat - P3_lat
P3_lon_delta = Q3_lon - P3_lon

print(f"db (Columbus, OH): {fmt_gon_str(P3_lat_delta, precision=20)}")
print(f"dl (Columbus, OH): {fmt_gon_str(P3_lon_delta, precision=20)}")


R_ = Mat3.from_axis_and_angle(rotation_axis, angle_10y, infinitesimal=True)
Q3_ = R_ * P3
Q3_lat_, Q3_lon_, _ = SphereCoords.from_vec3(Q3_)
P3_lat_delta_ = Q3_lat_ - P3_lat
P3_lon_delta_ = Q3_lon_ - P3_lon

print("Using infinitesimal rotation matrix:")
print(f"db (Columbus, OH): {fmt_gon_str(P3_lat_delta_, precision=20)}")
print(f"dl (Columbus, OH): {fmt_gon_str(P3_lon_delta_, precision=20)}")
