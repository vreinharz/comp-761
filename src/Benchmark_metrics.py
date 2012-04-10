import os
import sys
from optparse import OptionParser
import time
import multiprocessing as MP
import Queue
import Functions as Fct
import ViennaRNA as VRNA
import LaTeX
import matplotlib
matplotlib.use('Agg')
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
    7) Entropy 

"""
metrics_list = ['mfe', 'mfe_masked', 'mfe_bp_distance', 
                'masked_bp_distance', 'mfe_energy', 'masked_energy', 'entropy']


def worker_do_benchmarks(rna_list, concensus, tasks_queue, out_queue):
    """Should be called with do_benchmarks_MP.
    Fill a dictionnary benchmark with the Functions.do_stats
    output for the 7 metric. the keys of benchmark are the node
    names, values a dict{"metric_name", Functions.do_stats}
    """
    benchmark = {} #We will keep track of the benchmark in this dict
   
    while True:
        rna = tasks_queue.get()
        tasks_queue.task_done()
        if rna is None:
            break
        print 'processing rna on process: ', os.getpid()
        benchmark[rna] = {}
        #:Now we want to generate a population, to do all the benchmarks
        pop = Fct.rand_rna_population(rna_list[rna],size=1000)
        
        #pop = [rna_list[rna]]
        
        #The first test is the mfe
        mfe = [VRNA.mfe(sequence)[1] for sequence in pop]
        benchmark[rna]['mfe'] = mfe

        #Masked mfe
        mfe_masked = [VRNA.mfe(sequence, concensus)[1] 
                    for sequence in pop]
        benchmark[rna]['mfe_masked'] = mfe_masked

        #MFE bp_distance
        mfe_bp_distance = [VRNA.mfe_bp_distance(sequence, concensus) 
                       for sequence in pop]
        benchmark[rna]['mfe_bp_distance'] = mfe_bp_distance

        #folding masked bp_distance
        masked_bp_distance = [VRNA.mfe_bp_distance(sequence, concensus,
                                                  concensus) 
                       for sequence in pop]
        benchmark[rna]['masked_bp_distance'] = masked_bp_distance

        #MFE Energy ensemble
        mfe_energy = [VRNA.fold_probability(sequence)[1]
                      for sequence in pop]
        benchmark[rna]['mfe_energy'] = mfe_energy

        #MFE Energy ensemble
        masked_energy = [VRNA.fold_probability(sequence)[1]
                         for sequence in pop]
        benchmark[rna]['masked_energy'] = masked_energy
        
        #Entropy
        ent = [VRNA.entropy(VRNA.fold_probability(sequence)[2])
        			for sequence in pop]
        #print 'valor fuera', ent
        benchmark[rna]['entropy'] = ent

    out_queue.put(benchmark)
    print 'This process computed %s benchmarks.' % len(benchmark)
    return None

def do_benchmarks_MP(rna_list, concensus, nb_processes):
    out_queue = MP.JoinableQueue()
    tasks_queue = MP.JoinableQueue()
    processes = []
    for k in rna_list.keys():
        tasks_queue.put(k)
        print k
    for i in range(nb_processes):
        tasks_queue.put(None)

    for i in range(nb_processes):
        p = MP.Process(target=worker_do_benchmarks, args=(
            rna_list, concensus, tasks_queue,out_queue, ))
        processes.append(p)
        p.start()
    benchmarks = {}
    for i in range(nb_processes):
        benchmarks.update(out_queue.get())
        out_queue.task_done()
    for p in processes:
            p.join()
    return benchmarks

def get_node_stats(node_id, benchmarks, metric):
    """Given a node_id, benchmarks and metric,
    return the stats of the node for the given metric
    as the tuple (avg, sd, min, max)
    """
    for node in benchmarks.keys():
        if node.split('+')[0] == node_id:
            return benchmarks[node][metric]
    return None
    
def plot_one_path_benchmarks(one_path, benchmarks, metric):
    #Do plot for one merged path of all the tree
    data = []
    for ranked_nodes in one_path:
        data.append([])
        for node_id in ranked_nodes:
            data[-1].extend(get_node_stats(node_id, benchmarks, metric))

        plt.rc('text', usetex=True)
        plt.rc('font', size=22)
        plt.boxplot(data)    
        plt.xlabel('From root to the Leafs')
        plt.ylabel(r'%s' % metric.replace('_', ' '))
        plt.savefig('%s_%s' % ('merged', metric))
        plt.clf()
    return None

def worker_plot_benchmarks(tasks_queue, benchmarks, metric):
    while True:
        path = tasks_queue.get()
        tasks_queue.task_done()
        if path is None:
            break
        data = []
        for i, node_id in enumerate(path):
            data.append(get_node_stats(node_id, benchmarks, metric))

        plt.rc('text', usetex=True)
        plt.rc('font', size=22)
        plt.boxplot(data)    
        plt.xlabel('From root to the Leaf  %s.'
                  % path[-1])
        plt.ylabel(r'%s' % metric.replace('_', ' '))
        plt.savefig('%s_%s' % (path[-1], metric))
        plt.clf()
    return None

def plot_benchmarks_MP(benchmarks, paths, metric, nb_processes):
    tasks_queue = MP.JoinableQueue()
    print metric
    for path in paths:
        tasks_queue.put(path)
    for i in range(nb_processes):
        tasks_queue.put(None)
    processes = []
    for i in range(nb_processes):
        p = MP.Process(target=worker_plot_benchmarks, args=(tasks_queue, 
                                                       benchmarks, metric,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    return None

def dummy_benchmarks(rna_list, mlist):
    benchmark = {}
    for rna in rna_list.keys():
        benchmark[rna] = {}
        for metric in mlist:
            benchmark[rna][metric] = ((1,2), (3,4))
    return benchmark
        

if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('-f', '--file', dest='filename', 
                   default='../data/RF00951.sank',
                   help='Path of tree in Masoud format to benchmark')
    opt.add_option('-o', '--output', dest='output_name', default='main',
                   help='Name of the pdf that will be outputed')
    opt.add_option('-p', '--number_processes', dest='nb_processes', 
                   type='int',default=2, help='Max number of processes allowed')
    opt.add_option('-c', '--concensus', dest='concensus', 
                #default goes with first tree we used
              #default='.....<<<<<<<.<<<.<<<<<........>.>>>>.>>>.>>>>>>>....',
              #default RF00032
              #default='..............................................',
              #default RF00130
              #default='.........................................................................................................',
              #default RF01990
              #default='......................................',
              #default RF01771
              default='.............................................................................................................',
                   help='concencus structure of the tree')
    (options, arguments) = opt.parse_args()
    path_file_rnas = options.filename
    nb_processes = options.nb_processes
    output_name = options.output_name
    concensus = options.concensus
    concensus = concensus.replace('<', '(').replace('>', ')')


    start_time = time.time()

    #rna_list = Fct.parse_masoud_file(path_file_rnas)
    rna_list = Fct.parse_ancestors_prob_file_all('../data/RF00951.tree.ancestors.probs_MOD.txt')
    #rna_list = Fct.parse_ancestors_file('../data/RF01771.tree.ancestors')
    #rna_list = {'9685':'TTTTAAGTATAAGTATGTCCCATGCAAAATTTGGGATATACTTATATTAAAA','9615':'TTTTTAGTATAAGTATGTCCTATGCAATATTTGGGACATACTTATACTAAAA','9785':'ATTTTAGTATAAGTATGTCCCATACAATATTTGGGACATACTTATACTAAAA','9371':'TTTCTAATGTAAGTATGTCTCAGGCAATATTTGGGGCATATTTATATTAAAA','9978':'TTTTAAATATAATTATGTACCATGAAATATTTGGGAAATACTTATACTAAAA','9986':'CTTTTAGCATAAGTATATCACATGCAATATTTGGGACATAATTATGCTAAAA','10116':'TATGTAGTATAAGTATGTCCCATGAAGCATTTGGGATATTATTATATTATAC','10090':'TTTTTAGCGTAAGTAAGTCCCATGCAACATTTGGGATATACTTATACTAAAA','9447':'TAAGAAGTATAAGTATGTCCTATGAAGCATTTGAGACATATGTATACTAAAA','30608':'TTTTCAGTATAAGTATGTCCCATGCAATGTTTGGGACATACTTATACTACAA','9523':'TTAAACTTATAAATATGTCCTGTGAAATATTTAAGACATACTTATGCTAAAA','9483':'TTTTAAGTATAGGTATGTCCCATGCAATTTTGGGGATATAGTTATACTAAAT','9606':'TTCGTAGCATAAATATTTCCCAAGCTTAGTTTGGGACATACTTATGCTAAAA','9593':'TTTTTAGGATAAGTAAATCCCATTCAATATTTGTGACATACTTATCCTAAAA','9555':'TGTTTAGTATAAGTATGTCCCATGCAATATTTAGGATGTACTAATACTAAAC','9534':'TTAAACGTATAAGTATGTCCTGTGAAATATTTAGGACATACTTATGCTAAAA','9534+9555':'TGAAAAATATAAGTATGTCCCATGCAATATTTAGGACATACTTATACTAAAA','9544+9534+9555':'TGAAAAATATAAGTATGTCCCATGCAATATTTAGGACATACTTATACTAAAA','9593+9606':'TTAAAAACATAAGTATATCCCATACAATATTTGGGACATACTTATGCTAAAA','9601+9593+9606':'TTAAAAATATAAGTATGTACCATGCAATATTTGGCACATACTTATACTAAAA','61853+9601+9593+9606':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGTATATACTTATACTAAAA','9544+9534+9555+61853+9601+9593+9606':'TAAAAAATATAAGTATGTCCCATACAATATTTAGGATATACTTATACTAAAA','9483+9523':'TTAAAAATATAAATATGTCCTATGCAATATTTAAGATATACTTATACTAAAA','9544+9534+9555+61853+9601+9593+9606+9483+9523':'TAAAAAATATAAGTATGTCCTATATAATATTTAGGATATACTTATACTAAAA','30608+9447':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGACATACTTATACTAAAA','30611+30608+9447':'TTAAAAACATAAGTATGTCCCATGCAATATTTGGGACATATTTATACTAAAA','9544+9534+9555+61853+9601+9593+9606+9483+9523+30611+30608+9447':'TTAAAAATATAAGTATGTCCCATATAATATTTGGGATATACTTATACTAAAA','10090+10116':'TAAAAAATATAAGTATGTCCCATGCAACATTTGGGATATACTTATACTAAAA','43179+10090+10116':'CTAAAAATATAAGTATGTCCTATACAATATTTGGGACATACTTATGCTAAAA','9986+9978':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGACATACTTATACTAAAA','43179+10090+10116+9986+9978':'TTAAAAATATAAGTATGTCCCATATAATATTTGGGATATACTTATACTAAAA','9544+9534+9555+61853+9601+9593+9606+9483+9523+30611+30608+9447+43179+10090+10116+9986+9978':'TTAAAAATATAAGTGTGTCCCATGTAATATTTGGGATATACTTATACTAAAA','37347+9544+9534+9555+61853+9601+9593+9606+9483+9523+30611+30608+9447+43179+10090+10116+9986+9978':'TTAAAAATATAAGTGTGTCCCATGTAATATTTGGGATATACTTATACTAAAA','9371+9785':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGACATACTTATACTAAAA','9615+9685':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGATATACTTATACTAAAA','9417+40233':'TTAAAAATATAATTATGTCCCATGAAGCATTTGAGATATATTTATACTAAAA','42254+9365':'TTAAAAATATAAGTATGTCCCATGCAATATTTGAGATATACTTATACTAAAA','9417+40233+42254+9365':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGATATACTTATACTAAAA','9913+9417+40233+42254+9365':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGATATACTTATACTAAAA','9615+9685+9913+9417+40233+42254+9365':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGATATACTTATACTAAAA','9371+9785+9615+9685+9913+9417+40233+42254+9365':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGATATACTTATACTAAAA','37347+9544+9534+9555+61853+9601+9593+9606+9483+9523+30611+30608+9447+43179+10090+10116+9986+9978+9371+9785+9615+9685+9913+9417+40233+42254+9365':'TTAAAAATATAAGTATGTCCCATGCAATATTTGGGATATACTTATACTAAAA','9258+37347+9544+9534+9555+61853+9601+9593+9606+9483+9523+30611+30608+9447+43179+10090+10116+9986+9978+9371+9785+9615+9685+9913+9417+40233+42254+9365':'TTAAAAAGATAAGTATGTCCCATACCATGTTTGGGATATACATATACTAAAA','9365':'TTTTTAGTATAAGTATGTCTCATGTAGTATTTGAGATATACTTGCACTAAAA','42254':'ATACTTGTATAAGTATGTCCCATGCAATATCTGGGACATACTTATACTAACA','40233':'TTTTGAGTATAATTATGTCCCACGAAGCATTTGAGAGATATTTATTCTAAAA','9417':'TTTTAAGTATAATGATGTCCCACGAAGCGTTTGAGATATATTTATACTAAAG'}
    
    #for key in rna_list.iterkeys():
    #	print "key: ",key," value: ","\n"
    #print rna_list.keys(0)

    benchmarks = do_benchmarks_MP(rna_list, concensus,nb_processes)
    #benchmarks = dummy_benchmarks(rna_list, metrics_list)
    print 'benchmark done after: ', time.time() -start_time, 'seconds'
    #Now that we have all the info, we want to create a list of
    node_names = benchmarks.keys()
    #node_names = [x.split('+')[0] for x in rna_list.keys()]
    root = Fct.find_root(rna_list.keys())
    #print 'ROOT..........'
    #print root
    paths = Fct.paths_node_leaves(root, rna_list.keys())
    print 'PATHS..........'
    print paths
    one_path = Fct.rank_nodes(paths)
    print one_path

    #Since we are lazy, lets do a latex file
    list_tex = [LaTeX.standard_header()]
    for metric in metrics_list:
        #plot_benchmarks_MP(benchmarks, paths, metric, nb_processes)
        plot_one_path_benchmarks(one_path, benchmarks, metric)

        #We add a section for this metric, and we will
        #do 3x2 figures per page.
        list_tex.append("\\newpage\\section{%s}" % 
                        metric.replace('_', r'\_'))
        #Now we want a list of the names of the figures of the metric
        metric_figs_names = [x for x in os.listdir('.') if 
                            x.endswith('%s.png' % metric)]
        list_tex.append(LaTeX.figure_env(metric_figs_names))
    print "Graphs done after: ", time.time() - start_time, 'seconds'
    list_tex.append('\\end{document}')
    with open('%s.tex' % output_name, 'w') as latex_file:
        latex_file.write("\n".join(list_tex))
    print 'building TeX file'
    LaTeX.pdf_build(output_name)
    os.system('rm *.png')
    print "total time is: ", time.time()-start_time, 'seconds'

