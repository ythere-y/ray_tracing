import numpy as np
import os


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


def gen_map_file_name(file_prefix: str, idx: int):
    return '{}_{}.mid'.format(file_prefix, idx)


def gen_map_file(file_prefix: str, idx: int):
    with open('{}_{}.mp'.format(file_prefix, idx), 'w') as file:
        return file


def reduce_files(map_prefix: str, task_name: str, map_range: int, reduce_prefix: str, image_width: int, image_height: int):
    out_file_name = '{}.ppm'.format(reduce_prefix)
    with open(out_file_name, 'w') as out_file:
        write_prefix(out_file, image_width, image_height)
        for i in range(map_range-1, -1, -1):
            in_file_name = gen_map_file_name(
                map_prefix.format(task_name), i)
            with open(in_file_name, 'r') as in_file:
                in_str = in_file.read()
                out_file.write(in_str)
                in_file.close()
            os.unlink(in_file_name)
            print('try to remove file = ', in_file_name)
        out_file.close()

    print('out file = ', out_file_name)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
