from math import sin, cos, acos
from lib3d.Point import Point


class RotationMatrix:
    phi: float
    psi: float
    theta: float

    def __init__(self, phi, psi, theta):
        self.phi = phi
        self.psi = psi
        self.theta = theta

    def asMatrix(self):
        return [
            [
                cos(self.phi) * cos(self.psi)
                - sin(self.phi) * sin(self.psi) * cos(self.theta),
                -cos(self.phi) * sin(self.psi)
                - sin(self.phi) * cos(self.psi) * cos(self.theta),
                sin(self.phi) * sin(self.theta),
            ],
            [
                sin(self.phi) * cos(self.psi)
                + cos(self.phi) * sin(self.psi) * cos(self.theta),
                -sin(self.phi) * sin(self.psi)
                + cos(self.phi) * cos(self.psi) * cos(self.theta),
                -cos(self.phi) * sin(self.theta),
            ],
            [
                sin(self.psi) * sin(self.theta),
                cos(self.psi) * sin(self.theta),
                cos(self.theta),
            ],
        ]

    def asAngleAndAxis(self):
        x = Point(0, 0, 1)
        y = self * x
        h = y - x
        h.normalize()
        h_ = self * h
        axis = h_.cross(h)
        axis.normalize()
        angle = acos(h_.dot(h))
        return angle, axis

    def __mul__(self, point: Point) -> Point:
        mat = self.asMatrix()
        return Point(
            mat[0][0] * point.x + mat[0][1] * point.y + mat[0][2] * point.z,
            mat[1][0] * point.x + mat[1][1] * point.y + mat[1][2] * point.z,
            mat[2][0] * point.x + mat[2][1] * point.y + mat[2][2] * point.z,
        )
