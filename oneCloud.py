__author__ = 'mariosky'


import onemax
import cloud, time
#
# start = time.time()
# print "Se inicializa la poblacion"
# cloud.call(onemax.initialize,300 ,_type='s1', _env="deap")
#
# print "Empieza la Evolucion"
# jids = cloud.map(onemax.work, [5,5,5,5,5,5,5,5,5,5] , _type='s1' )
# results_list = cloud.result(jids)
#
# print results_list, time.time()-start

onemax.CHROMOSOME_LENGTH = 20
onemax.POPULATION_SIZE = 100
onemax.initialize()

r = onemax.work(3)
for l in r:
    print r
    print l[0],l[0]-l[1],l[1]-l[2],l[2]-l[3],l[4],l[5]