from libgeo import fmt_deg_str, from_deg
from lib3d import Mat3
from libsphere import SphereCoords

"""

Measurement Data

"""

# Positions of three measurement stations using latitude/longitude (given in gradians, converted to radians here).
#   P1: Fort Davis, TX
#   P2: Mammoth Lakes, CA
#   P3: Columbus, OH
P1_lat = from_deg(30, 38)
P1_lon = from_deg(-103, 57)

P2_lat = from_deg(37, 38)
P2_lon = from_deg(-118, 56)

P3_lat = from_deg(40)
P3_lon = from_deg(-83)

# Displacements of the original positions have been measured for the first two stations, given as delta latitude/longitude.
P1_lat_delta = from_deg(0, 0, -0.02033)
P1_lon_delta = from_deg(0, 0, 0.01034)

P2_lat_delta = from_deg(0, 0, -0.02506)
P2_lon_delta = from_deg(0, 0, 0.01119)


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
c1 = P1.projected_on(rotation_axis)
c2 = P2.projected_on(rotation_axis)

# Also project the rotated points onto the axis for scrutiny. They should be identical to the
# center of the non-rotated point!
c1_ = Q1.projected_on(rotation_axis)
c2_ = Q2.projected_on(rotation_axis)
assert (c1 - c1_).length() < 1e-6
assert (c2 - c2_).length() < 1e-6

# Using two vectors going from the center to the two point position (original and reported),
# we can find the angle of rotation as the angle between these two vectors.
cp1 = P1 - c1
cp1_ = Q1 - c1
angle1 = cp1.angle_between(cp1_)

# To check that the rotation is the same for both points (which we expect if the rotating body
# is rigid), calculate the angle for the second point and compare.
cp2 = P2 - c2
cp2_ = Q2 - c2
angle2 = cp2.angle_between(cp2_)
assert abs(angle1 - angle2) < 1e-6

# Angles deviate by about 1%. Calculate the average and work with that to minimize the error.
angle = (angle1 + angle2) / 2

# Check and potentially correct the orientation of the rotation axis
right_system = rotation_axis.cross(cp1).dot(cp1_) > 0
if not right_system:
    rotation_axis = -rotation_axis

# Now that we know the rotation over the span of 5 years, we can extrapolate it into the future.
angle_a = angle / 5
angle_5 = angle_a * 5
angle_10 = angle_a * 10

# Check how far Columbus would move in 10 years
R10 = Mat3.from_axis_and_angle(rotation_axis, angle_10, infinitesimal=True)
Q3 = R10 * P3

# This gives us the 3D coordinates of Columbus in 10 years.
# Transform them back into spherical coordinates.
Q3_lat, Q3_lon, _ = SphereCoords.from_vec3(Q3)

# Calculate the difference between the original and the predicted position,
# and output it in gradians.
P3_lat_delta = Q3_lat - P3_lat
P3_lon_delta = Q3_lon - P3_lon

"""

Backward Rotation (for verification)

"""

R5 = Mat3.from_axis_and_angle(rotation_axis, angle_5, infinitesimal=True)
Q1_ = R5 * P1
Q2_ = R5 * P2
assert Q1.equals(Q1_)
assert Q2.equals(Q2_)


Q1_lat_, Q1_lon_, _ = SphereCoords.from_vec3(Q1_)
Q2_lat_, Q2_lon_, _ = SphereCoords.from_vec3(Q2_)

P1_lat_delta_ = Q1_lat_ - P1_lat
P1_lon_delta_ = Q1_lon_ - P1_lon
P2_lat_delta_ = Q2_lat_ - P2_lat
P2_lon_delta_ = Q2_lon_ - P2_lon

"""

Output

"""

print(f"db1: {1e8*P1_lat_delta:.5f}")
print(f"dl1: {1e8*P1_lon_delta:.5f}")

print(f"db1': {1e8*P1_lat_delta_:.5f}")
print(f"dl1': {1e8*P1_lon_delta_:.5f}")

print(f"db2: {1e8*P2_lat_delta:.5f}")
print(f"dl2: {1e8*P2_lon_delta:.5f}")

print(f"db2': {1e8*P2_lat_delta_:.5f}")
print(f"dl2': {1e8*P2_lon_delta_:.5f}")


# print(f"rotational axis: {rotation_axis}")
# print(f"angle of rotation: {fmt_deg_str(angle)}")

# print(f"db (Columbus, OH): {fmt_deg_str(P3_lat_delta, precision=5)}")
# print(f"dl (Columbus, OH): {fmt_deg_str(P3_lon_delta, precision=5)}")
