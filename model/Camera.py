from .Vec3 import point3, Vec3
from .Ray import Ray
import numpy as np


class Camera:
    def __init__(self) -> None:
        aspect_ratio = 16/9
        viewport_height = 2.0
        viewport_width = aspect_ratio*viewport_height
        focal_length = 1.0

        self.origin = point3(np.array([0, 0, 0]))
        self.horizontal = Vec3(np.array([viewport_width, 0, 0]))
        self.vertical = Vec3(np.array([0, viewport_height, 0]))
        self.lower_left_corner = Vec3(self.origin.vec()-self.horizontal.vec()/2 -
                                      self.vertical.vec()/2-np.array([0, 0, focal_length]))

    def get_ray(self, u: float, v: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner+self.horizontal*u+self.vertical*v-self.origin)
