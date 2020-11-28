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
        """Takes f and g and returns the product fg."""
        if self.deg(f) == -1 or self.deg(g) == -1:
            return []
        n = self.deg(f) + self.deg(g)
        ret = [self.field.zero()] * (n+1)
        
        for i in range(len(f)):
            for j in range(len(g)):
                ret[i + j] = self.field.add(ret[i + j], self.field.mult(f[i],g[j]))

        return ret
    
    def derivative(self, f):
        """Computes the formal derivative of f."""
        ret = [0] * self.deg(f)
        for i in range(1,self.deg(f)+1):
            ret[i-1] = self.field.mult(f[i], self.field.uni(i))

        return ret

    def div_mod(self, f, g):
        """Given polynomials f, g, returns (q,r) s.t f = q*g + r."""
        k = self.deg(f) - self.deg(g)
        if k < 0:
            return ([], f)
        
        a = f[-1]; b = self.field.inv(g[-1])
        c = self.field.mult([-1],self.field.mult(a,b))

        g_2 = ([[]]*k) + list(map(lambda x: self.field.mult(x, c), g))
        f_red = self.prune([self.field.add(f[i], g_2[i]) for i in range(len(f))])
        
        q, r = self.div_mod(f_red, g)

        return self.add(([[]] * k) + [self.field.mult(a,b)], q), r

    def gcd(self, f, g):
        if g == self.field.zero():
            return f
        _, r = self.div_mod(f,g)

        return self.gcd(g, r)

    def display(self, f, var='x'):
        if len(f) == 0:
            return "0"
        if len(f) == 1:
            return self.__display_elem(f[0])
        
        head = ""
        if self.field.reduce_poly(f[-1]) != self.field.uni(1):
            head = self.__display_elem(f[-1])

        tailstr = self.display(self.prune(f[0:-1]), var=var)

        if self.deg(f) == 1:
            if tailstr != "0":
                return "{h}{v} + {t}".format(h=head,v=var,t=tailstr)
            else:
                return "{h}{v}".format(h=head,v=var)

        if tailstr != "0":
            return "{h}{v}^{d} + {t}".format(h=head,v=var,d=self.deg(f),t=tailstr)
        else:
            return "{h}{v}^{d}".format(h=head,v=var,d=self.deg(f))
            

    def __display_elem(self, e):
        if self.field.is_base(e):
            return self.field.display(e)
        else:
            return "({d})".format(d=self.field.display(e))

    @staticmethod
    def deg(p):
        return len(p) - 1

    @staticmethod
    def _xn(n,a):
        """Returns the polynomial x^n."""
        if n < 0:
            return []
        return [0]*n + [a]

    def prune(self, f):
        """Takes a polynomial with leading 0s and removes them."""
        n = len(f) - 1
        while n >= 0 and f[n] == self.field.zero():
            n -= 1
        return f[0:n+1]


import fields

if __name__ == "__main__":
    field = fields.FiniteField(p=3, pivot=[-1,-1,0,1])
    polyring = Polynomial(field=field)
    print(polyring.display([[1,2] , [1,1,1], [], [7]]))