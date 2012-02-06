import RNA

class Fitness():
    
    def __init__(self, G, alpha, beta, fit_fct="alpha*MFE + beta*D",
                 D_scheme=None):
        """This construct an fitness object with by default a linear
        combination of the MFE and the base pair distance of a given
        MFE secondary structure with G (the goal seconday structure).
        A new fitness function can be given with the key work "fit_fct".
        It must have at most the 4 parameters, (alpha, beta, MFE, D).
        If a new scheme for computing D is desired, a function having
        as input (G,S) where G is the target seconday structure
        and S the sequence can be passed with the keyword "D_scheme".
        
        """
        self.G = G
        self.alpha = alpha
        self.beta = beta
        self.fit_fct = fit_fct
        self.D_scheme = D_scheme
        
        
    def fitness(self, S):
        """This function evaluates the fitness of a given RNA sequence,
        in function of the parameters when the object was built. 
        If the error is done when evaluating the fitness function,
        the error will be printed but None will be returned. Else,
        the output is the result of the fitness function.
        """
        
        secondary_structure, MFE = RNA.fold(S)
        if not self.D_scheme: #Here we compute the usual bp_distance
            D = RNA.bp_distance(self.G, secondary_structure)
        else:   #And here we apply some custom scheme
            D = self.D_scheme(self.G, secondary_structure)
        
        #So we can evaluate the function
        alpha = self.alpha
        beta = self.beta
        try:
            return eval(self.fit_fct) #We just dumbly evaluate the fit.
        except (SyntaxError, ValueError, ZeroDivisionError) as err:
            print """The fitness function can't be evaluated with the
            actual parameters. The error is:
                <<%s>>
            Here are the culprits:
            fitness function : %s
            MFE : %s
            D : %s
            alpha : %s
            beta : %s
            """ % (err, self.fit_fct, MFE, D, alpha, beta)
            return None

if __name__ == "__main__":
    S = 'GAUCCCGAUCGAUC'
    G = '(((...))..)...'
    
    my_fitness = Fitness(G, 1, 1)
    print my_fitness.fitness(S)
    
    my_funky_fitness=Fitness(G,3.4,3,'beta*MFE**(D/alpha)')
    print my_funky_fitness.fitness(S)
    
    def funky_dis(G, S):
        return len(S) + len(G)
    
    even_funkier = Fitness(G, 0.5, 4, "alpha*MFE + beta*D", funky_dis)
    print "this is absurd", even_funkier.fitness(S)
    