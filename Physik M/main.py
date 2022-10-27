from forces import gravity
from vector import *


print(
    gravity(
        mass1=3e24,
        mass2=2e21,
        pos1=Vec3(3e8, 4e7, -7e8),
        pos2=Vec3(-9e8, -7e6, 2e7),
    )
)
