import math
from lib.vector import Vec3

electricConstant = 8.854e-12  # eps0
electronCharge = -1.602176487e-19
electronMass = 9.10938215e-31

# Returns the coloumb force being applied to an electron at
# pos1 by an electron at pos2
# Returns the coloumb force of the particle at pos2!
def coulomb(
    pos1: Vec3,
    pos2: Vec3,
    charge1: float = electronCharge,
    charge2: float = electronCharge,
) -> Vec3:
    r21 = -pos2 + pos1
    distance = r21.normalize()

    # constant factor for electric fields
    scaleFactor = 1 / (4 * math.pi * electricConstant)

    # variable factors defined by charge and position of the two particles
    oomphFactor = charge1 * charge2 / (distance**2)

    return r21 * (oomphFactor * scaleFactor)


# Returns the force being applied to an electron at
def lorentz(electricField: Vec3, magneticField: Vec3, electronSpeed: Vec3):
    return (electricField + electronSpeed.cross(magneticField)) * electronCharge


class ElectricField:
    charges: tuple[float, Vec3] = []

    def add_point_charge(self, charge: float, position: Vec3):
        self.charges.append((charge, position))

    def get_potential(self, position: Vec3):
        potential = 0
        for charge, pos in self.charges:
            potential += charge / (
                4 * math.pi * electricConstant * (position - pos).length()
            )
        return potential
