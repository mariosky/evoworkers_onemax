
import random, time

from deap import base
from deap import creator
from deap import tools

import jsonrpclib
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

CHROMOSOME_LENGTH = 100
IND_PB    = 0.05
TOURNAMENT_SIZE = 3
SAMPLE_SIZE = 60
POPULATION_SIZE = 400

SERVER = "http://evening-beyond-6989.herokuapp.com/evospace"
#SERVER = "http://localhost:5000/evospace"

def getToolBox():
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, CHROMOSOME_LENGTH)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register("evaluate", evalOneMax)
    toolbox.register("mate", tools.cxTwoPoints)
    toolbox.register("mutate", tools.mutFlipBit, indpb = IND_PB)
    toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)
    return toolbox





def initialize(n):
    pop = getToolBox().population(n=POPULATION_SIZE)
    server = jsonrpclib.Server(SERVER)
    server.initialize(None)
    for cs in pop:
        chrome = cs[:]
        individual = {'id':None,'fitness':{"DefaultContext":0.0 },'chromosome':chrome}
        server.putIndividual(individual)


def evalOneMax(individual):
    return sum(individual),


def evolve(i, CXPB = 0.5, MUTPB = 0.2, NGEN = 90  ):
    toolbox = getToolBox()
    random.seed(64)
    server = jsonrpclib.Server(SERVER)
    evospace_sample = server.getSample(SAMPLE_SIZE)
    pop = [ creator.Individual( cs['chromosome']) for cs in evospace_sample['sample']]

    out = []


    out.append( "Start of evolution %i" % i)

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    out.append( "  Evaluated %i individuals" % len(pop))

    # Begin the evolution

    for g in range(NGEN):
        #print "-- Generation %i --" % g,

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        #print "  Evaluated %i individuals" % len(invalid_ind),

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        out.append( "  Min %s" % min(fits) + "  Max %s" % max(fits)+ "  Avg %s" % mean + "  Std %s" % std)

    #print "-- End of (successful) evolution --"

    sample = [ {"chromosome":ind[:],"id":None,
            "fitness":{"DefaultContext":ind.fitness.values[0]} }
                                                            for ind in pop]
    evospace_sample['sample'] = sample
    server.putSample(evospace_sample)


    best_ind = tools.selBest(pop, 1)[0]
    print "Best individual is %s, %s" % ( best_ind.fitness.values, best_ind)

    return [best_ind.fitness.values[0] == CHROMOSOME_LENGTH, best_ind.fitness.values[0],best_ind ,out]


def work(max_samples):
    results = []
    for i in range(max_samples):
        evolve(i)


if __name__ == "__main__":
    start = time.time()

    print "iniciando.."
    start = time.time()
    #initialize(300)
    print "Evol."
    print time.time()-start
    work(20)
    print time.time()-start

#    for i in range(100):
#        print i
#        if evolve(0):
#            print "Global Minimum Reached"
#            exit()

#    num_jobs = 2
#    jids = cloud.map(evolve, range(num_jobs) , _type='s1', _env="deap")
#    results_list = cloud.result(jids)
#    for r in results_list:
#        print r
#
