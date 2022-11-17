import numpy as np


class RayMode:
    Direct = 'direct'
    Random = 'random'


def write_prefix(file, width, height):
    if file == None:
        print("P3\n{} {}\n255\n".format(width, height), end='')
    else:
        file.write("P3\n{} {}\n255\n".format(width, height))


def degree_to_radians(degrees: float) -> float:
    return np.deg2rad(degrees)


def random_float() -> float:
    return np.random.uniform(0, 1)


def random_float_range(min: float, max: float) -> float:
    return np.random.uniform(min, max)


def clamp(x: float, min: float, max: float) -> float:
    if x < min:
        return min
    elif x > max:
        return max
    return x


def clamp_vec(vec: np.array, min: float, max: float) -> np.array:
    for i in range(len(vec)):
        vec[i] = clamp(vec[i], min, max)
    return vec


def random_array() -> np.array:
    return np.array([random_float(), random_float(), random_float()])


def random_array_range(min: float, max: float) -> np.array:
    return np.array([random_float_range(min, max), random_float_range(min, max), random_float_range(min, max)])


def gamma_x(vec: np.array, x: int, scale: int):
    return pow(vec*scale, 1/x)


def gamma_2(vec: np.array) -> np.array:
    return np.sqrt(vec)
