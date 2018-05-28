# CIS 473/573
# Homework #5
# Daniel Lowd
# May 2018
#
# TEMPLATE CODE
#
import sys
import tokenize
import operator
import itertools

# List of variable cardinalities is global, for convenience.
# NOTE: This is not a good software engineering practice in general.
# However, the autograder code currently uses it to set the variable 
# ranges directly without reading in a full model file, so please keep it
# here and use it when you need variable ranges!
var_ranges = []

#
# FACTOR CLASS
#
def get_strides(scope) :
    global var_ranges
    strides = []
    for i in range(len(scope)) :
        strides.append(1)
        for j in range(i) :
            strides[i] = strides[i]*var_ranges[scope[j]]
    return strides

def get_num_values(scope) :
    vals = 1
    for i in scope :
      vals = vals*var_ranges[i]
    return vals

class Factor:

    def __init__(self, scope_, vals_):
        self.scope = scope_
        self.vals = vals_
        stride_ = get_strides(scope_)
        self.stride = dict(zip(scope_, stride_))

    def __mul__(self, other):
        """Returns a new factor representing the product."""
        #calculate new scope for the variables.
        newScope = list(set().union(self.scope, other.scope))
        numVars = len(newScope)
        assignment = [0 for i in range(numVars)]
        stride_ = get_strides(newScope)
        stride = dict(zip(newScope, stride_))
        #print("**************************")
        #print(newScope)
        #print(assignment)
        #print(self.stride)
        maxIter = get_num_values(newScope)
        j = 0
        k = 0
        newVals = []
        for i in range(maxIter) :
            newVals.append(self.vals[j]*other.vals[k])
            for l in range(numVars) :
                currVar = newScope[l]
                assignment[l] = assignment[l] + 1
                cardinality = var_ranges[currVar]
                if assignment[l] == cardinality :
                    assignment[l] = 0
                    j = j - (cardinality - 1)*self.stride.get(currVar, 0)
                    k = k - (cardinality - 1)*other.stride.get(currVar, 0)
                else :
                    j = j + self.stride.get(currVar, 0)
                    k = k + other.stride.get(currVar, 0)
                    break
        #print(newVals)
        #print("**************************")
        # Return the same until the first part is done.
        new_scope = newScope
        new_vals  = newVals
        return Factor(new_scope, new_vals)

    def sumout(self, v):
        #print(self.__repr__())
        newScope = self.scope[:]
        newScope.remove(v)
        oldNumVals = len(self.vals)
        newNumVals = get_num_values(newScope)
        varRange = var_ranges[v]
        varStride = self.stride.get(v, 0)
        newVals = [0] * newNumVals
        pointer = 0
        opps = 0
        jumps = 1
        for i in range(newNumVals) :
            # print("****************Value for %d" %i)
            acc = pointer
            for j in range(varRange) :
                newVals[i] = newVals[i] + self.vals[acc]
                # print ("adding %d : %f, after : %f" %(acc, self.vals[acc], newVals[i]))
                acc = acc + varStride
            opps = opps + 1
            pointer = pointer + 1
            if(opps == varStride) :
                opps = 0
                pointer = jumps*varRange*varStride
                # print("Pointer jumped to %d" %pointer)
                jumps = jumps + 1 
        #print(newVals)
        #print("**************************")
        new_scope = newScope
        new_vals  = newVals
        return Factor(new_scope, new_vals)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def __repr__(self):
        """Return a string representation of a factor."""
        rev_scope = self.scope[::-1]
        val = "x" + ", x".join(str(s) for s in rev_scope) + "\n"
        itervals = [range(var_ranges[i]) for i in rev_scope]
        for i,x in enumerate(itertools.product(*itervals)):
            val = val + str(x) + " " + str(self.vals[i]) + "\n"
        return val
