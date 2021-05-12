from random import randint
from utils import *
from time import time

def performance(fn):
  def wrapper(*args, **kwargs):
    t1 = time()
    result = fn(*args, **kwargs)
    t2 = time()
    print(f'This function took {t2-t1} s to run')
    return result
  return wrapper


@performance
def genetic_search(problem, ngen=1000, pmut=0.1, n=20):
    """Call genetic_algorithm on the appropriate parts of a problem.
    This requires the problem to have states that can mate and mutate,
    plus a value method that scores states."""

    NSize = problem.N
    gene_pool = range(NSize)

    # get population
    population = init_population(n, gene_pool, NSize)

    # get f_thres
    f_thres = NSize * (NSize - 1)

    return genetic_algorithm(population, fitness_fn, gene_pool, f_thres, ngen, pmut)


def genetic_algorithm(population, fitness_fn, gene_pool, f_thres, ngen, pmut):
    """[Figure 4.8]"""
    iterations = 0
    for i in range(ngen):
        population = [mutate(recombine(*select(2, population, fitness_fn)), gene_pool, pmut)
                      for i in range(len(population))]
        iterations+=1
        fittest_individual = fitness_threshold(fitness_fn, f_thres, population)
        if fittest_individual:
            print(f"Number of iterations: {iterations}")
            return fittest_individual
    print(f"Hit maximum amount of generations of {ngen}")
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
    size = len(candidate)
    maxFitness = size * (size - 1)
    for (r1, c1) in enumerate(candidate):
        for (r2, c2) in enumerate(candidate):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflicts(r1, c1, r2, c2)
    return maxFitness - num_conflicts


def conflicts(row1, col1, row2, col2):
    return (row1 == row2 or col1 == col2 or row1 - col1 == row2 - col2 or row1 + col1 == row2 + col2)



