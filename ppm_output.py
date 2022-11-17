from model import *
import time
import numpy as np
from utils import *

GL_sample_num = 40
# GL_ray_mode = RayMode.Direct
GL_ray_mode = RayMode.Random
GL_max_depth = 40


def output_train(file):
    nx = 200
    ny = 100
    write_prefix(file, nx, ny)
    # file.write("P3\n{} {}\n255\n".format(nx, ny))
    for j in range(ny-1, -1, -1):
        for i in range(nx):
            pixel_color = color(np.array([i/nx, j/ny, 0.25]))
            write_color(file, pixel_color)


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


def ray_color(r: Ray, world: hittable,  depth: int) -> color:
    if depth <= 0:
        return color(np.array([0, 0, 0]))
    hit_any, rec = world.hit(r, 0.001, float('inf'))
    if hit_any:
        # print(rec.normal)
        # target = rec.p+rec.normal+random_unit_vector()
        scatter_flag, attenuation, scattered = rec.mat_ptr.scatter(r, rec)
        if scatter_flag:
            return color(ray_color(scattered, world, depth-1).vec()*attenuation.vec())
        # target = rec.p+random_in_hemishpere(rec.normal)
        # return ray_color(Ray(rec.p, target-rec.p), world, depth-1)*0.5
        # return color(0.5*(np.array([1, 1, 1])+rec.normal.vec()))
    unit_direction = r.direction().unit()
    t = 0.5*(unit_direction.y()+1.0)
    return color(np.array([1, 1, 1])*(1-t)+np.array([0.5, 0.7, 1.0])*t)


def gen_at_pos(file, i: int, j: int, world, samples_per_pixel, image_width, image_height, max_depth, cam):
    pixel_color = color(np.array([0, 0, 0]))
    if GL_ray_mode == RayMode.Direct:
        u = i/(image_width-1)
        v = j/(image_height-1)
        r = cam.get_ray(u, v)
        pixel_color += ray_color(r, world, max_depth)
        write_color(file, pixel_color)
    elif GL_ray_mode == RayMode.Random:
        for _ in range(samples_per_pixel):
            u = (i+random_float())/(image_width-1)
            v = (j+random_float())/(image_height-1)
            r = cam.get_ray(u, v)
            pixel_color += ray_color(r, world, max_depth)
        write_color(file, pixel_color, samples_per_pixel)
    pass


def ground_viewer(file):

    # image
    aspect_ratio = 16/9
    image_width = 400
    image_height = int(image_width/aspect_ratio)
    samples_per_pixel = GL_sample_num
    max_depth = GL_max_depth

    # world
    world = hittable_list()
    material_ground = lambertion(color(np.array([0.8, 0.8, 0.0])))
    material_center = lambertion(color(np.array([0.7, 0.3, 0.3])))
    material_left = metal(color(np.array([0.8, 0.8, 0.8])))
    material_right = metal(color(np.array([0.8, 0.6, 0.2])))

    world.add(sphere(point3(np.array([0, -100.5, -1])), 100, material_ground))
    world.add(sphere(point3(np.array([0, 0, -1])), 0.5, material_center))
    world.add(sphere(point3(np.array([-1, 0, -1])), 0.5, material_left))
    world.add(sphere(point3(np.array([1, 0, -1])), 0.5, material_right))

    # camera
    viewport_height = 2
    viewport_width = aspect_ratio*viewport_height
    focal_length = 1
    cam = Camera()

    origin = point3(np.array([0, 0, 0]))
    horizontal = Vec3(np.array([viewport_width, 0, 0]))
    vertical = Vec3(np.array([0, viewport_height, 0]))
    lower_left_corner = origin-horizontal/2 -\
        vertical/2-Vec3(np.array([0, 0, focal_length]))

    # render
    write_prefix(file, image_width, image_height)
    for j in range(image_height-1, -1, -1):
        print('j = {}'.format(j))
        for i in range(image_width):
            gen_at_pos(file=file, i=i, j=j, world=world, samples_per_pixel=samples_per_pixel,
                       image_width=image_width, image_height=image_height, max_depth=max_depth, cam=cam)


def gen(file) -> float:
    print('gen started')
    start_time = time.time()
    ground_viewer(file)
    end_time = time.time()
    print('gen finished')
    return end_time-start_time


def main():
    mid_name = 'material_4'
    if GL_ray_mode == RayMode.Direct:
        file_name = './output/{}_direct.ppm'.format(mid_name)
    elif GL_ray_mode == RayMode.Random:
        file_name = './output/{}_random_{}.ppm'.format(mid_name, GL_sample_num)
    time_list = []
    with open(file_name, 'w') as file:
        time_list.append(gen(file))
    for duration in time_list:
        print('time usage = {:.2f} s'.format(duration))
    print('out file name = {}'.format(file_name))
    return


if __name__ == '__main__':
    main()
