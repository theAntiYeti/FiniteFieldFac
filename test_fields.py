from Fields import FiniteField as FF
import unittest

class Test_Fields(unittest.TestCase):
    def test_xn(self):
        """Test the function taking n |-> x^n"""
        self.assertEqual([], FF._xn(-1,1))
        self.assertEqual([1], FF._xn(0,1))
        self.assertEqual([0,1], FF._xn(1,1))
        self.assertEqual([0,0,1], FF._xn(2,1))
        f = [0 for i in range(101)]
        f[-1] = 1
        self.assertEqual(f, FF._xn(100,1))


    def test_prune(self):
        self.assertEqual([1,2,3], FF.prune([1,2,3,0,0]))
        self.assertEqual([], FF.prune([]))
        self.assertEqual([], FF.prune([0,0,0]))
        self.assertEqual([1,2,3], FF.prune([1,2,3]))
        self.assertEqual([1,2,3,0,1], FF.prune([1,2,3,0,1,0,0]))

    def test_auxilliary_add(self):
        self.assertEqual(FF._add([1,2,3],[],1), [1,2,3])
        self.assertEqual(FF._add([1,2,3], [1,2,3], -1), [])
        self.assertEqual(FF._add([1,2,3], [1,2,3], 2), [3,6,9])
        self.assertEqual(FF._add([1], [4,5,6], 1), [5,5,6])


    def test_div_mod(self):
        self.assertEqual(FF.div_mod([0,1,2], [0,1]) , ([1,2],[]))
        self.assertEqual(FF.div_mod([0,1],[0,1,1]) , ([],[0,1]))
        #self.assertEqual(FF.div_mod([],[]) , ([],[]))

    def test_reduce(self):
        fp3 = FF(3) # X^2 - 1
        self.assertEqual(fp3.reduce_poly([5]), [2])
        self.assertEqual(fp3.reduce_poly([6]), [])

        fp27 = FF(3, pivot=[-1,-1,0,1]) 
        self.assertEqual(fp27.reduce_poly([0,0,0,0,1]), [0,1,1])

    def test_element_add(self):
        fp27 = FF(3, pivot=[-1,-1,0,1])
        self.assertEqual(fp27.add([1],[1]), [2])
        self.assertEqual(fp27.add([1],[2]), [])
        self.assertEqual(fp27.add([1,1],[0,1,2]), [1,2,2])

    def test_mult(self):
        fp27 = FF(3, pivot=[-1,-1,0,1])
        self.assertEqual(fp27.mult([],[1,2,3]), [])
        self.assertEqual(fp27.mult([1,2,3],[]), [])
        self.assertEqual(fp27.mult([2],[0,2,1]), [0,1,2])
        self.assertEqual(fp27.mult([1,1],[1,1]), [1,2,1])

    def test_inverse_Fp(self):
        fp27 = FF(3, pivot=[-1,-1,0,1])
        self.assertEqual(fp27.inverse_f_p(2), 2)

    def test_inverse_Fp_error(self):
        fp27 = FF(3, pivot=[-1,-1,0,1])
        self.assertRaises(ValueError, fp27.inverse_f_p, 3)

    def test_inverse1(self):
        fp27 = FF(3, pivot=[-1,-1,0,1])
        a = fp27.inv([1,1,1])
        self.assertEqual(fp27.mult(a, [1,1,1]), [1])

    def test_inverse2(self):
        fp16 = FF(2, pivot=[1,1,0,0,1])
        f = [1,1,1]
        g = fp16.inv(f)
        self.assertEqual(fp16.mult(f,g), [1])

if __name__ == "__main__":
    unittest.main()
