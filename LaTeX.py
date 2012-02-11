"""This file contains functions helping create LaTeX files
"""
import os

def standard_header(font_size=12, doc_class='article',
                          author='evolution', title='Work'):
    """This output a normal header up "\\begin{document} \\maketitle"
    Don't forget the \\end{document}!
    """
    type = ['\\documentclass[%s]{%s}' % (str(font_size), doc_class)]
    packages = ['\\usepackage[english]{babel}',
                          '\\usepackage{graphicx}'
                          '\\usepackage{geometry}'
                          '\\geometry{letterpaper}'
                          '\\usepackage[cm]{fullpage}'
                          '\\usepackage{amssymb}'
                          '\\usepackage{amsmath}'
                          '\\usepackage{amsthm}'
                          '\\usepackage{epstopdf}'
                          '\\usepackage{inputenc}'
                          '\\usepackage{subfig}']
    title = ['\\title{%s}' % title,
             '\\author{%s}' % author]
    start_doc = ['\\begin{document}',
                 '\t\\maketitle']
    return '\n'.join(type + packages + title + start_doc)

def figure_env(subfigures_list, width=0.47):
    """Given a list of figures path,
    create a LaTeX environment figure with all the subfigure
    with width "width", by default 0.47 which is 2 per row.
    """
    environment = ['\\begin{figure}[h!]\n\t\\centering']
    for fig in subfigures_list:
        environment.append('\t\\subfloat{}\\includegraphics[width=%s\\textwidth]{%s}' % (width, fig))
    environment.append('\end{figure}')
    return '\n'.join(environment)

def make_table(table, **kwargs):
    """auto_generates a table
    """

def pdf_build(file_name, bib=None, keep_log=None):
    """Build the pdf and remove built files. If bib is not None,
    it will run the bibtex. If keep log is not None, it will leave
    the logs in the file "%s_log.tex" % file_name.
    """
    tmp = ['.aux', '.log', '.tex']
    os.system('pdflatex %s.tex >> %s_log.txt' % (file_name,file_name))
    os.system('pdflatex %s.tex >> %s_log.txt' % (file_name,file_name))
    if bib:
        os.system('bibtex %s.bib' % bib)
    for x in tmp:
        os.system('rm %s%s' % (file_name, x))
    if not keep_log:
        os.system('rm %s_log.txt' % file_name)
    return None


    
