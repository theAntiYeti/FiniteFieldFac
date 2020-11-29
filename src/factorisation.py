import fields
import polynomial

def square_free_factorisation(f, poly):
    R = [] # Store factors

    c = poly.gcd(f,poly.derivative(f))
    w, _ = poly.div_mod(f,c)

    i = 1
    while len(w) != 1:
        y = poly.gcd(w,c)
        fac, _ = poly.div_mod(w,y)
        if poly.deg(fac) > 0:
            R.append([poly.monic(fac),i])
        w = y
        c, _ = poly.div_mod(c,y)
        i += 1
    
    if len(c) != 1:
        c = poly.pth_root(c)
        R += list(map(lambda t: (t[0],t[1]*poly.field.p), square_free_factorisation(c,poly)))

    # deal with polynomials with weird multiplicity here
    return R

def distinct_degree_factorisation(f, poly):
    i = 1
    S = []
    f_star = f

    while poly.deg(f_star) >= 2*i:
        l = poly.field.order() ** i
        char_poly = [poly.field.uni(0)]*(l+1)
        char_poly[-1] = poly.field.uni(1)
        char_poly[1] = poly.field.uni(-1) # char_poly is x^q^i - x
        g = poly.gcd(f_star, char_poly)

        if poly.deg(g) != 0:
            S.append([poly.monic(g), i])
            f_star, _ = poly.div_mod(f_star,g)
        
        i += 1

    if poly.deg(f_star) != 0:
        S.append([poly.monic(f_star), poly.deg(f_star)])
    if len(S) == 0:
        return [[f, 1]]
    else:
        return S

def equal_degree_factorisation(f, d, poly):
    """Factors a polynomial f with factors of equal degree d. Cantor Zassenhaus algorithm."""
    n = poly.deg(f)
    r = n // d 
    q = poly.field.order()

    if r == 1:
        return [f]
    
    irr_factors = []
    incomplete = [f]

    while r > 0:
        n = max(list(map(lambda x: poly.deg(x), incomplete)))

        h = poly.sample_poly_upto(n)
        e = ((q**d) - 1) // 2
        g = poly.add(poly.exp(h,e), [poly.field.uni(-1)])

        new_incomplete = []
        for u in incomplete:
            k = poly.gcd(g,u)
            if poly.deg(k) != 0 and poly.deg(k) != poly.deg(u):
                quot, _ = poly.div_mod(u, k)

                if poly.deg(k) == d:
                    irr_factors.append(poly.monic(k))
                    r -= 1
                else:
                    new_incomplete.append(k)

                if poly.deg(quot) == d:
                    irr_factors.append(poly.monic(quot))
                    r -= 1
                else:
                    new_incomplete.append(quot)
            else:
                new_incomplete.append(u)

        incomplete = [x for x in new_incomplete]
    return irr_factors

if __name__ == "__main__":

    fp   = fields.FiniteField(3, pivot=[1,0,1])
    poly = polynomial.Polynomial(fp)

    n = 9
    cyclo = [[]]*(n+1)
    cyclo[n] = [1]
    cyclo[1] = [-1]
    print(poly.display(cyclo))

    #f = list(map(lambda x: [x],[1,0,2,2,0,1,1,0,2,2,0,1]))
    str = ""

    for e, i in square_free_factorisation(cyclo, poly):
        for g, d in distinct_degree_factorisation(e, poly):
            for h in equal_degree_factorisation(g, d, poly):
                str += "({f})^{n}".format(f=poly.display(h),n=i)
    print("f="+str)

    k = poly.gcd([[1],[],[],[1]], [[],[2],[],[1]])
