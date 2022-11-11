import numpy as np


class Vec3:
    def __init__(self, arr) -> None:
        self.e = arr

    def x(self) -> float:
        return self.e[0]

    def y(self) -> float:
        return self.e[1]

    def z(self) -> float:
        return self.e[2]

    def vec(self) -> np.array:
        return self.e

    def __add__(self, other):
        return Vec3(self.e + other.vec())

    def __sub__(self, other):
        return Vec3(self.e - other.vec())

    def __truediv__(self, other):
        return Vec3(self.e / other.vec())

    def __mul__(self, other):
        return Vec3(self.e * other.vec())

    def __getitem__(self, idx: int):
        return self.e[idx]

    def __setitem__(self, idx: int, val: float):
        self.e[idx] = val

    def length(self) -> float:
        return np.linalg.norm(self.e)

    def length_squared(self) -> float:
        return self.e.dot(self.e)

    def dot(self, other):
        return self.e.dot(other.vec())

    def cross(self, other):
        return np.cross(self.e, other.vec())

    def unit(self):
        return self.e/self.length()


class color(Vec3):
    def __str__(self) -> str:

        out_vec = self.vec()*255.999
        return "{} {} {}\n".format(int(out_vec[0]),
                                   int(out_vec[1]), int(out_vec[2]))
    pass


class point3(Vec3):
    pass


def write_color(file, color):
    if file == None:
        print(color)
    else:
        file.write(str(color))


def write_prefix(file, width, height):
    if file == None:
        print("P3\n{} {}\n255\n".format(width, height), end='')
    else:
        file.write("P3\n{} {}\n255\n".format(width, height))
