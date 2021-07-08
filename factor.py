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
from functools import reduce

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

    # Initialize a new factor object.
    def __init__(self, scope_, vals_):
        super().__init__()
        self.scope = scope_
        self.vals = vals_
        # Create dictionary from variable -> stride,
        # which will help when iterating through factor entries.
        self.stride = {}
        curr_stride = 1
        for v in scope_:
            self.stride[v] = curr_stride
            curr_stride *= var_ranges[v]
        # DEBUG
        # print "Scope:  ",self.scope
        # print "Stride: ",self.stride
        # print "Values: ",self.vals

    # Factor multiplication
    def __mul__(self, other):
        global var_ranges

        # New factor scope is union of the scopes of the old factors
        new_scope = list(set.union(set(self.scope), set(other.scope)))

        # Initialize helper variables for iterating through factor
        # tables.  First factor is "self", second is "other".
        phi1, stride1, index1 = self.vals, self.stride, 0
        phi2, stride2, index2 = other.vals, other.stride, 0

        # assignment keeps track of the current state of all
        # variables, which determines which factor entries to
        # multiply.
        assignment = {}
        for v in new_scope:
            assignment[v] = 0

        # Iterate through all variable assignments in the scope of the
        # new factor.  For each assignment, create the entry in the
        # new factor by multiplying the corresponding entries in the
        # original factors.  Use indices into each original factor,
        # and use variable strides to update them as we go.
        new_vals = []
        num_vals = reduce(operator.mul, [var_ranges[v] for v in new_scope], 1)
        for i in range(num_vals):
            # Add new value to the factor
            new_vals.append(phi1[index1] * phi2[index2])

            # Update indices
            # If incrementing the first variable would go past its range,
            # set it to zero and try to increment the next one, etc.
            #   e.g., (0,0,1,1) -> (0,1,0,0)
            # Once we succeed in incrementing a variable, stop.
            for v in new_scope:
                if assignment[v] == var_ranges[v] - 1:
                    if v in stride1:
                        index1 -= stride1[v] * assignment[v]
                    if v in stride2:
                        index2 -= stride2[v] * assignment[v]
                    assignment[v] = 0

                # If we can increment this variable, do so and stop
                else:
                    assignment[v] += 1
                    if v in stride1:
                        index1 += stride1[v]
                    if v in stride2:
                        index2 += stride2[v]
                    break
        return Factor(new_scope, new_vals)

    def sumout(self, v):
        # You don't have to keep this code -- it's just one way of starting the problem.
        # This creates a new scope and a new set of values, initially zero, for the new
        # factor. You'll need to figure out how to compute the correct values.

        """
        For the scope - sum out values with similar entries
        (i.e. a_0b_0 + a_0b_1 if we are removing b)
        This means we want to find the two entries required to remove the variable, add them together, and then
        add it to the values

        """
        new_scope = self.scope[:]
        stride = self.stride[v]
        new_vals = []
        # print('initail vals: ',self.vals)
        iter = [0 for i in range(len(self.vals))]
        for i in range(len(self.vals)):
            if iter[i] is 0:
                int = 0
                # print(var_ranges[i])
                for k in range(var_ranges[v]):
                    int += self.vals[i+stride*k]
                    iter[i+stride*k] = 1
                new_vals.append(int)
        new_scope.remove(v)
        # print("finished values: ",new_vals)
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


# def _main():
#     global var_ranges
#     var_ranges = [2, 2, 2, 2, 3, 3, 5]
#     f3 = Factor([1], [4, 5])
#     f4 = Factor([1, 2], [2.0, 1.0, 0.5, 0.25])
#     f5 = Factor([1,4], [1,2,3,4,5,6])
#     f34 = f3 * f4
#     final = f4.sumout(1)
#     print(final.vals)
#
#
# if __name__ == "__main__":
#     _main()
