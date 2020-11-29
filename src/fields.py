import random

class FiniteField:
    def __init__(self,p,pivot=None):
        self.pivot = [0,1]
        if pivot:
            self.pivot = pivot
        assert(self.pivot) 
        self.p = p # The Characteristic

    def order(self):
        return self.deg(self.pivot) * self.p

    def uni(self, i):
        """Image of the universal morphism Z->k. I.E 'What is i in k'."""
        return self.reduce_poly([i])
        
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

    def inv(self,f):
        """Takes an element and returns its inverse in Fp[x]/<pivot>."""
        a, _ = self.bezout(f, self.pivot)
        return a

    def bezout(self, f, g):
        """Perform Bezout in Fp[X], returns a,b s.t af + bg = 1.
           Only works if f, g coprime (guaranteed by inputs)."""
        a = g[-1] # Leading coefficient of g
        a_inv = self.inverse_f_p(a) 
        g_monic = [(a_inv * c) % self.p for c in g] # g = a * g_monic. This operation is fine because of Fp invertability.

        q_1, r = self.div_mod(f, g_monic)
        r = self.reduce_poly(r)
        
        q = [-(a_inv * c) % self.p for c in q_1] # f + q*g = r

        if len(r) == 1:
            return ([self.inverse_f_p(r[0])], q)
        
        x, y = self.bezout(g, r) # xg + yr = 1
        q_ = self.mult(y,q)
        new_y = self.prune([x % self.p for x in self._add(x, q_, 1)])
        return (y, new_y)
  
    def inverse_f_p(self, a):
        """Takes an element a in Fp and returns it's inverse"""
        if a % self.p == 0:
            raise ValueError("Division by zero in F", self.pivot)

        return (a**(self.p-2)) % self.p

    def frobenius(self, f):
        """Computes f^p."""
        d = self.deg(f)*self.p
        power_poly = [0] * (d+1)

        for i in range(len(f)):
            power_poly[self.p*i] = f[i]
        # power_poly now represents f^p in k[X]/<pivot>

        return self.reduce_poly(power_poly)

    def inverse_frobenius(self, f):
        e = self.deg(self.pivot)
        g = f
        for i in range(e-1):
            g = self.frobenius(g)
        return g

    def sample(self):
        r = self.deg(self.pivot)
        return self.prune([random.randrange(self.p) for _ in range(r)])

    def display(self, f, var='t'):
        """Returnsthe representative of Fp[x]/<pivot> as a string."""
        f_red = self.reduce_poly(f)
        if len(f_red) == 0:
            return "0"
        if len(f_red) == 1:
            return str(f_red[0])

        head = ""
        if f_red[-1] != 1:
            head = str(f_red[-1])

        tailstr = self.display(f_red[0:-1], var=var)

        if self.deg(f_red) == 1:
            if tailstr != "0":
                return "{h}{v}+{t}".format(h=head,v=var,t=tailstr)
            else:
                return "{h}{v}".format(h=head,v=var)
                
        if tailstr != "0":
            return "{h}{v}^{d}+{t}".format(h=head,v=var,d=self.deg(f_red),t=tailstr)
        else:
            return "{h}{v}^{d}".format(h=head,v=var,d=self.deg(f_red))
        

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
    
    @staticmethod
    def zero():
        """For compliance with the interfact of polynomial."""
        return []

    @staticmethod
    def is_base(f):
        """See if f is an element of Fp."""
        return (FiniteField.deg(f) == 0)

if __name__=="__main__":
    # For testing cosmetic functions.
    fp27 = FiniteField(3, pivot=[-1,-1,0,1]) 
    print(fp27.display([]))
    print(fp27.display([1,1,1]))
    print(fp27.display([1,0,1]))