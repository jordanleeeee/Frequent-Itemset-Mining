import apriori as ap
import treeNode
from basicOperation import loadDatabase
import time


def aprioriAlgorithmWithHashing(data, minsup):
    # same algorithm as apriori
    Lk = ap.length_1_freqItemSet(data, minsup)
    freq_itemsets = list(Lk)
    length = 1
    while len(Lk) > 0:
        length += 1
        start = time.time()
        nextLk = ap.generateCandidates(Lk)
        nextLk = ap.prune(nextLk, Lk)

        # use hashing to count and eliminate candidate instead
        Lk = list()
        hashTreeRoot = treeNode.TreeNode(800, 0, 20)
        print(len(nextLk))
        for itemSet in nextLk:
            hashTreeRoot.addChildren(itemSet)
        if len(nextLk) > 0:
            for itemSet in data:
                hashTreeRoot.updateFreqOfLeaf(itemSet)
            smallFreqItemSet = list()
            hashTreeRoot.getFreqItemSet(smallFreqItemSet, minsup)
            if smallFreqItemSet is not None:
                for item in smallFreqItemSet:
                    Lk.append(item)
                    freq_itemsets.append(item)
        print(str(length) + ": " + str(time.time() - start))
    return freq_itemsets


data = loadDatabase('a1dataset.txt')
start = time.time()
minsup = 400
freq_itemsets = aprioriAlgorithmWithHashing(data, minsup)
print("result is")
print(freq_itemsets)
print(len(freq_itemsets))
duration = time.time() - start
print(duration)
