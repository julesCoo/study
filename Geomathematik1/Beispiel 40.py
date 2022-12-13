from math import radians, degrees
from lib3d.Matrix import Mat3
from lib3d.Vector import Vec3

axis = Vec3(2, -1, 0.5)
angle = radians(330)

R = Mat3.from_axis_and_angle(axis, angle)
print(R)

axis2, angle2 = R.axis_and_angle()
print(axis2 * axis.length())
print(degrees(angle2))
