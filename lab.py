import numpy as np
import vec3

test1 = vec3.color(np.array([1.3, 423, 43]))
test2 = vec3.color(np.array([222, 423, 43]))

print((test1+test2).vec())
