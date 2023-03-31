from copy import deepcopy


# Base class
class Vector:
    # Private copy of the vector values
    _values: list[float]

    def __init__(self, values: list[float]):
        # On initialization, make a deep copy of the values
        self._values = deepcopy(values)

    def __str__(self) -> str:
        return str(self._values)

    def __len__(self) -> int:
        return len(self._values)

    # Individual values can be accessed by index
    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._values[index] = value

    # Vectors of the same length can be added and subtracted
    def __add__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise ValueError(f"length mismatch {len(self)} != {len(other)}")
        return Vector([x + y for x, y in zip(self._values, other._values)])

    def __sub__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise ValueError(f"length mismatch {len(self)} != {len(other)}")
        return Vector([x - y for x, y in zip(self._values, other._values)])

    # Vectors can be added and subtracted in place
    def __iadd__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise ValueError(f"length mismatch {len(self)} != {len(other)}")
        self._values = [x + y for x, y in zip(self._values, other._values)]
        return self

    def __isub__(self, other: "Vector") -> "Vector":
        if len(self) != len(other):
            raise ValueError(f"length mismatch {len(self)} != {len(other)}")
        self._values = [x - y for x, y in zip(self._values, other._values)]
        return self

    def norm(self) -> float:
        """
        The norm of a vector is its length.
        """
        return sum([x**2 for x in self._values]) ** 0.5


class Vector3d(Vector):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        # Store values in base class
        super().__init__([x, y, z])

    # Read-Write properties for x, y and z (accesses the underlying base values)
    @property
    def x(self) -> float:
        return self[0]

    @property
    def y(self) -> float:
        return self[1]

    @property
    def z(self) -> float:
        return self[2]

    @x.setter
    def x(self, value: float) -> None:
        self[0] = value

    @y.setter
    def y(self, value: float) -> None:
        self[1] = value

    @z.setter
    def z(self, value: float) -> None:
        self[2] = value

    def cross_product(self, other: "Vector3d") -> "Vector3d":
        """
        The cross product of two vectors is a vector that is perpendicular to both of them.
        Its length is the area of the parallelogram spanned by the two vectors.
        """
        return Vector3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


# Test Code
if __name__ == "__main__":
    vec1 = Vector([1, 2, 3, 4])
    vec2 = Vector([10, 20, 30, 40])
    print(vec1[2])
    print(len(vec2))
    print(vec1 + vec2)
    vec3 = vec1 - vec2
    print(vec3.norm())
    vec4 = Vector3d(2, 3, 4)
    vec5 = Vector3d(5, 6, 7)
    vec6 = Vector3d.cross_product(vec4, vec5)
    print(len(vec6))
    print(vec6)
    print(vec6.norm())
    vec7 = Vector3d(z=5)
    vec7.y = 9
    vec8 = Vector([100, 200, 300])
    vec7 += vec8
    print(vec7)
    try:
        vec7 -= vec1
    except Exception as ex:
        print(ex)
