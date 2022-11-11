import unittest
# from . import model
import model
import numpy as np


class TestVec3(unittest.TestCase):
    def test_add(self):
        c = dev.Calculate().add(1, 4)
        self.assertEqual(c, 5)

    def test_vec3_add(self):
        t_1 = model.Vec3(np.array([1, 2, 3]))
        t_2 = model.Vec3(np.array([1, 2, 3]))
        t_3 = t_1+t_2
        exp = np.array([2, 4, 6])
        same_flag = True
        for i in range(3):
            if not t_3[i] == exp[i]:
                same_flag = False
        self.assertTrue(same_flag)

    def test_get(self):
        t = model.Vec3(np.array([1, 2, 3]))
        self.assertEqual(t[0], 1)
        self.assertEqual(t[1], 2)
        self.assertEqual(t[2], 3)

    def test_set(self):
        t = model.Vec3(np.array([1, 2, 3]))
        for i in range(3):
            t[i] = i
        for i in range(3):
            self.assertEqual(t[i], i)

    def test_dot(self):
        t_1 = model.Vec3(np.array([1, 2, 3]))
        t_2 = model.Vec3(np.array([3, 2, 1]))
        self.assertEqual(t_1.dot(t_2), 10)

    def test_length(self):
        t = model.Vec3(np.array([0.5, 1, 1]))
        self.assertEqual(t.length(), np.sqrt(1+1+0.25))

    def test_length_squared(self):
        t = model.Vec3(np.array([1, 1, 1]))
        self.assertEqual(t.length_squared(), 3)

    def test_unit(self):
        t = model.Vec3(np.array([1, 1, 1]))
        self.assertEqual(t.unit()[0], 1/np.sqrt(3))
        t2 = model.Vec3(np.array([-1.777777, 1.0, -1.0]))
        self.assertEqual(t.unit()[0], 0.5773502691896258)


color_1 = model.color(np.array([1, 1, 1]))
color_2 = model.color(np.array([0.4, 0.5, 0.7]))


class TestColor(unittest.TestCase):
    def test_str(self):
        get = str(color_1)
        print(get)
        self.assertEqual(get, '255 255 255\n')
        get = str(color_2)
        print(get)
        self.assertEqual(get, '102 127 179\n')


if __name__ == '__main__':
    unittest.main
