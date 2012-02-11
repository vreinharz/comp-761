import sys
import Functions 

def Sankoff(rnas, weights=None):
    """Given a list of rnas sequence or profiles (must be a 4-tuple
    in the order "A, C, G, U") will output the 'Sankoff' (tuple of
    4-tuples of sankoffs values in the order "A,C,G,U"). An
    optional weight dict can be added, there is a default one just below.
    """
    if not weights and any([isinstance(rna, str) for rna in rnas]):
        weights = {'A':{'A':0, 'C':5, 'G':2, 'U':5},
                   'C':{'A':5, 'C':0, 'G':5, 'U':2},
                   'G':{'A':2, 'C':5, 'G':0, 'U':5},
                   'U':{'A':5, 'C':2, 'G':5, 'U':0}}
    #We search for the leaves and sequences
    leaves = []
    internal = []
    for rna in rnas:
        if isinstance(rna, str):
            leaves.append(rna)
        else:
            internal.append(rna)
    #They should all have the same length so it doesn't matter
    nucleotides = ['A', 'C', 'G', 'U']
    sank = []
    for i in range(len(rnas[0])):
        this_position = [0,0,0,0] #we start with 0 for every nucleotide
        for rna in leaves:
            for j, nuc in enumerate(nucleotides):
                this_position[j] += weights[rna[i]][nuc]
        for rna in internal:
            for j in range(4):
                this_position[j] += rna[i][j]
        sank.append(tuple(this_position))
    return tuple(sank)

def Newick_parser(tree):
    """Given a string of a tree in the Newick format,where
    leafs are the only elements to have names!.
    Will output the tree in the following format:
        every internal node is a list of its children, every leaf
        is a string of its name.
    """
    positions = Functions.bp_positions(tree)
    if not positions:
        return tree.replace('+', '_').split('|')[-1]
    positions.remove((0, len(tree)-1))
    commas = [i for i, x in enumerate(tree) if x == ',']
    separators = []
    #We check for all separators of our current node
    for i in commas:
        if all([ (i < x[0] or x[1] < i) for x in positions]):
            separators.append(i)
    newick_vals = [Newick_parser(tree[1:separators[0]]),
                   Newick_parser(tree[separators[-1]+1:-1])]
    for i in range(1, len(separators)-1):
        newick_vals.append(tree[separators[i]+1:separators[i+1]])
    return newick_vals

def make_sankoff_profile(tree):
    """Given a rna tree as outputed by Newick_parser,
    will create the sankoff profile.
    Every node in the profile is or an rna string(leaf) 
    a 3-tuple where the 0st element is 
    the name, the second the 'sankoff value' of the node
    (in order 'A, C, G, U'), and the last element is
    a tuple of children.
    """
    tree = tree[:] #copy so we don't overwrite
    if isinstance(tree, str) or isinstance(tree, tuple):
        return tree
    #If we are not at the leaf, or computed value, pick the childs
    children = []
    sank = []
    name = []
    for child in tree:
        if isinstance(child, str):
            name.append(child)
            sank.append(child)
            children.append(child)
        elif isinstance(child, tuple):
            name.append(child[0])
            sank.append(child[1])
            children.append(child)
        else:
            child = make_sankoff_profile(child)
            name.append(child[0])
            sank.append(child[1])
            children.append(child)
    tree = ('_'.join(name), Sankoff(sank), tuple(children))
    return tree

def write_tree_profile(tree, file_path):





if __name__ == '__main__':
    tree_seq = [x.strip() for x in open('sample.tree')][0][1:-1]
    #print Sankoff(['AUGC', 'CGAC'])
    #print Functions.bp_positions(tree_seq)
    a = Newick_parser('((AUGC,AUGC),CGAA)')
    b = make_sankoff_profile(a)
    print b
