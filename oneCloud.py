__author__ = 'mariosky'


import onemax
import cloud, time

start = time.time()
print "Se inicializa la población"
cloud.call(onemax.initialize,300 ,_type='s1', _env="deap")

print "Empieza la Evolución"
jids = cloud.map(onemax.work, [5,5,5,5,5,5,5,5,5,5] , _type='s1' )
results_list = cloud.result(jids)

print results_list, time.time()-start

