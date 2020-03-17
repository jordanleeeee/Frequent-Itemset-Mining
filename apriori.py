from basicOperation import count
import time


def merge(itemset1, itemset2):
    newFreqItem = set(itemset1).union(set(itemset2))
    if len(newFreqItem) == (len(itemset1)+1):
        return newFreqItem


# generate candidates of size (k+1) by merging two frequent itemsets of size k
def generateCandidates(old_candidates):
    new_candidates = set()
    for i in range(len(old_candidates)):
        for j in range(i + 1, len(old_candidates)):
            newItemset = merge(old_candidates[i], old_candidates[j])
            # if merge is success
            if newItemset is not None:
                new_candidates.add(tuple(sorted(tuple(newItemset))))
    result = list()
    for i in new_candidates:
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
def prune(candidates, old_candidates):
    after_prune = list()
    for itemset in candidates:
        if isFrequentSubset(itemset, old_candidates):
            after_prune.append(itemset)
    return after_prune


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
    #     generate frequent itemsets of size 1
    Lk = length_1_freqItemSet(data, minsup)
    freq_itemsets = list(Lk)
    # length = 1
    while len(Lk) > 0:
        # length += 1
        start = time.time()
        nextLk = generateCandidates(Lk)
        nextLk = prune(nextLk, Lk)
        # print(len(Cknext))
        Lk = list()
        for itemSet in nextLk:
            if count(itemSet, data) >= minsup:
                Lk.append(itemSet)
                freq_itemsets.append(itemSet)
        # print(str(length) + ": " + str(time.time() - start))
    return freq_itemsets
