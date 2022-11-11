from abc import ABCMeta, abstractmethod
from .Vec3 import point3, Vec3
from .Ray import Ray


class hit_record:
    def __init__(self, p: point3, normal: Vec3, t: float, front_face: bool) -> None:
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
    def hit(self, r: Ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        pass


class hittable_list(hittable):
    def __init__(self, objects: list[hittable]) -> None:
        self.objects = objects

    def hit(self, r: Ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        temp_rec = hit_record()
        hit_anything = False
        closed_so_far = t_max

        for obj in self.objects:
            if obj.hit(r, t_min, closed_so_far, temp_rec):
                hit_anything = True
                closed_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything

    def clear(self):
        self.objects.clear()

    def add(self, obj: hittable):
        self.objects.append(obj)
