from Polynomial import *

P = 19
ZERO = Polynomial([0], P)

def factorise(f):
    # Check for 0 polynomial.
    if f == ZERO:
        raise ValueError('Cannot factor zero polynomial')
    
    counter = [0 for i in range(f.degree+1)]
    counter[1] = 1 # No point dividing by anything smaller than a linear factor.
    c = 1
    while c < f.degree:
        g = Polynomial(counter, P)
        (q,r) = Polynomial.div_mod(f, g)
        if r == ZERO:
            g.pretty_print()
            f = q
        else:
            c = inc(counter,c)
    f.pretty_print()
    
def inc(counter, c):
    i = 0
    while i <= c:
        counter[i] += 1
        if counter[i] == P:
            counter[i] = 0
            i += 1
        else:
            break
    
    if counter[c] != 1: # Means we've overflowed, we skip non monic polynomials.
        counter[c] = 0
        c += 1
        counter[c] = 1
    return c



if __name__ == "__main__":
    f = Polynomial([-2,0,0,0,0,1], P)
    #f = Polynomial([-1,0,0,0,0,1],P)
    #f = Polynomial([0],P)
    #f.pretty_print()
    factorise(f)