from random import randint
from utils import *


def genetic_search(problem, ngen=1000, pmut=0.1, n=20):
    """Call genetic_algorithm on the appropriate parts of a problem.
    This requires the problem to have states that can mate and mutate,
    plus a value method that scores states."""

    # NOTE: This is not tested and might not work.
    # TODO: Use this function to make Problems work with genetic_algorithm.
    # TODO: auto generate problem states, n is the amount in the list
    # TODO:rewrite h function to emphasize the maximum, works the opposite 
    # TODO: scale ngen and pmut for each different queens problem
    NSize = problem.N
    gene_pool = range(NSize)
    
    #get population 
    population = init_population(n, gene_pool, NSize)

    #get fitness function
    # fitness_fn = eval_func(NSize, population[0])
    # print(fitness_fn)

    #get f_thres
    f_thres = NSize * (NSize-1)
    
    return genetic_algorithm(population, fitness_fn, gene_pool, f_thres, ngen, pmut, NSize)

def genetic_algorithm(population, fitness_fn, gene_pool, f_thres, ngen, pmut, NSize):
    """[Figure 4.8]"""
    for i in range(ngen):
        population = [mutate(recombine(*select(2, population, fitness_fn)), gene_pool, pmut)
                      for i in range(len(population))]

        fittest_individual = fitness_threshold(fitness_fn, f_thres, population)
        if fittest_individual:
            return fittest_individual

    return max(population, key=fitness_fn)


def fitness_threshold(fitness_fn, f_thres, population):
    if not f_thres:
        return None

    fittest_individual = max(population, key=fitness_fn)
    if fitness_fn(fittest_individual) >= f_thres:
        return fittest_individual

    return None


def init_population(pop_number, gene_pool, state_length):
    """Initializes population for genetic algorithm
    pop_number  :  Number of individuals in population
    gene_pool   :  List of possible values for individuals
    state_length:  The length of each individual"""
    g = len(gene_pool)
    population = []
    for i in range(pop_number):
        new_individual = [gene_pool[random.randrange(0, g)] for j in range(state_length)]
        population.append(new_individual)

    return population


def select(r, population, fitness_fn):
    fitnesses = map(fitness_fn, population)
    sampler = weighted_sampler(population, fitnesses)
    return [sampler() for i in range(r)]


def recombine(x, y):
    n = len(x)
    c = random.randrange(0, n)
    return x[:c] + y[c:]


def recombine_uniform(x, y):
    n = len(x)
    result = [0] * n
    indexes = random.sample(range(n), n)
    for i in range(n):
        ix = indexes[i]
        result[ix] = x[ix] if i < n / 2 else y[ix]

    return ''.join(str(r) for r in result)


def mutate(x, gene_pool, pmut):
    if random.uniform(0, 1) >= pmut:
        return x

    n = len(x)
    g = len(gene_pool)
    c = random.randrange(0, n)
    r = random.randrange(0, g)

    new_gene = gene_pool[r]
    return x[:c] + [new_gene] + x[c + 1:]

def fitness_fn(candidate):
    num_conflicts = 0
    maxFitness = len(candidate) * (len(candidate)-1)
    for (r1, c1) in enumerate(candidate):
        for (r2, c2) in enumerate(candidate):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflicts(r1, c1, r2, c2)
    return maxFitness - num_conflicts

def conflicts(row1, col1, row2, col2):
    return (row1 == row2 or col1 == col2 or row1-col1 == row2 - col2 or row1 + col1 == row2 + col2)