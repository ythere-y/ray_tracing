import os
import traceback
import model
from model import color, Ray, point3, Vec3, hittable, hit_record, hittable_list, sphere

import numpy as np
from utils import write_prefix


def output_train(file):
    nx = 200
    ny = 100
    write_prefix(file, nx, ny)
    # file.write("P3\n{} {}\n255\n".format(nx, ny))
    for j in range(ny-1, -1, -1):
        for i in range(nx):
            pixel_color = color(np.array([i/nx, j/ny, 0.25]))
            model.write_color(file, pixel_color)


def hit_sphere(center: point3, radius: float, r: Ray) -> bool:
    oc = r.origin()-center
    a = r.direction().length_squared()
    half_b = oc.dot(r.direction())
    c = oc.dot(oc)-radius*radius
    discriminant = half_b*half_b-a*c
    if discriminant < 0:
        return -1.0
    else:
        return (-half_b-np.sqrt(discriminant))/a


def ray_color(r: Ray, world: hittable) -> color:
    hit_any, rec = world.hit(r, 0, float('inf'))
    if hit_any:
        print(rec.normal)
        return color(0.5*(np.array([1, 1, 1])+rec.normal.vec()))
    unit_direction = r.direction().unit()
    t = 0.5*(unit_direction.y()+1.0)
    return color(np.array([1, 1, 1])*(1-t)+np.array([0.5, 0.7, 1.0])*t)


def sky_viewer(file):
    aspect_ratio = 16/9
    image_width = 400
    image_height = int(image_width/aspect_ratio)

    viewport_height = 2
    viewport_width = aspect_ratio*viewport_height
    focal_length = 1

    origin = point3(np.array([0, 0, 0]))
    horizontal = Vec3(np.array([viewport_width, 0, 0]))
    vertical = Vec3(np.array([0, viewport_height, 0]))
    lower_left_corner = origin-horizontal/2 -\
        vertical/2-Vec3(np.array([0, 0, focal_length]))

    write_prefix(file, image_width, image_height)
    for j in range(image_height-1, -1, -1):
        for i in range(image_width):
            u = i/(image_width+1)
            v = j/(image_height-1)
            r = Ray(origin, lower_left_corner+horizontal*u+vertical*v-origin)
            pixel_color = ray_color(r)
            model.write_color(file, pixel_color)


def ground_viewer(file):

    # image
    aspect_ratio = 16/9
    image_width = 400
    image_height = int(image_width/aspect_ratio)

    # world
    world = hittable_list()
    world.add(sphere(point3(np.array([0, 0, -1])), 0.5))
    world.add(sphere(point3(np.array([0, -100.5, -1])), 100))

    # camera
    viewport_height = 2
    viewport_width = aspect_ratio*viewport_height
    focal_length = 1

    origin = point3(np.array([0, 0, 0]))
    horizontal = Vec3(np.array([viewport_width, 0, 0]))
    vertical = Vec3(np.array([0, viewport_height, 0]))
    lower_left_corner = origin-horizontal/2 -\
        vertical/2-Vec3(np.array([0, 0, focal_length]))

    # render
    write_prefix(file, image_width, image_height)
    for j in range(image_height-1, -1, -1):
        for i in range(image_width):
            u = i/(image_width+1)
            v = j/(image_height-1)
            r = Ray(origin, lower_left_corner+horizontal*u+vertical*v-origin)
            pixel_color = ray_color(r, world)
            model.write_color(file, pixel_color)


def gen(file):
    print('gen started')
    ground_viewer(file)

    print('gen finished')


def main():
    file_name = './output/see_ground.ppm'
    # if not os.path.exists(file_name):
    #     open(file_name, 'w').close()
    with open(file_name, 'w') as file:
        gen(file)
    # gen(None)
    return


if __name__ == '__main__':
    main()
