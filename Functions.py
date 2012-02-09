"""This file contains functions that only call standard libraries
"""
import random

def weighted_selection(elements, weights=None):
    """Takes as input two list. The first is the elements and in the same
    order the second list should contain their weights (default all equal) 
    in the same order. The output is a random element
    """
    if weights:
        r = random.uniform(0,sum(weights))
        sub_total = 0
        for i, w in enumerate(weights):
            sub_total += w
            if sub_total > r:
                return elements[i]
        return elements[i]
    else:
        return random.choice(elements)

def bp_positions(sec_struct):
    """This function takes as input a secondary structure,
    without pseudo-knots, and outputs a list of tuples (a,b)
    of the interacting  nucleotides ( 0 <= a < b < n )
    """
    left_bps = [] #Keeps track of the seen '('
    base_pairs = [] #Keeps track of the completed base pairs
    for i, position in enumerate(sec_struct):
        if position == '(':
            left_bps.append(i)
        #Every closing must match the last opening
        elif position == ')':
            base_pairs.append((left_bps.pop(), i))
    return base_pairs

if __name__ == '__main__':
    print bp_positions('....(((.(....)..))).')

    bob = ['a', 'b', 'c']
    print weighted_selection(bob, [3,1,1])
