from hashTreeRun import aprioriAlgorithmWithHashing as freqItemset
import basicOperation


# check if largeSet is immediate superset of smallSet
def isImmediateSuperSet(smallSet, largeSet):
    if largeSet.issuperset(smallSet):
        if len(largeSet) - len(smallSet) == 1:
            return True
    return False


data = basicOperation.loadDatabase('a1dataset.txt')
minsup = 400
# get frequent Itemset from external library
freqItemSet = freqItemset(data, minsup)

# count the occurrence of each freq item
dataWithFreq = dict()
for itemSet in freqItemSet:
    dataWithFreq[tuple(itemSet)] = basicOperation.count(itemSet, data)

# find closed and max itemset
closedItemSet = list()
maxItemSet = list()
# go though every freqitem set, and check if it is closed of max
for x, y in dataWithFreq.items():
    targetSet = set(x)
    freq = y
    isClosedFreqItemSet = True
    isMaxSet = True
    # compare a itemSet to all other itemSet
    for p, q in dataWithFreq.items():
        comparingSet = set(p)
        comparingfreq = q
        # do not do self comparison
        if targetSet == comparingSet:
            continue
        if isImmediateSuperSet(targetSet, comparingSet):
            isMaxSet = False
            if comparingfreq == freq:
                isClosedFreqItemSet = False
                break
    if isClosedFreqItemSet:
        closedItemSet.append(list(targetSet))
    if isMaxSet:
        maxItemSet.append(list(targetSet))

print("\nclosedItemSet is")
print(closedItemSet)
print(len(closedItemSet))

print("\nmaxSet is")
print(maxItemSet)
print(len(maxItemSet))