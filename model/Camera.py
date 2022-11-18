from .Vec3 import *
from .Ray import Ray
import numpy as np


class Camera:
    def __init__(self, lookfrom: point3, lookat: point3, vup: Vec3, vfow: float, aspect_ratio: float) -> None:
        # aspect_ratio = 16/9
        # viewport_height = 2.0
        # viewport_width = aspect_ratio*viewport_height

        theta = np.deg2rad(vfow)
        h = np.tan(theta/2)
        viewport_height = 2.0*h
        viewport_width = aspect_ratio*viewport_height
        focal_length = 1.0

        w = unit_vector(lookfrom-lookat)
        u = unit_vector(cross(vup, w))
        v = cross(w, u)

        self.origin = lookfrom
        self.horizontal = u*viewport_width
        self.vertical = v*viewport_height
        self.lower_left_corner = Vec3(self.origin.vec()-self.horizontal.vec()/2 -
                                      self.vertical.vec()/2-w.vec())

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner+self.horizontal*s+self.vertical*t-self.origin)
