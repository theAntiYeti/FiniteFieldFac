from Polynomial import *
import unittest

class Test_Polynomial(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(Polynomial([1,2,3],5), Polynomial([1,2,3,0], 5))
        self.assertEqual(Polynomial([1,-1,1,0],2), Polynomial([-1,1,1,2],2))
        self.assertNotEqual(Polynomial([0],2),Polynomial([0],3))

    def test_invert(self):
        with self.assertRaises(ZeroDivisionError):
            Polynomial._inverse(5,5)
        with self.assertRaises(ZeroDivisionError):
            Polynomial._inverse(333,3)
        self.assertEqual(Polynomial._inverse(3,7),5)

    def test_init(self):
        f = Polynomial([1,2,3],3)
        self.assertEqual(f.degree,1)
        
    def test_add(self):
        f = Polynomial([1,22,3,34,5],17)
        g = Polynomial([2,3,0,0,12],17)
        self.assertEqual(Polynomial.add(f,g), Polynomial([3,25,3,34,0],17))
        with self.assertRaises(TypeError):
            Polynomial.add(f,Polynomial([1],2))

    def test_mult(self):
        f = Polynomial([1,22,3,34,5],17)
        g = Polynomial([2,3,0,0,12],17)
        self.assertEqual(Polynomial.mult(f,g), Polynomial([2,47,72,77,124,279,36,408,60],17))
        with self.assertRaises(TypeError):
            Polynomial.mult(f,Polynomial([1],2))


if __name__ == "__main__":
    unittest.main()