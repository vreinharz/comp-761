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

def make_rna_profile(profile, start_char='(', end_char='Z'):
    """Given an rna sequence or profile, will output a 4-tuple
    of strings where each one is the probability of a given nucleotide
    to be at a given place in the order 'A, C, G, U'"""
    probs = {x:[] for x in ('A', 'C', 'G', 'U')}
    if isinstance(profile, str):
        for nuc in profile:
            for x in probs:
                if x == nuc:
                    probs[x].append(end_char)
                else:
                    probs[x].append(start_char)
        return '\n'.join((''.join(probs['A']),
                         ''.join(probs['C']),
                         ''.join(probs['G']),
                         ''.join(probs['U'])))
    else:#We have a sankoff profile
        nucleotides = ('A', 'C', 'G', 'U')
        for nuc in profile:
            #First check if one is 0
            if 0 in nuc:
                for i, x in enumerate(nuc):
                    if x == 0:
                        probs[nucleotides[i]].append(end_char)
                    else:
                        probs[nucleotides[i]].append(start_char)
            else: #We just compute as partition the sum of inverses
                inverse_sum = sum((1.0/x for x in nuc)) 
                for i, x in enumerate(nuc):
                        span = (1.0/x)/inverse_sum
                        char_range = ord(end_char) - ord(start_char)
                        probs[nucleotides[i]].append(chr(int(
                            span*char_range + ord(start_char))))
        return '\n'.join((''.join(probs['A']),
                         ''.join(probs['C']),
                         ''.join(probs['G']),
                         ''.join(probs['U'])))

def write_tree_profile(tree, file_obj):
    """Given a file_obj open to append text, will write
    in it the profile of a "sankoff profile"
    """
    if isinstance(tree, str):
        file_obj.write('>%s\n' % tree)
        file_obj.write(make_rna_profile(tree) + '\n')
    else:
        name = [tree[0]]
        for child in tree[2]:
            name.append(child[0])
            write_tree_profile(child, file_obj)
        file_obj.write('>' + '+'.join(name) + '\n')
        file_obj.write(make_rna_profile(tree[1]))
    return None




if __name__ == '__main__':
    tree_seq = [x.strip() for x in open('sample.tree')][0][1:-1]
    #print Sankoff(['AUGC', 'CGAC'])
    #print Functions.bp_positions(tree_seq)
    a = Newick_parser(tree_seq)
    b = make_sankoff_profile(a)
    with open('sank.txt', 'w') as sank:
        write_tree_profile(b, sank)
