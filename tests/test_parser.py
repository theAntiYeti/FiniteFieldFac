import unittest

import os
import sys
sys.path.insert(0, os.getcwd()+'/src') # To access /src file to import FF.
from parse_polynomial import *

class TestParse(unittest.TestCase):
    def test_process_x(self):
        el = 'x'
        self.assertEqual(process(el), [1,1])

    def test_process_xtod(self):
        el = 'x^3'
        self.assertEqual(process(el), [1,3])
    
    def test_process_n(self):
        el = '5'
        self.assertEqual(process(el), [5,0])
    
    def test_process_nx(self):
        el = '7x'
        self.assertEqual(process(el), [7,1])

    def test_process_nxd(self):
        el = '21x^7'
        self.assertEqual(process(el), [21,7])

    def test_parse1(self):
        f = parse_unbracketed("x^5 + 4 x ^2", as_integer=True)
        self.assertEqual(f, [0,0,4,0,0,1])

    def test_parse2(self):
        f = parse_unbracketed('x^2 + x^3 + x^0')
        self.assertEqual(f, [[1],[],[1],[1]])
    
    def test_parse3(self):
        f = parse_unbracketed('x^3 + 2x + 1')
        self.assertEqual(f, [[1],[2],[],[1]])

    def test_parse4(self):
        f = parse_unbracketed('x', as_integer=True)
        self.assertEqual(f, [0,1])

    def test_parse5(self):
        f = parse_unbracketed('1', as_integer=True)
        self.assertEqual(f, [1])

    def test_parse6(self):
        f = parse_unbracketed('x^3 + 2x^2 + 6x + 4', as_integer=True)
        self.assertEqual(f, [4, 6, 2, 1])

if __name__ == "__main__":
    unittest.main()