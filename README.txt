The folder 'src/' contains the python modules
The folder 'src_cpp' contains the c++ implementation of the Sankoff algo.
The folder 'data/' contains some data for the project
The folder 'doc/' contains an automatic generator of documentation for
    python with "epydoc". Just run: epydoc-2.4 --config epydoc_conf.txt 
    to generate a pdf.


The module Functions.py contains a bunch of functions on RNA that (should)
    only call standard python modules
The module ViennaRNA.py contains functions calling the ViennaRNA 1.8.5 package python API. The instructions for installations are below.
The module LaTeX.py contains functions to create a LaTeX file and build it
    using pdflatex
The module Benchmarks.py contains a bunch of function to do the benchmarks
    of different fitness functions on a tree writen in the Masoud format.
    It calls the 3 other modules and also needs matplotlib.The options are
        -f <file to read>
        -p <max number of processes to create>
        -o <name of pdf output>

##########################################################################
Install the ViennaRNA python API as follows:
   
    1- Download the ViennaRNA packages 1.8.5 from here:
        http://www.tbi.univie.ac.at/RNA/ViennaRNA-1.8.5.tar.gz
    2- Unpack it:
        >tar -xzf ViennaRNA-1.8.5.tar.gz
    3- Go inside the ViennaRNA-1.8.5 folder an compile it (no install)
        >./configure
        > make
    3- Go inside the ViennaRNA-1.8.5/Perl directory an run 'swig' for python
        >swig python RNA.i
    4- copy the script at the end  into the ViennaRNA-1.8.5/ folder and name
        it "setup.py". Then run (sudo may be needed for install):
       >python setup.py build
       >python setup.py install 
    5- open a python shell and try:
        > import RNA
        > RNA.fold('CCCCCAAAGGGGG')
    6- you can delete de ViennaRNA folder 

Now, the ViennaRNA package has a tricky API, there is a Perl documentation
at: 
    http://www.bcgsc.ca/downloads/genereg/remcbigdata/miR/ViennaRNA-1.8.5/Perl/blib/html/site/lib/RNA.html#folding_routines

Now they are a couple of tricks. In bold lower-case are the name of functions,
in bold and upper-case the possible arguments in the required order. The lower
case letters preceded by an $ are global variables for the software. Swig
places all those variables as attributes of PACKAGE.cvar . In our case,
to allow constrains we need to set $fold_constrained to 1, so if we do:
    >Import RNA
the variable can be changed as follow:
    >RNA.cvar.fold_constrained = 1


###########################################
#!/usr/bin/env python
"""
This script was writen by Ivo Hofacker, Institut für theoretische Chemie, University of Vienna, Austria.
It was copied from: biopython.org.wiki/Scriptcentral
"""
 
from distutils.core import setup, Extension
import os
import sys
 
old_filename = os.path.join("Perl", "RNA.py")
new_filename = os.path.join("Perl", "__init__.py")
if os.path.exists(old_filename):
    os.rename(old_filename, new_filename)
 
extra_link_args = []
if sys.platform != 'darwin':
    extra_link_args.append('-s')
 
extension = Extension("_RNA",
                      ["Perl/RNA_wrap.c"],
                      libraries=['RNA'],
                      library_dirs=['lib'],
                      extra_link_args=extra_link_args
                      )
 
setup(name="RNA",
      version="1.8.5",
      description="Vienna RNA",
      author="Ivo Hofacker, Institute for Theoretical Chemistry, University of Vienna",
      url="http://www.tbi.univie.ac.at/RNA/",
      package_dir = {'RNA':'Perl'},
      packages = ['RNA'],
      ext_modules=[extension],
      )
