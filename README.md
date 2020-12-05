# FiniteFieldFac
A finite field factoriser written with python and PyQt5.

## Table of Contents
* [General Info](#general-info)
* [Structure](#structure)
* [Running the program](#running)
## General Info
In algebra (including number theory and algebraic geometry) we often care about finite fields of the form F_p^n = GF(p^n).
The motivation is to be able to factor a (monic) polynomial in GF(p^n)[x] into irreducible factors.

## structure
interface_layouts contains work in progress layouts. <br />
legacy contains prototype code. <br />
src:
* fields.py interprets integer valued lists as elements in Fp^r
* polynomial.py interprets lists of field elements as polynomials in Fp^r[x]
* interface.py is the driver, runs the interface
* parse_polynomial.py reads strings and returns lists representing polynomials
* finite_field_factorisation.py contains the main factoring algorithms.
tests contains tests for all of the above.

## Running
To run the program execute:
```
$ cd src
$ python3 interface.py
```