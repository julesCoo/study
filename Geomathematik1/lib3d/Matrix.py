from __future__ import annotations
from typing import Union
from math import sin, cos, acos
from lib3d.Vector import Vec3


class Mat3:
    xx: float
    xy: float
    xz: float
    yx: float
    yy: float
    yz: float
    zx: float
    zy: float
    zz: float

    def __init__(
        self,
        x: tuple[float, float, float],
        y: tuple[float, float, float],
        z: tuple[float, float, float],
    ):
        self.xx, self.xy, self.xz = x
        self.yx, self.yy, self.yz = y
        self.zx, self.zy, self.zz = z

    def __str__(self) -> str:
        return (
            f"|{self.xx:7.4f}, {self.xy:7.4f}, {self.xz:7.4f}|\n"
            + f"|{self.yx:7.4f}, {self.yy:7.4f}, {self.yz:7.4f}|\n"
            + f"|{self.zx:7.4f}, {self.zy:7.4f}, {self.zz:7.4f}|"
        )

    def __add__(self, other: Mat3) -> Mat3:
        return Mat3(
            (self.xx + other.xx, self.xy + other.xy, self.xz + other.xz),
            (self.yx + other.yx, self.yy + other.yy, self.yz + other.yz),
            (self.zx + other.zx, self.zy + other.zy, self.zz + other.zz),
        )

    def __sub__(self, other: Mat3) -> Mat3:
        return Mat3(
            (self.xx - other.xx, self.xy - other.xy, self.xz - other.xz),
            (self.yx - other.yx, self.yy - other.yy, self.yz - other.yz),
            (self.zx - other.zx, self.zy - other.zy, self.zz - other.zz),
        )

    def __mul__(self, other: Union[float, Vec3, Mat3]) -> Vec3:
        if isinstance(other, float):
            return Mat3(
                (self.xx * other, self.xy * other, self.xz * other),
                (self.yx * other, self.yy * other, self.yz * other),
                (self.zx * other, self.zy * other, self.zz * other),
            )
        if isinstance(other, Vec3):
            (x, y, z) = other
            return Vec3(
                self.xx * x + self.xy * y + self.xz * z,
                self.yx * x + self.yy * y + self.yz * z,
                self.zx * x + self.zy * y + self.zz * z,
            )
        elif isinstance(other, Mat3):
            return self @ other
        else:
            raise TypeError("Invalid type")

    def __matmul__(self, other: Mat3) -> Mat3:
        return Mat3(
            (
                self.xx * other.xx + self.xy * other.yx + self.xz * other.zx,
                self.xx * other.xy + self.xy * other.yy + self.xz * other.zy,
                self.xx * other.xz + self.xy * other.yz + self.xz * other.zz,
            ),
            (
                self.yx * other.xx + self.yy * other.yx + self.yz * other.zx,
                self.yx * other.xy + self.yy * other.yy + self.yz * other.zy,
                self.yx * other.xz + self.yy * other.yz + self.yz * other.zz,
            ),
            (
                self.zx * other.xx + self.zy * other.yx + self.zz * other.zx,
                self.zx * other.xy + self.zy * other.yy + self.zz * other.zy,
                self.zx * other.xz + self.zy * other.yz + self.zz * other.zz,
            ),
        )

    def transpose(self) -> Mat3:
        return Mat3(
            (self.xx, self.yx, self.zx),
            (self.xy, self.yy, self.zy),
            (self.xz, self.yz, self.zz),
        )

    def invert(self) -> Mat3:
        # Calculate the determinant
        det = (
            self.xx * self.yy * self.zz
            + self.xy * self.yz * self.zx
            + self.xz * self.yx * self.zy
            - self.xx * self.yz * self.zy
            - self.xy * self.yx * self.zz
            - self.xz * self.yy * self.zx
        )

        # Calculate the inverse
        return Mat3(
            (
                (self.yy * self.zz - self.yz * self.zy) / det,
                (self.xz * self.zy - self.xy * self.zz) / det,
                (self.xy * self.yz - self.xz * self.yy) / det,
            ),
            (
                (self.yz * self.zx - self.yx * self.zz) / det,
                (self.xx * self.zz - self.xz * self.zx) / det,
                (self.xz * self.yx - self.xx * self.yz) / det,
            ),
            (
                (self.yx * self.zy - self.yy * self.zx) / det,
                (self.xy * self.zx - self.xx * self.zy) / det,
                (self.xx * self.yy - self.xy * self.yx) / det,
            ),
        )

    def axis_and_rotation(self) -> tuple[Vec3, float]:
        # Rotate an arbitrary vector x into vector y
        x = Vec3(0, 0, 1)
        y = self * x

        # Take the (normalized) vector between x and y, which lies in the rotation plane
        h = (y - x).normalized()

        # Rotate this vector, which now gets us two clamping vectors in the rotation plane
        h2 = self * h

        # The cross product of these two vectors is the rotation axis (perpendicular to both in plane)
        axis = h.cross(h2).normalized()

        # The dot product of the (normalized) clamping vectors is cos(angle)
        angle = acos(h2.dot(h))

        return axis, angle

    @classmethod
    def identity(cls) -> Mat3:
        return cls((1, 0, 0), (0, 1, 0), (0, 0, 1))

    @classmethod
    def from_euler_angles(cls, phi: float, psi: float, theta: float):
        return cls(
            (
                cos(phi) * cos(psi) - sin(phi) * sin(psi) * cos(theta),
                -cos(phi) * sin(psi) - sin(phi) * cos(psi) * cos(theta),
                sin(phi) * sin(theta),
            ),
            (
                sin(phi) * cos(psi) + cos(phi) * sin(psi) * cos(theta),
                -sin(phi) * sin(psi) + cos(phi) * cos(psi) * cos(theta),
                -cos(phi) * sin(theta),
            ),
            (
                sin(psi) * sin(theta),
                cos(psi) * sin(theta),
                cos(theta),
            ),
        )

    @classmethod
    def from_axis_and_angle(cls, axis: Vec3, angle: float) -> Mat3:
        (x, y, z) = axis
        proj = Mat3(
            (x * x, x * y, x * z),
            (y * x, y * y, y * z),
            (z * x, z * y, z * z),
        )

        A = Mat3(
            (0, -z, y),
            (z, 0, -x),
            (-y, x, 0),
        )

        I = Mat3.identity()

        return proj + (I - proj) * cos(angle) + A * sin(angle)
