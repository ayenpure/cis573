# CIS 473/573
# Homework #4
# Daniel Lowd
# May 2018
#
# TEMPLATE CODE
#
# You shouldn't need to modify this file at all. You can edit it to
# help with debugging, but you will only submit factor.py.
#

import sys
import tokenize
import itertools
from functools import reduce

# Import your factor class, which you will have to complete.
import factor

#
# READ IN MODEL FILE
#

# Read in all tokens from stdin.  Save it to a (global) buf that we use
# later.  (Is there a better way to do this? Almost certainly.)
curr_token = 0
token_buf = []

def read_tokens():
    global token_buf
    for line in sys.stdin:
        token_buf.extend(line.strip().split())
    #print("Num tokens:",len(token_buf))

def next_token():
    global curr_token
    global token_buf
    curr_token += 1
    return token_buf[curr_token-1]

def next_int():
    return int(next_token())

def next_float():
    return float(next_token())

def read_model():
    # Read in all tokens and throw away the first (expected to be "MARKOV")
    read_tokens()
    s = next_token()

    # Get number of vars, followed by their ranges
    num_vars = next_int()

    # NOTE: Variable ranges are set as a module variable in factor.py.
    # Therefore, you can't load two models at the same time.
    # This is bad software engineering practice in general, but it
    # makes this assignment slightly simpler.
    factor.var_ranges = [next_int() for i in range(num_vars)]

    # Get number and scopes of factors 
    num_factors = int(next_token())
    factor_scopes = []
    for i in range(num_factors):
        scope = [next_int() for i in range(next_int())]
        # NOTE: 
        #   UAI file format lists variables in the opposite order from what
        #   the pseudocode in Koller and Friedman assumes. By reversing the
        #   list, we switch from the UAI convention to the Koller and
        #   Friedman pseudocode convention.
        scope.reverse()
        factor_scopes.append(scope)

    # Read in all factor values
    factor_vals = []
    for i in range(num_factors):
        factor_vals.append([next_float() for i in range(next_int())])

    # DEBUG
    # print("Num vars: ",num_vars)
    # print("Ranges: ",factor.var_ranges)
    # print("Scopes: ",factor_scopes)
    # print("Values: ",factor_vals)
    return [factor.Factor(s,v) for (s,v) in zip(factor_scopes,factor_vals)]


#
# MAIN PROGRAM
#

if __name__ == "__main__":
    factors = read_model()
    #print(factors)
    # Compute Z by brute force
    f = reduce(factor.Factor.__mul__, factors)
    print(f.__repr__())
    z = sum(f.vals)
    print("Z = ",z)
