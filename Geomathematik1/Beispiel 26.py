from math import acos, sin, tau

from lib3d.Matrix import Mat3

M = Mat3(
    (0.8584, 0.4723, 0.2004),
    (-0.2834, 0.7621, -0.5821),
    (-0.4277, 0.4429, 0.7880),
)

theta = tau - acos(M.zz)
phi = tau - acos(-M.yz / sin(theta))
psi = acos(M.zy / sin(theta))

M2 = Mat3.from_euler_angles(phi, psi, theta)
(axis, angle) = M2.axis_and_rotation()

M3 = Mat3.from_axis_and_angle(axis, angle)
print(M3 - M)
print(M2 - M)

print("phi =", phi)
print("psi =", psi)
print("theta =", theta)
print("axis =", axis)
print("angle =", angle)