import os
import sys
sys.path.insert(0, os.getcwd()+'/src') # To access /src file to import FF.
from fields import FiniteField as FF
from polynomial import Polynomial as Poly
import unittest

class TestPoly(unittest.TestCase):
    def test_add(self):
        field = FF(p=5)
        polyring = Poly(field=field)

        f = [[0],[1]]
        g = [[],[],[2]]

        self.assertEqual(polyring.add(f,g), [[],[1],[2]])
    
    def test_mult(self):
        field = FF(p=5)
        polyring = Poly(field=field)

        f = [[0],[1]]
        g = [[],[],[2]]

        self.assertEqual(polyring.mult(f,g), [[],[],[],[2]])

    def test_derivative(self):
        field = FF(p=3)
        polyring = Poly(field=field)

        f = [field.uni(1) for i in range(11)]
        self.assertEqual(polyring.derivative(f), [field.uni(i+1) for i in range(10)])

    def test_div_mod(self):
        field = FF(p=3)
        polyring = Poly(field=field)

        f = [[0],[1]]
        g = [[],[],[2]]

        self.assertEqual(polyring.div_mod(g,f), ([[],[2]],[]))

    def test_gcd(self):
        field = FF(p=3)
        polyring = Poly(field=field)

        f = [[0],[1]]
        g = [[],[],[2]]

        self.assertEqual(polyring.gcd(f,g), f)

if __name__=="__main__":
    unittest.main()