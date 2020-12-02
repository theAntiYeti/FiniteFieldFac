from fields import FiniteField as FF
from polynomial import Polynomial as poly
from functools import reduce
def var_max(x,y):
    if x > y:
        return x
    return y

def parse_unbracketed(f):
    """Takes a string representing a completely expanded polynomial and returns it as a list."""
    terms = list(map(lambda x: x.split('x^'),f.replace(" ","").split('+')))
    deg   = reduce(lambda x,y: var_max(int(x[1]), int(y[1])), terms)
    
    out   = [0 for i in range(deg+1)]

    for t in terms:
        if t[0] == '':
            out[int(t[1])] += 1
        else:
            out[int(t[1])] += int(t[0])
    print(out)
    return out

if __name__ == "__main__":
    print(parse_unbracketed("x^5 + 4 x ^2"))
    print(parse_unbracketed('x^2 + x^0'))