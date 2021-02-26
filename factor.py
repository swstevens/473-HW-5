# CIS 473/573
# Homework #5
# Daniel Lowd
# February 2021
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

class Factor:

    def __init__(self, scope_, vals_):
        self.scope = scope_
        self.vals = vals_
        # TODO -- ADD YOUR CODE FROM HW4 HERE IF NEEDED 

    def __mul__(self, other):
        """Returns a new factor representing the product."""
        # TODO -- ADD YOUR CODE FROM HW4 HERE
        # BEGIN PLACEHOLDER CODE -- DELETE THIS! 
        new_scope = self.scope
        new_vals  = self.vals
        # END PLACEHOLDER CODE
        return Factor(new_scope, new_vals)

    def sumout(self, v):
        # You don't have to keep this code -- it's just one way of starting the problem.
        # This creates a new scope and a new set of values, initially zero, for the new
        # factor. You'll need to figure out how to compute the correct values.
        new_scope = self.scope[:]
        new_scope.remove(v)
        new_vals = []

        #### YOUR HW5 CODE GOES HERE ####

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
