from abc import ABCMeta, abstractmethod

import numpy as np
from typing import Tuple
from .Ray import Ray
from .Vec3 import *
from utils import *


class hit_record:
    def __init__(self, p: point3 = point3(), normal: Vec3 = Vec3(), t: float = 0.0, front_face: bool = True) -> None:
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.mat_ptr: material

    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        self.front_face = r.direction().dot(outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal


class material:

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        pass

    @abstractmethod
    def scatter(self, r_in: Ray, rec: hit_record) -> Tuple[bool, color, Ray]:
        pass


class lambertion(material):

    def __init__(self, color: color) -> None:
        self.albedo: color = color

    def scatter(self, r_in: Ray, rec: hit_record) -> Tuple[bool,  color, Ray]:
        scatter_direction = rec.normal+random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True, attenuation, scattered


class metal(material):
    def __init__(self, color: color, fuzz: float) -> None:
        self.albedo: color = color
        self.fuzz = min(fuzz, 1)

    def scatter(self, r_in: Ray, rec: hit_record) -> Tuple[bool, color, Ray]:
        reflected = reflect(r_in.direction().unit(), rec.normal)
        # scattered = Ray(rec.p, point3(reflected.vec() +
        #                 self.fuzz*random_in_unit_sphere().vec()))
        scattered = Ray(rec.p, point3(reflected.vec()))
        attenuation = self.albedo
        scatter_flag = scattered.direction().dot(rec.normal) > 0
        return scatter_flag, attenuation, scattered


class dielectric(material):
    def __init__(self, index_of_refraction: float) -> None:
        self.ir = index_of_refraction

    def reflectance(self, cosin: float, ref_idx: float) -> float:
        # Use Schlick's approximation reflectance.
        r0 = (1-ref_idx)/(1+ref_idx)
        r0 = r0*r0
        return r0+(1-r0)*pow((1-cosin), 5)

    def scatter(self, r_in: Ray, rec: hit_record) -> Tuple[bool, color, Ray]:
        attenuation = color(np.array([1, 1, 1]))
        refraction_ratio = (1/self.ir) if rec.front_face else self.ir

        unit_direction = r_in.direction().unit()
        cos_theta = min(rec.normal.dot(-unit_direction), 1.0)
        sin_theta = np.sqrt(1.0-cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0

        if (cannot_refract or self.reflectance(cos_theta, refraction_ratio) > random_float()):
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refraction_ratio)

        scattered = Ray(rec.p, direction)
        return True, attenuation, scattered


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
    def __init__(self, center: point3, radius: float, m: material) -> None:
        self.center = center
        self.radius = radius
        self.mat_ptr: material = m

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
        rec.mat_ptr = self.mat_ptr
        return True, rec
