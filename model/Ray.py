from .Vec3 import point3
import numpy as np


class Ray:
    def __init__(self, orig, dir) -> None:
        self.orig = point3(orig)
        self.dir = point3(dir)

    def origin(self) -> point3:
        return self.orig

    def direction(self) -> point3:
        return self.dir

    def at(self, t: float) -> point3:
        return self.orig+t*self.dir
