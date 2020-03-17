import apriori as ap
import treeNode
from basicOperation import loadDatabase
# import time


def aprioriAlgorithmWithHashing(data, minsup):
    # same algorithm as apriori at first
    Lk = ap.length_1_freqItemSet(data, minsup)
    freq_itemsets = list(Lk)
    while len(Lk) > 0:
        # start = time.time()
        nextLk = ap.generateCandidates(Lk)
        nextLk = ap.prune(nextLk, Lk)

        # use hashing to count and eliminate candidate instead
        Lk = list()
        # read treeNode.py for details of tree node
        hashTreeRoot = treeNode.TreeNode(800, 0, 20)
        # add all item set to the tree
        for itemSet in nextLk:
            hashTreeRoot.addChildren(itemSet)
        if len(nextLk) > 0:
            # update the frequent of each item
            for itemSet in data:
                hashTreeRoot.updateFreqOfLeaf(itemSet)
            # get frequent items
            smallFreqItemSet = list()
            hashTreeRoot.getFreqItemSet(smallFreqItemSet, minsup)
            if smallFreqItemSet is not None:
                for item in smallFreqItemSet:
                    Lk.append(item)
                    freq_itemsets.append(item)
    return freq_itemsets


data = loadDatabase('a1dataset.txt')
# start = time.time()
minsup = 400
freq_itemsets = aprioriAlgorithmWithHashing(data, minsup)
print("frequent itemset are")
print(freq_itemsets)
print(len(freq_itemsets))
# duration = time.time() - start
# print(duration)
