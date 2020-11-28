class Polynomial:
    """
    A class for representing the polynomial ring over a given (finite) field and interpreting
    lists of field elements as polynomials.
    """
    def __init__(self, field):
        self.field = field

    def add(self, f, g):
        """Takes polynomials f, g as lists and returns the list representing f+g."""
        n = len(f)
        m = len(g)

        if n <= m:
            big = g
            small = f
        else:
            big = f
            small = g
            m = len(f)
            n = len(g)
        # m >= n
        
        output = [None for i in range(m)]
        for i in range(n):
            output[i] = self.field.add(big[i],small[i])
        for i in range(n,m):
            output[i] = big[i]

        return output

    def mult(self, f, g):
        if self.deg(f) == -1 or self.deg(g) == -1:
            return []
        n = self.deg(f) + self.deg(g)
        ret = [self.field.zero()] * (n+1)
        
        for i in range(len(f)):
            for j in range(len(g)):
                ret[i + j] = self.field.add(ret[i + j], self.field.mult(f[i],g[j]))

        return ret
    
    @staticmethod
    def deg(p):
        return len(p) - 1

    @staticmethod
    def _xn(n,a):
        """Returns the polynomial x^n."""
        if n < 0:
            return []
        return [0]*n + [a]

    @staticmethod
    def prune(f):
        """Takes a polynomial with leading 0s and removes them."""
        n = len(f) - 1
        while n >= 0 and f[n] == 0:
            n -= 1
        return f[0:n+1]