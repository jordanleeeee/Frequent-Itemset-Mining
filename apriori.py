from basicOperation import count
# import time


# merge two itemset (if possible)
def merge(itemset1, itemset2):
    newFreqItem = set(itemset1).union(set(itemset2))
    if len(newFreqItem) == (len(itemset1)+1):
        return newFreqItem


# generate candidates of length (k+1) by merging two frequent itemsets of length k
def generateCandidates(oldCandidates):
    newCandidates = set()
    for i in range(len(oldCandidates)):
        for j in range(i + 1, len(oldCandidates)):
            newItemset = merge(oldCandidates[i], oldCandidates[j])
            # if merge is success, add it to newCandidate set
            if newItemset is not None:
                newCandidates.add(tuple(sorted(tuple(newItemset))))
    # conver the set to a list
    result = list()
    for i in newCandidates:
        result.append(sorted(i))
    return sorted(result)


# check whether a itemset has infrequent subsets
def isFrequentSubset(itemset, old_candidates):
    for i in range(len(itemset)):
        subset = list(itemset)
        del subset[i]
        if subset not in old_candidates:
            return False
    return True


# prune candidates which has infrequent subsets
def prune(candidates, oldCandidates):
    afterPrune = list()
    for itemset in candidates:
        if isFrequentSubset(itemset, oldCandidates):
            afterPrune.append(itemset)
    return afterPrune


# generate the frequent items of length 1
def length_1_freqItemSet(data, minsup):
    items = dict()
    for record in data:
        for i in record:
            if i in items:
                items[i] += 1
            else:
                items[i] = 1

    freq_items = list()
    for item in items:
        if items[item] >= minsup:
            freq_items.append([item])
    return sorted(freq_items)


def aprioriAlgorithm(data, minsup):
    #  generate frequent itemsets of size 1
    Lk = length_1_freqItemSet(data, minsup)
    freq_itemsets = list(Lk)
    while len(Lk) > 0:
        # length K+1 candidates
        nextLk = generateCandidates(Lk)
        # remove infrequent candidates
        nextLk = prune(nextLk, Lk)
        # count and kick away infrequent candidate
        Lk = list()
        for itemSet in nextLk:
            if count(itemSet, data) >= minsup:
                Lk.append(itemSet)
                freq_itemsets.append(itemSet)
    return freq_itemsets
