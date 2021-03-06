from functools import reduce

def lift_el(x):
    """Takes an element and brackets it."""
    if x == 0:
        return []
    return [x]

def process(term):
    # Terms are of the form: nx^d | nx | n | x^d | x
    if term == 'x':
        return [1,1]

    splt = term.split("x")

    if len(splt) == 1:
        return [int(splt[0]), 0]

    elif splt[0] != '' and splt[1] != '':
        return [int(splt[0]), int(splt[1][1:])]

    elif splt[1] != '':
        return [1, int(splt[1][1:])]

    elif splt[0] != '':
        return [int(splt[0]), 1]

    else:
        return [1,0]

def parse_unbracketed(f, as_integer=False):
    """Takes a string representing a completely expanded polynomial (integer coefficients)
       and returns it as a list.
       """
    # Remove spaces and normalise - signs and split
    terms = f.replace(" ","").replace("-","+-").split("+")
    terms_parsed = list(map(process, terms))

    deg   = max(map(lambda x: x[1], terms_parsed))
    
    out   = [0 for i in range(deg+1)]

    for t in terms_parsed:
        if t[0] == '':
            out[t[1]] += 1
        else:
            out[t[1]] += t[0]

    if as_integer:
        return out

    return list(map(lift_el, out))
