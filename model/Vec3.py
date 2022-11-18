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

    def dot(self, other) -> float:
        return self.e.dot(other.vec())

    def cross(self, other):
        return np.cross(self.e, other.vec())

    def unit(self):
        len = self.length()
        return Vec3(self.e / len)

    def __str__(self):
        return '{}_{}_{}'.format(self.e[0], self.e[1], self.e[2])

    def random():
        return Vec3(utils.random_array())

    def random_range(min: float, max: float):
        return Vec3(utils.random_array_range(min, max))

    def near_zero(self) -> bool:
        s = 1e-8
        return (self.e[0] < s) and (self.e[1] < s) and (self.e[2] < s)


class color(Vec3):
    def __str__(self) -> str:
        out_vec = self.vec()*255.999
        return "{} {} {}\n".format(int(out_vec[0]),
                                   int(out_vec[1]), int(out_vec[2]))
    pass


class point3(Vec3):
    pass


def write_color(file, color: color, samples_per_pixel: int = 1):
    out_vec = utils.gamma_x(color.vec(), 2, 1/samples_per_pixel)
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


def random_in_unit_sphere() -> Vec3:
    while (True):
        p = Vec3.random_range(-1, 1)
        if p.length_squared() >= 1:
            continue
        return p


def random_unit_vector() -> Vec3:
    return random_in_unit_sphere().unit()


def random_in_hemishpere(normal: Vec3) -> Vec3:
    in_unit_shpere = random_in_unit_sphere()
    if in_unit_shpere.dot(normal) > 0.0:
        return in_unit_shpere
    return -in_unit_shpere


def reflect(v: Vec3, u: Vec3) -> Vec3:
    return v-u*(v.dot(u)*2)


def refract(uv: Vec3, n: Vec3, etai_over_etai: float) -> Vec3:
    cos_theta = min(-uv.dot(n), 1.0)
    r_out_prep = (uv+n*cos_theta)*etai_over_etai
    r_out_parallel = -n*(np.sqrt(np.abs(1.0-r_out_prep.length_squared())))
    return r_out_prep+r_out_parallel


def rgb(r, g, b) -> np.array:
    return np.array([r/255, g/255, b/255])


class favor_color:
    Beige = color(rgb(240, 202, 163))
    Pink = color(rgb(192, 96, 161))
    Purple = color(rgb(59, 24, 95))
    Navy = color(rgb(0, 0, 92))

    Earth = color(rgb(40, 84, 48))
    Nature = color(rgb(95, 141, 78))
    Green = color(rgb(164, 190, 123))

    Red = color(rgb(220, 53, 53))
    Orange = color(rgb(244, 157, 26))
    Yellow = color(rgb(255, 225, 93))

    White = color(rgb(255, 255, 255))
    Black = color(rgb(0, 0, 0))
    Teal = color(rgb(160, 228, 203))
