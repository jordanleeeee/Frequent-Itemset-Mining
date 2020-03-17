from basicOperation import loadDatabase
import time
from apriori import aprioriAlgorithm

data = loadDatabase('a1dataset.txt')
start = time.time()
minsup = 400
freq_itemsets = aprioriAlgorithm(data, minsup)
print(freq_itemsets)
print(len(freq_itemsets))
duration = time.time() - start
print(duration)