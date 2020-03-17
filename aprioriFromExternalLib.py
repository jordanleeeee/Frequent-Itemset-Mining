from apyori import apriori
from basicOperation import loadDatabase
import time


def getFreqItemSet(data, minsup):
    transactions = data
    associationRule = apriori(transactions, min_support=minsup/len(transactions))

    result = list(associationRule)
    listRules = [list(result[i][0]) for i in range(0, len(result))]
    freq_itemsets = []
    for i in listRules:
        freq_itemsets.append(sorted(i))

    return freq_itemsets

data = loadDatabase('a1dataset.txt')
start = time.time()
minsup = 400
freqitemset = getFreqItemSet(data, minsup)
print(freqitemset)
print(len(freqitemset))
