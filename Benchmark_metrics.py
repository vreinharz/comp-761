import os
import sys
import Functions as Fct
import ViennaRNA as VRNA
import LaTeX
from matplotlib import pyplot as plt

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
        benchmark[rna]['mfe'] = (mfe)

        #Masked mfe
        mfe_masked = [VRNA.mfe(sequence, concensus)[1] 
                    for sequence in pop]
        benchmark[rna]['mfe_masked'] = (mfe_masked)

        #MFE bp_distance
        mfe_bp_distance = [VRNA.mfe_bp_distance(sequence, concensus) 
                       for sequence in pop]
        benchmark[rna]['mfe_bp_distance'] = (mfe_bp_distance)

        #folding masked bp_distance
        masked_bp_distance = [VRNA.mfe_bp_distance(sequence, concensus,
                                                  concensus) 
                       for sequence in pop]
        benchmark[rna]['masked_bp_distance'] = (
            masked_bp_distance)

        #MFE Energy ensemble
        mfe_energy = [VRNA.fold_probability(sequence)[1]
                      for sequence in pop]
        benchmark[rna]['mfe_energy'] = (mfe_energy)

        #MFE Energy ensemble
        masked_energy = [VRNA.fold_probability(sequence)[1]
                         for sequence in pop]
        benchmark[rna]['masked_energy'] = (masked_energy)
    return benchmark

def get_node_stats(node_id, benchmarks, metric):
    """Given a node_id, benchmarks and metric,
    return the stats of the node for the given metric
    as the tuple (avg, sd, min, max)
    """
    for node in benchmarks.keys():
        if node.split('+')[0] == node_id:
            return benchmarks[node][metric]
    return None
    
def plot_benchmarks(benchmarks, paths, metric):
    for path in paths:
        data = []
        for i, node_id in enumerate(path):
            data.append(get_node_stats(node_id, benchmarks, metric))
        plt.boxplot(data)    
        plt.xlabel('->'.join(path), fontsize='22')
        plt.ylabel(metric, fontsize='22')
        plt.rc('font', size=17)
        plt.savefig('%s_%s' % ('_'.join(path), metric))
        

if __name__ == '__main__':
    path_file_rnas = 'sample.txt'
    concensus = '(...........)'
    rna_list = Fct.parse_masoud_file(path_file_rnas)

    benchmarks = do_benchmarks(rna_list, concensus)
    
    #Now that we have all the info, we want to create a list of
    node_names = benchmarks.keys()
    paths = Fct.paths_root_leafs(node_names)

    #Since we are lazy, lets do a latex file
    list_tex = [LaTeX.standard_header()]
    for metric in metrics_list:
        plot_benchmarks(benchmarks, paths, metric)
        #We add a section for this metric, and we will
        #do 3x2 figures per page.
        list_tex.append("\\newpage\\section{%s}" % 
                        metric.replace('_', '\\_'))
        #Now we want a list of the names of the figures of the metric
        metric_figs_names = [x for x in os.listdir('.') if 
                             x.endswith('%s.png' % metric)]
        list_tex.append(LaTeX.figure_env(metric_figs_names))
    list_tex.append('\\end{document}')
    with open('main.tex', 'w') as latex_file:
        latex_file.write("\n".join(list_tex))
    os.system('pdflatex main.tex && pdflatex main.tex')
    os.system('rm *.png')

