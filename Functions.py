"""This file contains functions that only call standard libraries
"""
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
