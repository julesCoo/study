# import math
from math import tau, degrees
from lib3d.Matrix import Mat3
from lib3d.Vector import Vec3

rotation_axis = Vec3(-1.1, -2.0, 3.5)
rotation_period = 12 * 60 * 60  # 12 hours in seconds

# A position of the satellite at unknown time, in LE (Length Equivalence)
x = Vec3(-1.4, -2.7, 2.8)

# In 3 seconds, the satellite moves this angle (in radians)
angle = tau * 3 / rotation_period

r = x.distance_to(Mat3.from_vector_as_projection(rotation_axis) * x)

R1 = Mat3.from_axis_and_angle(rotation_axis, angle, infinitesimal=True)
y1 = R1 * x
d1 = (y1 - x).length()

R2 = Mat3.from_axis_and_angle(rotation_axis, angle, infinitesimal=False)
y2 = R2 * x
d2 = (y2 - x).length()

d3 = angle * r

print(f"rotation angle:        {degrees(angle)}°")
print(f"distance (simplified): {d1} LE")
print(f"distance (full):       {d2} LE")
print(f"distance (exact):      {d3} LE")
print(f"difference:            {d1 - d2} LE")

# # This gives us the radius of the circle in LE
# origin = Vec3(0, 0, 0)
# rotation_radius = (x - origin).length()

# # The length of the arc that the satellite moved in 3 seconds, deduced from angle and radius
# arc_length = rotation_radius * angle


# # TODO: Why is this so different?
# print(f"arc length: {arc_length} LE")

# # TODO: Why is this not 0?
# print("{}°".format(math.degrees((x - origin).angle_between(rotation_axis))))

# # => Satellite does NOT circle around origin, but around a some point on the rotation axis
