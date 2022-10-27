from typing import Tuple
from Point import Point
from Angle import Angle


# Given a Point and an oriented angle + distance, returns another Point
def HA1(P: Point, nu: Angle, s: float) -> Point:
    return Point(P.x + s * nu.cos(), P.y + s * nu.sin())


# Returns oriented angle and distance from A to B
def HA2(A: Point, B: Point) -> Tuple[Angle, float]:
    dist = A.distance_to(B)
    angle = A.oriented_angle_to(B)
    return angle, dist
