from abc import ABCMeta, abstractmethod


import numpy as np
from typing import Tuple
from .Ray import Ray
from .Vec3 import Vec3, point3


class hit_record:
    def __init__(self, p: point3 = point3(), normal: Vec3 = Vec3(), t: float = 0.0, front_face: bool = True) -> None:
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face

    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        self.front_face = r.direction().dot(outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal


class hittable:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        pass

    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, hit_record]:
        pass


class hittable_list(hittable):
    def __init__(self, objects: list[hittable] = list()) -> None:
        self.objects = objects

    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, hit_record]:
        hit_anything = False
        closed_so_far = t_max
        rec = None
        for obj in self.objects:
            hit_any, temp_rec = obj.hit(r, t_min, closed_so_far)
            if hit_any:
                hit_anything = True
                closed_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything, rec

    def clear(self):
        self.objects.clear()

    def add(self, obj: hittable):
        self.objects.append(obj)


class sphere(hittable):
    def __init__(self, center, radius) -> None:
        self.center = center
        self.radius = radius

    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, hit_record]:
        oc = r.origin()-self.center
        a = r.direction().length_squared()
        half_b = oc.dot(r.direction())
        c = oc.length_squared()-self.radius*self.radius
        rec = None
        discriminant = half_b*half_b-a*c
        if discriminant < 0:
            return False, rec
        sqrtd = np.sqrt(discriminant)

        root = (-half_b-sqrtd)/a
        if not t_min < root < t_max:
            root = (-half_b+sqrtd)/a
            if not t_min < root < t_max:
                return False, rec
        rec = hit_record()
        rec.t = root
        rec.p = r.at(root)
        outward_normal = (rec.p-self.center)/self.radius
        rec.set_face_normal(r, outward_normal)
        return True, rec
