import os
import traceback
import vec3
import numpy as np


def output_train(file):
    nx = 200
    ny = 100
    vec3.write_prefix(file, nx, ny)
    # file.write("P3\n{} {}\n255\n".format(nx, ny))
    for j in range(ny-1, -1, -1):
        for i in range(nx):
            pixel_color = vec3.color(np.array([i/nx, j/ny, 0.25]))
            vec3.write_color(file, pixel_color)


def gen(file):
    print('gen started')
    output_train(file)
    print('gen finished')


def main():
    file_name = './output/my_output2.ppm'
    # if not os.path.exists(file_name):
    #     open(file_name, 'w').close()
    with open(file_name, 'w') as file:
        gen(file)
    # gen(None)
    return


if __name__ == '__main__':
    main()
