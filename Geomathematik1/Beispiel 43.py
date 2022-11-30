from math import degrees
from lib3d.Algorithms import Vorwärtsschnitt
from lib3d.Vector import Vec3

# Satellite moves on circle in space
# Time from x0->x1 and x1->x2 is equal

x0 = Vec3(2, 1, 1)
x1 = Vec3(2, 7, 1) / 3
x2 = Vec3(-2, 5, 5) / 3

# x0x1 and x1x2 are secants on a circle.
# Since both are inside the rotational plane, the rotation_axis is perpendicular to both.
x0x1 = x1 - x0
x1x2 = x2 - x1
rotation_axis = x0x1.cross(x1x2)

# To find the center xm of the rotation, cast lines from the center of the secants.
# Those lines must be within the rotational plane, so they are perpendicular to the rotation_axis and the secant.
# Both lines should intersect at the center of the circle.
A = x0 + x0x1 / 2
B = x1 + x1x2 / 2
AC = x0x1.cross(rotation_axis)
BC = x1x2.cross(rotation_axis)
rotation_center = Vorwärtsschnitt(A, AC, B, BC)

# Also the angle of rotation is the angle between the secant bisectors.
angle = AC.angle_between(BC)

print(f"Rotation axis: {rotation_axis}")
print(f"Rotation center: {rotation_center}")
print(f"Rotation angle: {angle:.4f} ({degrees(angle):.4f}°)")
