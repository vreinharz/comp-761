"""This file contains functions that only call standard libraries
"""
import random

def find_parent(id, node_names):
    """Given a list of node names in the format A+B+C where A is the 
    unique node identifier and B,C its children name, and the id of a 
    node, the output is the id of the parent.
    """
    for name in node_names:
        if id in name.split('+')[1:]:
            return name.split('+')[0]
    return None

def paths_root_leafs(node_names):
    """Given a list of node names in the format A+B+C where A is the 
    unique node identifier and B,C its children name, the output
    is a list of tuples, each one being the list of nodes from the root
    to a leaf
    """
    paths = []
    leafs = [x[:-2] for x in node_names if x[-2:] == '++']
    ids = [x.split('+')[0] for x in node_names]

    for id in ids:
        #The root is the only id which is not a children in all nodes
        if all([not id in x.split('+')[1:] for x in node_names]):
            root = id
            break

    for leaf in leafs:
        paths.append([leaf]) #we add a new path leaf-root
        actual = leaf
        while actual is not root:
            actual = find_parent(actual, node_names)
            paths[-1].append(actual)
        paths[-1] = list(reversed(paths[-1]))
    return paths

def do_stats(numbers):
    """Given a list of numbers, the output is the tuple:
        (average, standard_deviation, min, max)
    """
    avg = float(sum(numbers))/len(numbers)
    sum_square_diffs = 0
    for x in numbers:
        sum_square_diffs += pow(x - avg, 2)
    sd = pow(sum_square_diffs / len(numbers), 0.5)
    return (avg, sd, min(numbers), max(numbers))

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

def masoud_to_probability_vector(masoud_format, 
                              range_start='(', range_end='Z'):
    """Given the probabilities in the Masoud* format "for an RNA
    sequence, with the encoding starting at the "range_start" char and
    ending at the "range_end" char, we output a tuple of 4-tuple as:
    ( (P_A_1, P_C_1, P_G_1, P_U_1), ..., (P_A_n, P_C_n, P_G_n, P_U_n))
    where 'P_X_i' is the probability of having nucleotide 'X' at pos. 'i'.

    *Masoud format: 4 elements, each line represent a nucleotide
    probability in the order: "A, C, G, U". At the line of nucleotide
    'X', the i-th character represent the probability of having 'X'
    at position 'i'. If the i-th character is 'y', the probability of
    'X' at position 'i' is: (ord('y') - ord(range_start)) /(
        ord(range_end)-ord(range_start))
    """
    vector = []
    probs_range = ord(range_start) - ord(range_end)
    start = ord(range_start)
    end = ord(range_end)
    for pos in range(len(masoud_format[0])):
        vector.append((
            float(ord(masoud_format[0][pos])-start)/(end-start),
            float(ord(masoud_format[1][pos])-start)/(end-start),
            float(ord(masoud_format[2][pos])-start)/(end-start),
            float(ord(masoud_format[3][pos])-start)/(end-start)
        ))
    return tuple(vector)

def parse_masoud_file(file_path):
    """Given the path to a file with a list of RNAs in the masoud format,
    the output is a dictionnary where keys are the name of the RNA
    and values probability vectors
    """
    tree_raw_info = [x.strip() for x in open(file_path)]
    dict_rnas = {}
    position = 0
    while position < len(tree_raw_info):
        if tree_raw_info[position][0] == '>':#Annouce a name.
            name = tree_raw_info[position][1:]#We don't want to keep '>'
            #The four next positions are the probabilities 
            masoud_vector = [tree_raw_info[position + x] 
                             for x in range(1,5)]
            dict_rnas[name] = masoud_to_probability_vector(masoud_vector)
            position += 5
        else:
            position += 1
    return dict_rnas

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

def rand_rna(nuc_probabilities):
    """Generates a random RNA sequence given probabilities
    at each positions contained in "nuc_probabilities. It should be
    an iterable where each element in a 4-tuples (P_A, P_C_, P_G, P_U)
    """
    nucleotides = ['A', 'C', 'G', 'U']
    rna = []
    for position in nuc_probabilities:
        rna.append(weighted_selection(nucleotides, position))
    return ''.join(rna)

def rand_rna_population(probabilities, size=1000):
    """Generates "size" random RNAs given the probability
    vector "probabilities" who must be an iterator, the size
    of the desired RNA, where each position is a 4-tuple
    with the probabilities of the nucleotides: (P_A, P_C, P_G, P_U)
    """
    return [rand_rna(probabilities) for x in range(size)]


if __name__ == '__main__':
    print bp_positions('....(((.(....)..))).')

    print rand_rna_population(masoud_probability_vector([
        '(64<:((ZZZASD',
        'Z34>((((((WQE',
        '(PO}E(((((WEW',
        '(S:>}ZZ((((((']))
