import os
import sys
import Functions as Fct
import ViennaRNA as VRNA

"""The general strategy here will be to recreate the phylogenetic tree
where each node will contains the profile (as a valid input to
Function.rand_rna() ).
Then for each node we will generate 1000random sequences with the given
profile and apply our 6 metrics to them (contained in VRNA:
    1) MFE value
        "mfe"
    2) MFE value when masked with concensus
        "mfe_masked"
    3) Base pair distance of MFE structure and concensus.
        "mfe_bp_distance"
    4) Base pair distance of folding masked with concensus and concensus
        "masked_bp_distance"
    5) Energy of ensemble of folding in mfe (pf_fold)
        "mfe_energy"
    6) Energy of ensemble of folding masked with concensus
        "masked_energy"

"""
metrics_list = ['mfe', 'mfe_masked', 'mfe_bp_distance', 
                'masked_bp_distance', 'mfe_energy', 'masked_energy']

def do_benchmarks(rna_list, concensus):
    """Fill a dictionnary benchmark with the Functions.do_stats
    output for the 6 metric. the keys of benchmark are the node
    names, values a dict{"metric_name", Functions.do_stats}
    """
    benchmark = {} #We will keep track of the benchmark in this dict
    for rna in rna_list: 
        benchmark[rna] = {}
        #Now we want to generate a population, and do all the benchmarks
        #on them.
        pop = Fct.rand_rna_population(rna_list[rna])

        #The first test is the mfe
        mfe = [VRNA.mfe(sequence)[1] for sequence in pop]
        benchmark[rna]['mfe'] = Fct.do_stats(mfe)

        #Masked mfe
        mfe_masked = [VRNA.mfe(sequence, concensus)[1] 
                    for sequence in pop]
        benchmark[rna]['mfe_masked'] = Fct.do_stats(mfe_masked)

        #MFE bp_distance
        mfe_bp_distance = [VRNA.mfe_bp_distance(sequence, concensus) 
                       for sequence in pop]
        benchmark[rna]['mfe_bp_distance'] = Fct.do_stats(mfe_bp_distance)

        #folding masked bp_distance
        masked_bp_distance = [VRNA.mfe_bp_distance(sequence, concensus,
                                                  concensus) 
                       for sequence in pop]
        benchmark[rna]['masked_bp_distance'] = Fct.do_stats(
            masked_bp_distance)

        #MFE Energy ensemble
        mfe_energy = [VRNA.fold_probability(sequence)[1]
                      for sequence in pop]
        benchmark[rna]['mfe_energy'] = Fct.do_stats(mfe_energy)

        #MFE Energy ensemble
        masked_energy = [VRNA.fold_probability(sequence)[1]
                         for sequence in pop]
        benchmark[rna]['masked_energy'] = Fct.do_stats(masked_energy)
    return benchmark



if __name__ == '__main__':
    path_file_rnas = 'sample.txt'
    concensus = '(...........)'
    rna_list = Fct.parse_masoud_file(path_file_rnas)

    benchmark = do_benchmarks(rna_list, concensus)
    
    #Now that we have all the info, we want to create a list of
    node_names = benchmark.keys()
    paths = Fct.paths_root_leafs(node_names)
    print paths
    print
    print

    """
    for rna in benchmark:
            print rna
            for metric in benchmark[rna]:
                print '\t%s:' % metric
                print '\t\tmean\tsd\tmin\tmax'
                print '\t\t%.2f\t%.2f\t%.2f\t%.2f' % benchmark[rna][metric]
    """



         

