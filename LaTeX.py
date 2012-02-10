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

def figure_env(subfigures_list, width=0.43):
    environment = ['\\begin{figure}[h!]\n\t\\centering']
    for fig in subfigures_list:
        environment.append('\t\\subfloat{}\\includegraphics[width=%s\\textwidth]{%s}' % (width, fig))
    environment.append('\end{figure}')
    return '\n'.join(environment)

