__author__ = 'mariosky'


import random

from deap import base
from deap import creator
from deap import tools

import jsonrpclib, time


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 128)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

random.seed(64)


start = time.time()

pop = toolbox.population(n=300)
server = jsonrpclib.Server("http://evening-beyond-6989.herokuapp.com/evospace")
#server = jsonrpclib.Server("http://localhost:5000/evospace")
server.initialize(None)

for cs in pop:
    chrome = cs[:]
    individual = {'id':None,'fitness':{"DefaultContext":0.0 },'chromosome':chrome}
    server.putIndividual(individual)

run_time= time.time()-start
print run_time
