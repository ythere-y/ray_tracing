from .Vec3 import *
from .Ray import Ray
import numpy as np


class Camera:
    def __init__(self, lookfrom: point3, lookat: point3, vup: Vec3, vfow: float, aspect_ratio: float, aperture: float, focus_dist: float) -> None:
        # aspect_ratio = 16/9
        # viewport_height = 2.0
        # viewport_width = aspect_ratio*viewport_height

        theta = np.deg2rad(vfow)
        h = np.tan(theta/2)
        viewport_height = 2.0*h
        viewport_width = aspect_ratio*viewport_height
        focal_length = 1.0

        self.w = unit_vector(lookfrom-lookat)
        self.u = unit_vector(cross(vup, self.w))
        self.v = cross(self.w, self.u)

        self.origin = lookfrom
        self.horizontal = self.u*viewport_width*focus_dist
        self.vertical = self.v*viewport_height*focus_dist
        self.lower_left_corner = Vec3(self.origin.vec()-self.horizontal.vec()/2 -
                                      self.vertical.vec()/2-self.w.vec()*focus_dist)
        self.lens_radius = aperture/2

    def get_ray(self, s: float, t: float) -> Ray:
        rd = random_in_unit_disk()*self.lens_radius
        offset = self.u*rd.x()+self.v*rd.y()

        return Ray(
            self.origin+offset,
            self.lower_left_corner+self.horizontal*s+self.vertical*t-self.origin-offset)
