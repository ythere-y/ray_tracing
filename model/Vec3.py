import numpy as np
import utils


class Vec3:
    def __init__(self, arr: np.array = np.array([0, 0, 0])) -> None:
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

    def __neg__(self):
        return Vec3(-self.e)

    def __truediv__(self, other):
        return Vec3(self.e / other)

    def __mul__(self, other):
        return Vec3(self.e * other)

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
        len = self.length()
        return Vec3(self.e / len)

    def __str__(self):
        return '{}_{}_{}'.format(self.e[0], self.e[1], self.e[2])


class color(Vec3):
    def __str__(self) -> str:
        out_vec = self.vec()*255.999
        return "{} {} {}\n".format(int(out_vec[0]),
                                   int(out_vec[1]), int(out_vec[2]))
    pass


class point3(Vec3):
    pass


def write_color(file, color: color, samples_per_pixel: int = 1):
    scale = 1/samples_per_pixel
    out_vec = color.vec()*scale
    cl_min = 0.0
    cl_max = 0.999

    color_txt = utils.clamp_vec(out_vec, cl_min, cl_max)
    color_txt = color_txt*256
    write_out = '{} {} {}\n'.format(
        int(color_txt[0]), int(color_txt[1]), int(color_txt[2]))
    if file == None:
        print(write_out)
    else:
        file.write(write_out)
