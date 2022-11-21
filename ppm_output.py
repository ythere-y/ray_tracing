from model import *
import time
import numpy as np
from utils import *
import threading
import multiprocessing

GL_samples_per_pixel = 500
# GL_ray_mode = RayMode.Direct
GL_ray_mode = RayMode.Random
GL_max_depth = 50
GL_map_prefix = './output/mid/{}_map'
# GL_concurrency = False
GL_concurrency = True
GL_image_with = 1200
GL_ration = 3.0/2.0
GL_process_num = 6
GL_task_name = 'end_render'


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


def random_scene() -> hittable_list:
    world = hittable_list()
    ground_meterial = lambertion(favor_color.Grey)
    world.add(sphere(point3(np.array([0, -1000, 0])), 1000, ground_meterial))
    for a in range(-11, 11, 1):
        for b in range(-11, 11):
            choose_mat = random_float()
            center = point3(
                np.array([a+0.9*random_float(), 0.2, b+0.9*random_float()]))
            if (center-point3(np.array([4, 0.2, 0]))).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = favor_color.Random_twice()
                    sphere_material = lambertion(albedo)
                    world.add(sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = favor_color.Random(0.5, 1)
                    fuzz = random_float_range(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))
    material1 = dielectric(1.5)
    world.add(sphere(point3([0, 1, 0]), 1.0, material1))
    material2 = lambertion(favor_color.Beige)
    world.add(sphere(point3([-4, 1, 0]), 1.0, material2))
    material3 = metal(color(np.array([0.7, 0.6, 0.5])), 0.0)
    world.add(sphere(point3([4, 1, 0]), 1.0, material3))
    return world


def ray_color(r: Ray, world: hittable,  depth: int) -> color:
    if depth <= 0:
        return favor_color.Black
    hit_any, rec = world.hit(r, 0.001, float('inf'))
    if hit_any:
        scatter_flag, attenuation, scattered = rec.mat_ptr.scatter(r, rec)
        if scatter_flag:
            return color(ray_color(scattered, world, depth-1).vec()*attenuation.vec())
    # background
    unit_direction = r.direction().unit()
    t = 0.5*(unit_direction.y()+1.0)
    return color(favor_color.White.vec()*(1-t)+favor_color.Teal.vec()*t)


def gen_at_line(j: int, world, samples_per_pixel, image_width, image_height, max_depth, cam: Camera):
    with open(gen_map_file_name(GL_map_prefix.format(GL_task_name), j), 'w') as file:
        for i in range(image_width):
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
        file.close()


def build_target_name() -> str:
    run_mode = ''
    if GL_concurrency:
        run_mode = 'concurrency'
    else:
        run_mode = 'flow'
    task_name = GL_task_name
    ray_mode = ''
    sample_num = ''
    if GL_ray_mode == RayMode.Direct:
        ray_mode = 'dir'
        sample_num = '1'
    else:
        ray_mode = 'ran'
        sample_num = str(GL_samples_per_pixel)

    target_file_prefix = './output/{}/{}_{}_{}_{}'.format(
        run_mode, task_name, ray_mode, GL_image_with, sample_num)
    return target_file_prefix


def ground_viewer():
    # file_name
    target_file_prefix = build_target_name()

    # image
    # huge
    aspect_ratio = GL_ration
    image_width = GL_image_with
    image_height = int(image_width/aspect_ratio)
    samples_per_pixel = GL_samples_per_pixel
    max_depth = GL_max_depth

    # small test
    # aspect_ratio = 3.0/2.0
    # image_width = 120
    # image_height = int(image_width/aspect_ratio)
    # samples_per_pixel = 50
    # max_depth = 50

    # world
    world = random_scene()
    # # R = np.cos(np.pi/4)

    # world = hittable_list()
    # # material_left = lambertion(color(np.array([0, 0, 1])))
    # # material_right = lambertion(color(np.array([1, 0, 0])))
    # # world.add(sphere(point3(np.array([-R, 0, -1])), R, material_left))
    # # world.add(sphere(point3(np.array([R, 0, -1])), R, material_right))

    # material_ground = lambertion(favor_color.Purple)
    # material_center = lambertion(color(np.array([0.1, 0.2, 0.5])))
    # # material_center = dielectric(1.5)
    # # material_left = metal(color(np.array([0.8, 0.8, 0.8])), 0.3)
    # material_left = dielectric(1.5)
    # # material_right = metal(color(np.array([0.8, 0.6, 0.2])), 1.0)
    # material_right = metal(color(np.array([0.8, 0.6, 0.2])), 0.0)

    # world.add(
    #     sphere(point3(np.array([0, -100.5, -1])), 100, material_ground))
    # world.add(sphere(point3(np.array([0, 0, -1])), 0.5, material_center))
    # world.add(sphere(point3(np.array([-1, 0, -1])), 0.5, material_left))
    # world.add(sphere(point3(np.array([-1, 0, -1])), -0.45, material_left))
    # world.add(sphere(point3(np.array([1, 0, -1])), 0.5, material_right))

    # camera
    # look_from = point3(np.array([3, 3, 2]))
    # look_at = point3(np.array([0, 0, -1]))
    # vup = Vec3(np.array([0, 1, 0]))
    # dist_to_focus = (look_from-look_at).length()
    # aperture = 2.0

    look_from = point3(np.array([13, 2, 3]))
    look_at = point3(np.array([0, 0, 0]))
    vup = Vec3(np.array([0, 1, 0]))
    dist_to_focus = 10
    aperture = 0.1

    cam = Camera(look_from, look_at, vup, 20,
                 aspect_ratio, aperture, dist_to_focus)

    # render
    if GL_concurrency == True:
        pool = multiprocessing.Pool(processes=GL_process_num)
        for j in range(image_height-1, -1, -1):
            printProgressBar(image_height-j, image_height,
                             prefix='Map', suffix='Map all started', length=40)
            pool.apply_async(func=gen_at_line, args=(
                j, world, samples_per_pixel, image_width, image_height, max_depth, cam))
        pool.close()
        pool.join()
        reduce_files(GL_map_prefix, GL_task_name, image_height, target_file_prefix,
                     image_width=image_width, image_height=image_height)
    else:
        with open('{}.ppm'.format(target_file_prefix), 'w')as file:
            write_prefix(file, image_width, image_height)
            for j in range(image_height-1, -1, -1):
                for i in range(image_width):

                    printProgressBar((image_height-j-1)*(image_width)+(i+1), image_height*image_width,
                                     prefix='Flow', suffix='Flow proc', length=60)
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
            file.close()
    print('target file name = {}'.format(target_file_prefix))


def gen() -> float:
    print('gen started')
    start_time = time.time()
    ground_viewer()
    end_time = time.time()
    print('gen finished')
    return end_time-start_time


def main():
    time_list = []
    time_list.append(gen())

    for duration in time_list:
        print('time usage = {:.2f} s'.format(duration))
    return


if __name__ == '__main__':
    main()
