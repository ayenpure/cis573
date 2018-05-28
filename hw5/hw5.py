# CIS 473/573
# Homework #5
# Daniel Lowd
# May 2018
#
# TEMPLATE CODE 
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
    #print("Num vars: ",num_vars)
    #print("Ranges: ",factor.var_ranges)
    #print("Scopes: ",factor_scopes)
    #print("Values: ",factor_vals)
    return [factor.Factor(s,v) for (s,v) in zip(factor_scopes,factor_vals)]



#
# MAIN PROGRAM
#
# 
def compute_z_varelim_vanilla(factors):
    while len(factors) != 1 :
        for i in range(len(factor.var_ranges)) :
            #print("**********Eliminating %d**********" %i)
            currentFactors = []
            for f in factors :
                if i in f.scope :
                    currentFactors.append(f)
            if len(currentFactors) == 0 :
                continue
            toEleminate = currentFactors.pop(0)
            factors.remove(toEleminate)
            for f in currentFactors :
                factors.remove(f)
                toEleminate = toEleminate.__mul__(f)
            eleminated = toEleminate.sumout(i)
            #print(eleminated.__repr__())
            factors.append(eleminated)
    return (factors[0])[0]

# Optimized Version
def compute_z_varelim(factors):
    numVars = len(factor.var_ranges)
    toSort = [0] * numVars
    varsList = []
    for i in range(numVars) :
        varsList.append(i)
        for f in factors :
            if i in f.scope :
                toSort[i] = toSort[i] + 1
    zipped_pairs = zip(toSort, varsList)
    z = [x for _, x in sorted(zipped_pairs)]
    for i in z :
        #print("**********Eliminating %d**********" %i)
        currentFactors = []
        for f in factors :
            if i in f.scope :
                currentFactors.append(f)
        #if len(currentFactors) == 1 and len(currentFactors[0].scope) == 1:
        #    continue
        toEleminate = currentFactors.pop(0)
        factors.remove(toEleminate)
        for f in currentFactors :
            factors.remove(f)
            toEleminate = toEleminate.__mul__(f)
        # if len(toEleminate.scope) == 1 :
        #    print(toEleminate.__repr__())
        #    factors.append(toEleminate)
        #    continue
        #else :
        eleminated = toEleminate.sumout(i)
        #print(eleminated.__repr__())
        factors.append(eleminated)
        #   continue
    #print "Total Factors : "
    #print len(factors)
    #for f in factors :
    #    print(f.__repr__())
    #toReduce = list(map(factor.Factor.sumout, factors))
    #print "To Reduce : "
    #print len(toReduce)
    #f = reduce(factor.Factor.__mul__, factors)
    #z = sum(f.vals)
    f = reduce( (lambda f1, f2: f1 * f2), factors)
    return f.vals[0]    

if __name__ == "__main__":
    factors = read_model()
    #f = reduce(factor.Factor.__mul__, factors)
    #print(f.__repr__())
    #newf = f.sumout(1)
    #print(newf.__repr__())
    # Compute Z by variable elimination
    z = compute_z_varelim(factors)
    print("Z = ",z)
