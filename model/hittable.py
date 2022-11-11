from abc import ABCMeta, abstractmethod
from .Vec3 import point3
from .Ray import Ray


class hit_record:
    def __init__(self, p, normal, t) -> None:
        self.p = p
        self.normal = normal
        self.t = t


class hittable:
    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        pass

    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        pass
