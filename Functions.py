import re

def bp_positions(sec_struct):
    """This function takes as input a secondary structure,
    and outputs a list of tuples (a,b) of the interacting
    nucleotides ( 0 <= a < b < n )
    """
    #First find position of all opening parenthesis
    pattern_open = re.compile("\(")
    open_match = [match.start() for match in 
                  pattern_open.finditer(sec_struct)]
    patter_close = re.compile("\)")
    close_match = [match.start() for match in 
                  pattern_close.finditer(sec_struct)]


