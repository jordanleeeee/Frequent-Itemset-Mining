from basicOperation import loadDatabase
from apriori import aprioriAlgorithm

# please refer to apriori.py for the implementation
data = loadDatabase('a1dataset.txt')
minsup = 400
freq_itemsets = aprioriAlgorithm(data, minsup)
print(freq_itemsets)
print(len(freq_itemsets))
