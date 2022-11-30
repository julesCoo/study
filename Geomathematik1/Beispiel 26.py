from lib3d.Matrix import Mat3
from math import degrees

M = Mat3(
    (0.8584, 0.4723, 0.2004),
    (-0.2834, 0.7621, -0.5821),
    (-0.4277, 0.4429, 0.7880),
)
theta, psi, phi = M.euler_angles()

M2 = Mat3.from_euler_angles(theta, psi, phi)
(axis, angle) = M2.axis_and_rotation()

M3 = Mat3.from_axis_and_angle(axis, angle)
print(M3 - M)
print(M2 - M)

print(f"phi = {phi:.4f}, ({degrees(phi):.4f}°)")
print(f"psi = {psi:.4f}, ({degrees(psi):.4f}°)")
print(f"theta = {theta:.4f}, ({degrees(theta):.4f}°)")
print(f"angle = {angle:.4f}, ({degrees(angle):.4f}°)")
print(f"axis = {axis}")
