from math import acos, sin, tau

from lib3d.RotationMatrix import RotationMatrix

M = [
    [0.8584, 0.4723, 0.2004],
    [-0.2834, 0.7621, -0.5821],
    [-0.4277, 0.4429, 0.7880],
]

theta = tau - acos(M[2][2])
phi = tau - acos(-M[1][2] / sin(theta))
psi = acos(M[2][1] / sin(theta))

M2 = RotationMatrix(phi, psi, theta)
(axis, angle) = M2.asAngleAndAxis()

print("phi =", phi)
print("psi =", psi)
print("theta =", theta)
print("axis =", axis)
print("angle =", angle)
