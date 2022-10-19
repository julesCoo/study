from Vector import *

electricConstant = 8.854e-12  # eps0
electronCharge = -1.602176487e-19
electronMass = 9.10938215e-31

# Returns the coloumb force being applied to an electron at
# pos1 by an electron at pos2
def coulomb(pos1: Vec3, pos2: Vec3):
    r21 = -pos2 + pos1
    force = electronCharge**2 / (4 * math.pi * electricConstant * r21.length() ** 2)
    return r21.normalized() * force


# Returns the force being applied to an electron at
def lorentz(electricField: Vec3, magneticField: Vec3, electronSpeed: Vec3):
    return (electricField + electronSpeed.cross(magneticField)) * electronCharge


print(
    lorentz(
        electronSpeed=Vec3(-9e5, 6e5, 2e5),
        electricField=Vec3(-5e3, -2e3, 6e3),
        magneticField=Vec3(2, 9, -5),
    )
)
