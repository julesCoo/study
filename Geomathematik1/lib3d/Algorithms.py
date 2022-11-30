from lib3d.Vector import Vec3


def Vorwärtsschnitt(A: Vec3, B: Vec3, AC: Vec3, BC: Vec3) -> Vec3:
    AB = B - A

    sAB = AC.dot(AB) / AC.dot(BC)
    C = A + sAB * AB

    ### Alternative:
    # sAC = AB.dot(AC) / AB.dot(BC)
    # C = A + sAC * AC

    return C
