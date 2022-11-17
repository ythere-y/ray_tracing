from .hittable import hit_record
from abc import ABCMeta, abstractmethod
from .Ray import Ray
from typing import Tuple
from .Vec3 import color


class material:

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        pass

    @abstractmethod
    def scatter(self, r_in: Ray) -> Tuple[bool, hit_record, color, Ray]:
        pass


