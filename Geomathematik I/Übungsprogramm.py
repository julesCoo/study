from libgeo import fmt_deg_str, from_deg
from lib3d import Mat3
from libsphere import SphereCoords

"""
Input data
"""

# Positions of three measurement stations using latitude/longitude
# (given in gradians, converted to radians here).
#   P1: Fort Davis, TX
#   P2: Mammoth Lakes, CA
#   P3: Columbus, OH
b1 = from_deg(30, 38)
l1 = from_deg(-103, 57)

b2 = from_deg(37, 38)
l2 = from_deg(-118, 56)

b3 = from_deg(40)
l3 = from_deg(-83)

# Displacements of the original positions have been measured for the
# first two stations, given as delta latitude/longitude.
db1 = from_deg(0, 0, -0.02033)
dl1 = from_deg(0, 0, 0.01034)

db2 = from_deg(0, 0, -0.02506)
dl2 = from_deg(0, 0, 0.01119)


"""
Convert to 3D vectors
"""

# Convert the lat/lon positions into cartesian coordinates.
#   p: position before rotation
#   r: position after rotation

p1 = SphereCoords(b1, l1).to_vec3()
p2 = SphereCoords(b2, l2).to_vec3()
p3 = SphereCoords(b3, l3).to_vec3()

r1 = SphereCoords(b1 + db1, l1 + dl1).to_vec3()
r2 = SphereCoords(b2 + db2, l2 + dl2).to_vec3()

"""
Find rotation axis
"""

# Calculate displacement vectors of the two stations within the rotational plane.
dv1 = r1 - p1
dv2 = r2 - p2

# Calculate the rotational axis as the perpendicular of the two displacement vectors.
axis = dv1.cross(dv2).normalized()
scalar_triple_product = axis.cross(p1).dot(r1)
if scalar_triple_product < 0:
    axis = -axis

axis_polar = SphereCoords.from_vec3(axis)

"""
Find rotation angle
"""

# Project the points onto the rotation axis to find the center of rotation.
# Since the two measurement stations might not be inside the same rotational plane (e.g.
# they are on different heights along the rotational axis), we have to calculate different
# centers for each point.
c1 = p1.projected_on(axis)
c2 = p2.projected_on(axis)

# Also project the rotated points onto the axis for scrutiny. They should be identical to the
# center of the non-rotated point!
c1_ = r1.projected_on(axis)
c2_ = r2.projected_on(axis)
assert (c1 - c1_).length() < 1e-6
assert (c2 - c2_).length() < 1e-6

# Using two vectors going from the center to the two point position (original and reported),
# we can find the angle of rotation as the angle between these two vectors.
cp1 = p1 - c1
cp1_ = r1 - c1
w1 = cp1.angle_between(cp1_)

# To check that the rotation is the same for both points (which we expect if the rotating body
# is rigid), calculate the angle for the second point and compare.
cp2 = p2 - c2
cp2_ = r2 - c2
w2 = cp2.angle_between(cp2_)
assert abs(w1 - w2) < 1e-6

# Angles deviate by about 1%. Calculate the average and work with that to minimize the error.
w = (w1 + w2) / 2

"""
Extrapolate rotation
"""

# Now that we know the rotation over the span of 5 years, we can extrapolate it into the future.
w_a = w / 5
w_5 = w_a * 5
w_10 = w_a * 10

# Check how far Columbus would move in 10 years
R10 = Mat3.from_axis_and_angle(axis, w_10, infinitesimal=True)
r3 = R10 * p3

# This gives us the 3D coordinates of Columbus in 10 years.
# Transform them back into spherical coordinates.
b3_, l3_, _ = SphereCoords.from_vec3(r3)

# Calculate the difference between the original and the predicted position,
# and output it in gradians.
db3 = b3_ - b3
dl3 = l3_ - l3

"""
Backward Rotation (for verification)
"""

R5 = Mat3.from_axis_and_angle(axis, w_5, infinitesimal=True)
r1_ = R5 * p1
r2_ = R5 * p2
assert r1.equals(r1_)
assert r2.equals(r2_)

b1_, l1_, _ = SphereCoords.from_vec3(r1_)
b2_, l2_, _ = SphereCoords.from_vec3(r2_)

db1_ = b1_ - b1
dl1_ = l1_ - l1
db2_ = b2_ - b2
dl2_ = l2_ - l2

"""
Output
"""

print("DMS converted to radians [with delta]:")
print(f"  b1: {b1:.5f} [{1e8*db1:.5f} * 1e-8]")
print(f"  l1: {l1:.5f} [{1e8*dl1:.5f} * 1e-8]")
print(f"  b2: {b2:.5f} [{1e8*db2:.5f} * 1e-8]")
print(f"  l2: {l2:.5f} [{1e8*dl2:.5f} * 1e-8]")
print(f"  b3: {b3:.5f}")
print(f"  l3: {l3:.5f}")
print("")
print("Points in 3d space [with delta]:")
print(f"  p1: {p1.fmt(5)} [{((r1 - p1)*1e8).fmt(5)} * 1e-8]")
print(f"  p2: {p2.fmt(5)} [{((r2 - p2)*1e8).fmt(5)} * 1e-8]")
print(f"  p3: {p3.fmt(5)}")
print("")
print("Rotational axis:")
print(f"  scalar triple product: {scalar_triple_product:.5e}")
print(f"  axis: {axis.fmt(5)}")
print(f"  axis polar (rad): {axis_polar.phi:.13f}, {axis_polar.lam:.13f}")
print(f"  axis polar: {axis_polar.fmt(5)}")
print("")
print("Rotational center:")
print(f"  c1 : {c1.fmt(5)}")
print(f"  c1': {c1_.fmt(5)}")
print(f"  c2 : {c2.fmt(5)}")
print(f"  c2': {c2_.fmt(5)}")
print("")
print("Angle of rotation (rad):")
print(f"  w1: {(w1*1e8):.5f} * 1e-8")
print(f"  w2: {(w2*1e8):.5f} * 1e-8")
print(f"   w: {(w*1e8):.5f} * 1e-8")
print("")
print("Extrapolated angles (rad):")
print(f"   w5: {(w_5*1e8):.5f} * 1e-8")
print(f"  w10: {(w_10*1e8):.5f} * 1e-8")
print("")
print("Rotational matrix (10 years, * 1e-8):")
print(((R10 - Mat3.identity()) * 1e8).fmt(5, 2))
print("")
print("Columbus in 10 years:")
print(f"  dr3: {((r3 - p3)*1e8).fmt(5)} * 1e-8")
print(f"  b3: {b3:.5f} [{1e8*db3:.5f} * 1e-8]")
print(f"  l3: {l3:.5f} [{1e8*dl3:.5f} * 1e-8]")
print(f" db3: {fmt_deg_str(db3, precision=5)}")
print(f" dl3: {fmt_deg_str(dl3, precision=5)}")
print("")
print("Angle of rotation (DMS):")
print(f"  wa: {fmt_deg_str(w_a,precision=5)}")
print(f"  w5: {fmt_deg_str(w_5,precision=5)}")
print(f" w10: {fmt_deg_str(w_10,precision=5)}")
print("")
print("Verification: Rotational matrix (5 years, * 1e-8):")
print(((R5 - Mat3.identity()) * 1e8).fmt(5, 2))
print()
print("Verification: Displacement in DMS:")
print(f"     db1: {fmt_deg_str(db1,precision=5)}")
print(f"     dl1: {fmt_deg_str(dl1,precision=5)}")
print(f"     db2: {fmt_deg_str(db2,precision=5)}")
print(f"     dl2: {fmt_deg_str(dl2,precision=5)}")
