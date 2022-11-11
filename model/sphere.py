from .hittable import hittable, hit_record
from .Ray import Ray
import numpy as np


class sphere(hittable):
    def __init__(self, center, radius) -> None:
        self.center = center
        self.radius = radius

    def hit(self, r: Ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        oc = r.origin()-self.center
        a = r.direction().length_squared()
        half_b = oc.dot(r.direction())
        c = oc.length_squared()-self.radius*self.radius

        discriminant = half_b*half_b-a*c
        if discriminant < 0:
            return False
        sqrtd = np.sqrt(discriminant)

        root = (-half_b-sqrtd)/a
        if not t_min < root < t_max:
            root = (-half_b+sqrtd)/a
            if not t_min < root < t_max:
                return False
        rec.t = root
        rec.p = r.at(root)
        outward_normal = (rec.p-self.center)/self.radius
        rec.set_face_normal(r, outward_normal)
        return True
