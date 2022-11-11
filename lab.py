import numpy as np
from model import Vec3

test1 = Vec3.color(np.array([1.3, 423, 43]))
test2 = Vec3.color(np.array([222, 423, 43]))

print((test1+test2).vec())
