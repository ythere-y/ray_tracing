from .Vec3 import point3
import numpy as np


class Ray:
    def __init__(self, orig: point3, dir: point3) -> None:
        self.orig = orig
        self.dir = dir

    def origin(self) -> point3:
        return self.orig

    def direction(self) -> point3:
        return self.dir

    def at(self, t: float) -> point3:
        return self.orig+self.dir*t
