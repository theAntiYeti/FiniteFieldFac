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

if __name__=="__main__":
    unittest.main()