"""This file contain functions who need to call the ViennaRNA API. 
For instructions on how to install it, go at the bottom of:
       http://biopython.org/wiki/Scriptcentral
"""
import RNA
import Functions
import math

RNA.cvar.fold_constrained = 1 #To allow use of constraints on folding

def mfe(S, G=None):
    """Returns the tuple (structure, mfe)  of an RNA sequence S. 
    A string of constraints can be added as a second argument.
    """
    return RNA.fold(S, G)

def mfe_bp_distance(S, G, masked=None):
    """This function takes an RNA sequence S, a secondary structure G,
    and returns de base pairs distance between the mfe structure (a mask
    for the folding can be provided as an optional argument) of S
    and G
    """
    Sec_struct = RNA.fold(S)[0]
    return RNA.bp_distance(Sec_struct, G)

def fold_probability(S, G=None):
    """Given a sequence S a secondary structure G (default mfe), we compute 
    the partition function of S given G as a constraint. The output
    is a triple (A,B,C) where A is the annotated partition folding,
    B is the energie of the ensemble A, and C a dictionary having as keys 
    a pair of positions and as value the probability of having the pair.
    """
    struct, energy = RNA.pf_fold(S, G) #Compute the partition function
    dict_probabilities = {}
    for left, right in ((x,y) for x in range(len(S)) for y in range(len(S))
                       if x < y):
        dict_probabilities[left,right] =RNA.get_pr(left + 1,right +1)
    return (struct, energy, dict_probabilities)

def entropy(Dic):
    """Returns the entropy value of a set of probabilities stored in a dictionary
    """
    ent=0
    for i,j in Dic.iteritems():
        if j > 0: ent = ent + (j * math.log(j,2))
    ent=ent*-1
    return ent

if __name__ == '__main__':
    a = 'GGGGCCCC'
    print mfe(a)
    print mfe(a, 'xxxxxxxx')
    print mfe_bp_distance(a, '......')
    print RNA.fold(a)
    print fold_probability(a, '((....))')
    print fold_probability(a, '........')

