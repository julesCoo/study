from __future__ import annotations
from math import sqrt, sin, cos, acos, tau
from itertools import product


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return self.fmt()

    def fmt(self, precision: int = 3) -> str:
        return (
            f"({self.x:.{precision}f}, {self.y:.{precision}f}, {self.z:.{precision}f})"
        )

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        raise IndexError("index out of range")

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scale: float) -> Vec3:
        return Vec3(self.x * scale, self.y * scale, self.z * scale)

    def __rmul__(self, scale: float) -> Vec3:
        return self * scale

    def __rmul__(self, scale: float) -> Vec3:
        return self * scale

    def __truediv__(self, scale: float) -> Vec3:
        return Vec3(self.x / scale, self.y / scale, self.z / scale)

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def dot(self, other: Vec3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3) -> Vec3:
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> float:
        l = self.length()
        self.x /= l
        self.y /= l
        self.z /= l
        return l

    def normalized(self) -> Vec3:
        return self / self.length()

    def equals(self, other: Vec3, epsilon: float = 1e-6) -> bool:
        return (
            abs(self.x - other.x) < epsilon
            and abs(self.y - other.y) < epsilon
            and abs(self.z - other.z) < epsilon
        )

    def angle_between(self, other: Vec3) -> float:
        return acos(self.dot(other) / (self.length() * other.length()))

    def distance_to(self, other: Vec3) -> float:
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def projected_on(self, other: Vec3) -> Vec3:
        return other * (self.dot(other) / other.dot(other))


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

    def __repr__(self) -> str:
        return self.fmt()

    def fmt(self, precision=3, indent=0) -> str:
        sp = " " * indent
        fmt = f"{precision+4}.{precision}f"
        return (
            f"{sp}|{self.xx:{fmt}}, {self.xy:{fmt}}, {self.xz:{fmt}}|\n"
            + f"{sp}|{self.yx:{fmt}}, {self.yy:{fmt}}, {self.yz:{fmt}}|\n"
            + f"{sp}|{self.zx:{fmt}}, {self.zy:{fmt}}, {self.zz:{fmt}}|"
        )

    def __eq__(self, other: Mat3) -> bool:
        return (
            abs(self.xx - other.xx) < 1e-3
            and abs(self.xy - other.xy) < 1e-3
            and abs(self.xz - other.xz) < 1e-3
            and abs(self.yx - other.yx) < 1e-3
            and abs(self.yy - other.yy) < 1e-3
            and abs(self.yz - other.yz) < 1e-3
            and abs(self.zx - other.zx) < 1e-3
            and abs(self.zy - other.zy) < 1e-3
            and abs(self.zz - other.zz) < 1e-3
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

    def __mul__(self, other: float | Vec3 | Mat3):
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

    def determinate(self) -> float:
        return (
            self.xx * self.yy * self.zz
            + self.xy * self.yz * self.zx
            + self.xz * self.yx * self.zy
            - self.xx * self.yz * self.zy
            - self.xy * self.yx * self.zz
            - self.xz * self.yy * self.zx
        )

    def is_rotation(self) -> bool:
        return abs(self.determinate() - 1) < 1e-3 and self.transpose() == self.inverse()

    def transpose(self) -> Mat3:
        return Mat3(
            (self.xx, self.yx, self.zx),
            (self.xy, self.yy, self.zy),
            (self.xz, self.yz, self.zz),
        )

    def inverse(self) -> Mat3:
        det = self.determinate()
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

    def axis_and_angle(self) -> tuple[Vec3, float]:
        # Rotate an arbitrary vector x into vector y
        x = Vec3(0, 0, 1)
        y: Vec3 = self * x

        # Take the (normalized) vector between x and y, which lies in the rotation plane
        h = y - x

        # Rotate this vector, which now gets us two clamping vectors in the rotation plane
        h2 = self * h

        # The cross product of these two vectors is the rotation axis (perpendicular to both in plane)
        axis = h.cross(h2).normalized()

        # The dot product of the (normalized) clamping vectors is cos(angle)
        angle = h.angle_between(h2)

        return axis, angle

    def euler_angles(self) -> tuple[float, float, float]:
        for (flipTheta, flipPsi, flipPhi) in product(
            [False, True],
            [False, True],
            [False, True],
        ):
            theta = acos(self.zz)
            if flipTheta:
                theta = tau - theta

            psi = acos(self.zy / sin(theta))
            if flipPsi:
                psi = tau - psi

            phi = acos(-self.yz / sin(theta))
            if flipPhi:
                phi = tau - phi

            M = Mat3.from_euler_angles(theta, psi, phi)
            if M == self:
                return theta, psi, phi

        raise ValueError("No valid euler angles found")

    @classmethod
    def identity(cls) -> Mat3:
        return Mat3((1, 0, 0), (0, 1, 0), (0, 0, 1))

    @classmethod
    def projection(cls, axis: Vec3) -> Mat3:
        x, y, z = axis.normalized()
        return Mat3(
            (x * x, x * y, x * z),
            (y * x, y * y, y * z),
            (z * x, z * y, z * z),
        )

    @classmethod
    def axiator(cls, axis: Vec3) -> Mat3:
        x, y, z = axis.normalized()
        return Mat3(
            (0, -z, y),
            (z, 0, -x),
            (-y, x, 0),
        )

    @classmethod
    def from_axis_and_angle(
        cls,
        axis: Vec3,
        angle: float,
        infinitesimal: bool = False,
    ) -> Mat3:
        if infinitesimal:
            I = Mat3.identity()
            A = Mat3.axiator(axis) * angle
            return I + A
        else:
            I = Mat3.identity()
            P = Mat3.projection(axis)
            A = Mat3.axiator(axis)
            return P + (I - P) * cos(angle) + A * sin(angle)

    @classmethod
    def from_euler_angles(
        cls,
        theta: float,
        psi: float,
        phi: float,
        infinitesimal: bool = False,
    ) -> Mat3:
        if infinitesimal:
            return Mat3.identity() + Mat3(
                (0, -phi - psi, 0),
                (phi + psi, 0, -theta),
                (0, theta, 0),
            )
        else:
            return Mat3(
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


# Vorwärtsschnitt
def vws(
    A: Vec3,
    B: Vec3,
    AC: Vec3,
    BC: Vec3,
) -> Vec3:
    AB = B - A

    sAB = AC.dot(AB) / AC.dot(BC)
    C = A + sAB * AB

    ### Alternative:
    # sAC = AB.dot(AC) / AB.dot(BC)
    # C = A + sAC * AC

    return C
