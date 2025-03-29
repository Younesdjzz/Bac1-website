import unittest
import math
from mobility.emission import distance,emission,AirCraft


class EmissionTestCase (unittest.TestCase):

    def test_distance(self):
        # Un angle de 1 Radian intercept un arc de longueur égal au rayon
        # Nous prenons deux points distants d'un angle de 1 radian
        expected = 6378 * math.radians(1)
        a = (0, 1)
        b = (0, 2)
        actual = distance(a[0], a[1], b[0], b[1])
        self.assertAlmostEqual(actual, expected, 1,msg=f'My error message on pl.f({actual}) different than {expected}')

        expected=0
        a=(0,0)
        b=(0,0)
        actual=distance(a[0], a[1], b[0], b[1])
        self.assertAlmostEqual(actual, expected, 1,msg=f'you travel around the world')

        a = (24, 42)
        b = (42, 24)
        actual = distance(a[0], a[1], b[0], b[1])
        expected = 2603.63
        self.assertAlmostEqual(actual, expected, 1, msg=f'Distance between {a} and {b} was {actual}, expected {expected}')

    def test_emission(self):
        actual=emission(100,AirCraft.S)
        expected=0.7875
        self.assertAlmostEqual(actual,expected,1,msg=f'The emission for the{AirCraft.S} is {expected} not {actual}')
        actual=emission(100,AirCraft.M)
        expected=1.96875
        self.assertAlmostEqual(actual,expected,1,msg=f'The emission for the{AirCraft.S} is {expected} not {actual}')
        actual=emission(100,AirCraft.H)
        expected=3.9375
        self.assertAlmostEqual(actual,expected,1,msg=f'The emission for the{AirCraft.S} is {expected} not {actual}')
        actual=emission(100,AirCraft.J)
        expected=9.45
        self.assertAlmostEqual(actual,expected,1,msg=f'The emission for the{AirCraft.S} is {expected} not {actual}')
        

if __name__ == '__main__':
    unittest.main(verbosity=2)