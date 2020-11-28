# Class for polynomnials over Fp.
class Polynomial:
    def __eq__(self, other):
        if self.degree != other.degree or self.p != other.p:
            return False
        for i in range(self.degree + 1):
            if self.coefficients[i] != other.coefficients[i]:
                return False
        return True


    def __init__(self, coefficients, p):
        self.p = p  # Characteristic of the field
        self.coefficients = coefficients 
        self.degree = len(coefficients)  # This is temporary, will be set correctly after _normalise().
        self.__normalise()

    # Reduces to a normal form, smallest positive coefficients.
    def __normalise(self):
        j = 0
        for i in range(self.degree):
            if (self.coefficients[i] != 0):
                self.coefficients[i] = self.coefficients[i] % self.p
                if (self.coefficients[i] % self.p != 0):
                    j = i

        self.degree = j

    # Might replace this with a to_string.
    def pretty_print(self):
        if self == Polynomial([0],self.p):
            print("0")
            return 
        first_term = True
        for i in range(self.degree+1):
            if self.coefficients[i] != 0:
                toprint = ""

                if not(first_term):
                    toprint += '+ '
                first_term = False

                if self.coefficients[i] != 1:
                    toprint += "{}".format(self.coefficients[i])
                toprint += "x^{} ".format(i)
                
                print(toprint, end='')
        print()

    @staticmethod
    def add(poly1, poly2):
        if poly1.p != poly2.p:
            raise ValueError("Must be over same finite field")

        deg = max(poly1.degree,poly2.degree)
        coef = [0 for i in range(deg+1)]
        for i in range(deg + 1):
            if i <= poly1.degree and i <= poly2.degree:
                coef[i] = poly1.coefficients[i] + poly2.coefficients[i]
            elif i <= poly1.degree:
                coef[i] = poly1.coefficients[i] 
            elif i <= poly2.degree:
                coef[i] = poly2.coefficients[i]
        return Polynomial(coef, poly1.p)

    @staticmethod
    def mult(poly1, poly2):
        if poly1.p != poly2.p:
            raise ValueError("Must be over same finite field")

        deg = poly1.degree * poly2.degree
        coef = [0 for i in range(deg + 1)]

        for i in range(deg + 1): #convolution product
            for j in range(i + 1):
                if i-j <= poly1.degree:
                    p1_i = poly1.coefficients[i-j]
                else:
                    p1_i = 0
                if j <= poly2.degree:
                    p2_j = poly2.coefficients[j]
                else:
                    p2_j = 0
                coef[i] += p1_i * p2_j
            
        return Polynomial(coef, poly1.p)

    @staticmethod
    def div_mod(f, g):
        if f.p != g.p:
            raise ValueError("Must be over same finite field")

        if f.degree < g.degree:
            return (Polynomial([0],f.p), f)

        #preliminary calculations; a d s.t f(x) - ax^d g(x) has smaller degree
        diff = f.degree - g.degree
        a = Polynomial._inverse(g.coefficients[g.degree], f.p) * f.coefficients[f.degree]

        #calculate f(x) - ax^n g(x) - felt right to do it like this rather than using the existing methods, may be a mistake
        coef = [0 for i in range(f.degree + 1)]
        for i in range(f.degree + 1):
            if i-diff < 0:
                coef[i] = f.coefficients[i]
            else:
                coef[i] = f.coefficients[i] - (a * g.coefficients[i-diff])
        
        #recursive step
        to_div = Polynomial(coef, f.p)
        (q,r) = Polynomial.div_mod(to_div, g)

        #have calculated f - ax^d g = qg + r
        #thus our q to return is ax^d + q
        quot = [0 for i in range(diff + 1)]

        for i in range(q.degree+1):
            quot[i] =  q.coefficients[i]

        quot[diff] = a  # After the loop as the zero polynomial has representation [0] rather than [].

        return (Polynomial(quot, f.p), r)

    @staticmethod
    def _inverse(a, p):
        if a % p == 0:
            raise ZeroDivisionError('Division by zero in Fp')

        return (a**(p-2)) % p