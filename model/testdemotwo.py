import unittest

from dev.Calculate import Calculate

c = Calculate()
add = c.add(1, 4)
red = c.red(4, 1)


class UnitTestTwo(unittest.TestCase):
    def setUp(self) -> None:
        print('start up !')

    def test001(self):
        self.assertEqual(add, 5)

    def test002(self):
        self.assertEqual(red, 3)

    def tearDown(self) -> None:
        print('end down')


if __name__ == '__main__':
    unittest.main
