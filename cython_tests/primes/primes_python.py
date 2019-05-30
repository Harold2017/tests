#!/usr/bin/env python3
"""
@author:Harold
@file: primes_python_cy.py
@time: 30/05/2019
"""


def primes_python(nb_primes):
    p = []
    n = 2
    while len(p) < nb_primes:
        # Is n prime?
        for i in p:
            if n % i == 0:
                break
        # If no break occurred in the loop
        else:
            p.append(n)
        n += 1
    return p
