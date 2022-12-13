import math
from lib3d import Mat3, Vec3

R1 = Mat3.from_axis_and_angle(
    axis=Vec3(2, 0, -1),
    angle=1 / 60 * math.tau / 360,  # 1 minute
    infinitesimal=True,
)

R2 = Mat3.from_axis_and_angle(
    axis=Vec3(-2, 1, 2),
    angle=2 / 60 * math.tau / 360,  # 2 minutes
    infinitesimal=True,
)

R = R1 @ R2
axis, angle = R.axis_and_angle()
print(f"axis: {axis}")
print(f"angle: {angle}°")


print("--- without infinitesimal ---")
R1 = Mat3.from_axis_and_angle(
    axis=Vec3(2, 0, -1),
    angle=1 / 60 * math.tau / 360,  # 1 minute
)

R2 = Mat3.from_axis_and_angle(
    axis=Vec3(-2, 1, 2),
    angle=2 / 60 * math.tau / 360,  # 2 minutes
)

R = R1 @ R2
axis, angle = R.axis_and_angle()
print(f"axis: {axis}")
print(f"angle: {angle}°")
