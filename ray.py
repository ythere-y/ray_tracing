import vec3
import numpy as np


class ray:
    def __init__(self, orig, dir) -> None:
        self.orig = vec3.point3(orig)
        self.dir = vec3.point3(dir)

    def origin(self) -> vec3.point3:
        return self.orig

    def direction(self) -> vec3.point3:
        return self.dir

    def at(self, t: float) -> vec3.point3:
        return self.orig+t*self.dir
