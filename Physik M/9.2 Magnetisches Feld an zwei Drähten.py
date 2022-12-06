from math import pi

from lib.electrostatic import lorentz
from lib.vector import Vec3

# Magnetic Field Constant
mu0 = 4 * pi * 1e-7


def B(
    # position where the magnetic field is calculated
    pos: Vec3,
    # one position on the conductor
    conductor_dir: Vec3,
    # direction of the conductor
    conductor_pos: Vec3,
    # current through the conductor in Ampere
    conductor_current: Vec3,
) -> Vec3:
    # project `pos` onto the conductor
    pos_proj = conductor_pos + (pos - conductor_pos).dot(conductor_dir) * conductor_dir

    # calculate the normal on the conductor from `pos`
    conductor_normal = pos_proj - pos

    # calculate the direction of the magnetic field (right hand rule)
    field_dir = conductor_normal.cross(conductor_dir).normalized()

    # calculate the magnetic field vector
    dist = conductor_normal.length()
    return field_dir * mu0 * conductor_current / (2 * pi * dist)


B1 = B(
    pos=Vec3(0, 0, 0),
    conductor_dir=Vec3(0, 0, -1),
    conductor_pos=Vec3(-0.01, -0.01, -0.01),
    conductor_current=0.004,
)

B2 = B(
    pos=Vec3(0, 0, 0),
    conductor_dir=Vec3(0, -1, 0),
    conductor_pos=Vec3(0.01, 0.01, 0.01),
    conductor_current=0.009,
)

# print(B1 + B2)


print(
    lorentz(
        electricField=Vec3(0, 0, 0),
        magneticField=B(
            pos=Vec3(0, 0.01, 0),
            conductor_dir=Vec3(1, 0, 0),
            conductor_pos=Vec3(0, 0, 0),
            conductor_current=0.098,
        ),
        electronSpeed=Vec3(421, 357, 426),
    )
)
