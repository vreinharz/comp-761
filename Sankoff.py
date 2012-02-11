class rna_leaf():
    def __init__(self,number,name,sequence):
        self.number = number
        self.name = name
        self.sequence = sequence

def Sankoff(rna1, rna2, weights=None):
    """We output a [4-tuples] with the values of 'A,C,G,U'
       given 2 instances of rna_leaf, 1 rna_leaf and 1 [4-tuples]
       or 2 [4-tuples].
    """

    def Sankoff_1_rna_leaf(rna1, rna2, weights):
        if isinstance(rna1, rna_leaf):
            seq = rna1.sequence
            profile = rna2
        else:
            seq = rna2.sequence
            profile = rna1
        sank = []
        nuc = ['A', 'C', 'G', 'U']
        for i in range(len(seq)):
            this_nuc_vals = []
            for j, x in enumerate(nuc):
                this_nuc_vals.append(weights[x][seq[i]] + profile[i][j])
            sank.append(tuple(this_nuc_vals))
        return tuple(sank)

    def Sankoff_2_rna_leafs(rna1, rna2, weights):
        seq1 = rna1.sequence
        seq2 = rna2.sequence
        sank = []
        nuc = ['A', 'C', 'G', 'U']
        for i in range(len(seq1)):
            this_nuc_vals = []
            for x in nuc:
                this_nuc_vals.append(weights[x][seq1[i]] + 
                                     weights[x][seq2[i]])
            sank.append(tuple(this_nuc_vals))
        return tuple(sank)

    if isinstance(rna1, rna_leaf) or isinstance(rna2, rna_leaf):
        if not weights:
            weights = {'A':{'A':0, 'C':5, 'G':2, 'U':5},
                       'C':{'A':5, 'C':0, 'G':5, 'U':2},
                       'G':{'A':2, 'C':5, 'G':0, 'U':5},
                       'U':{'A':5, 'C':2, 'G':5, 'U':0}}
        if isinstance(rna1, rna_leaf) and isinstance(rna2, rna_leaf):
            return Sankoff_2_rna_leafs(rna1, rna2, weights)
        else:
            return Sankoff_1_rna_leaf(rna1, rna2, weights)
    else:
        sank = []
        for i in range(len(rna1)):
            sank.append(tuple([rna1[i][j] + rna2[i][j] for j in range(4)]))
        return tuple(sank)

class internal_node():

    def __init__(self, left, right, data=None):
        self.left = left
        self.right = right
        self.data = data

if __name__ == '__main__':
    rna2 = rna_leaf('1', 'a', 'UAGC')
    rna1 = rna_leaf('2', 'b', 'UAGC')
    print Sankoff(((1,1,1,1),(1,2,3,4),(1,2,3,4),(1,2,1,1)), 
    ((1,1,1,1),(1,2,3,4),(1,2,3,4),(1,2,1,1)))

