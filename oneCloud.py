__author__ = 'mariosky'


import onemax
import cloud, time

onemax.SAMPLE_SIZE = 30
onemax.CHROMOSOME_LENGTH = 512
onemax.POPULATION_SIZE = 400
onemax.initialize()


start = time.time()
print "Se inicializa la poblacion"
cloud.call(onemax.initialize,_type='s1', _env="deap")

print "Empieza la Evolucion"
jids = cloud.map(onemax.work, [0,1,2,3] , _type='s1' )
results_list = cloud.result(jids)

print time.time()-start

for r in  results_list:
    for a in r:
        print a


#r = onemax.work(3)
