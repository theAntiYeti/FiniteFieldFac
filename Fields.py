class Finite_Field:
    def __init__(self,p,pivot=None):
        self.pivot = [0,1]
        if pivot:
            self.pivot = pivot
        assert(self.pivot) 
        self.p = p # The Characteristic

    def reduce_poly(self, f):   
        q, r = Finite_Field.div_mod(f, self.pivot)

        for i in range(len(r)):
            r[i] = r[i] % self.p 
        return Finite_Field.prune(r)

    @staticmethod
    def div_mod(f, g):
        """Division of monic f by monic g in Z[x]."""
        assert (g[-1] == 1), "Divisor must be monic."

        k = Finite_Field.deg(f) - Finite_Field.deg(g)
        if k < 0:
            return [], f # [] indicates the 0 polynomial.
        
        a = f[-1]
        f_red = Finite_Field._add(f,[0 for i in range(k)]+g,-a)
        q, r = Finite_Field.div_mod(f_red, g)

        return Finite_Field._add(Finite_Field._xn(k,a),q,1) , r



    @staticmethod
    def deg(p):
        return len(p) - 1

    @staticmethod
    def _add(f,g,a):
        """Add a*g to f in Z[x]."""
        n = max(Finite_Field.deg(f), Finite_Field.deg(g))
        fin = [0 for i in range(n+1)]

        for i in range(n+1):
            if i <= Finite_Field.deg(f):
                fin[i] += f[i]
            if i <= Finite_Field.deg(g):
                fin[i] += a * g[i]
        return Finite_Field.prune(fin)

    @staticmethod
    def _xn(n,a):
        """Returns the polynomial x^n."""
        p = [0 for i in range(n+1)]
        if (n > -1):
            p[-1] = a
        return p
    
    @staticmethod
    def prune(f):
        """Takes a polynomial with leading 0s and removes them."""
        n = len(f) - 1
        while n >= 0 and f[n] == 0:
            n -= 1
        return f[0:n+1]
