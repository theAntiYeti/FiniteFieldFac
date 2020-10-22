class FiniteField:
    def __init__(self,p,pivot=None):
        self.pivot = [0,1]
        if pivot:
            self.pivot = pivot
        assert(self.pivot) 
        self.p = p # The Characteristic

    def reduce_poly(self, f):   
        """Returns the Fp[x]/<pivot> representative of the polynomial."""
        q, r = FiniteField.div_mod(f, self.pivot)

        for i in range(len(r)):
            r[i] = r[i] % self.p 
        return FiniteField.prune(r)

    def add(self,f,g):
        """Adds two elements in Fp^n and returns the canonical representative mod pivot."""
        return self.reduce_poly(FiniteField._add(f,g,1))
        
    def mult(self,f,g):
        """Multiplies two elements in Fp^n and returns the canonical representative mod pivot."""
        if FiniteField.deg(f) == -1 or FiniteField.deg(g) == -1:
            return []

        n = FiniteField.deg(f) + FiniteField.deg(g)
        ret = [0] * (n + 1)
        for i in range(len(f)):
            for j in range(len(g)):
                ret[i+j] += f[i] * g[j]
        
        return self.reduce_poly(ret)

    @staticmethod
    def div_mod(f, g):
        """Division of monic f by monic g in Z[x]."""
        assert (g[-1] == 1), "Divisor must be monic."

        k = FiniteField.deg(f) - FiniteField.deg(g)
        if k < 0:
            return [], f # [] indicates the 0 polynomial.
        
        a = f[-1]
        f_red = FiniteField._add(f,[0]*k +g,-a)
        q, r = FiniteField.div_mod(f_red, g)

        return FiniteField._add(FiniteField._xn(k,a),q,1) , r



    @staticmethod
    def deg(p):
        return len(p) - 1

    @staticmethod
    def _add(f,g,a):
        """Add a*g to f in Z[x]."""
        n = max(FiniteField.deg(f), FiniteField.deg(g))
        fin = [0] * (n+1)

        for i in range(n+1):
            if i <= FiniteField.deg(f):
                fin[i] += f[i]
            if i <= FiniteField.deg(g):
                fin[i] += a * g[i]
        return FiniteField.prune(fin)

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

