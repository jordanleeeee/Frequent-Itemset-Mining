import aprioriFromExternalLib
import basicOperation


def isImmediateSuperSet(smallSet, largeSet):
    if largeSet.issuperset(smallSet):
        if len(largeSet) - len(smallSet) == 1:
            return True
    return False


data = basicOperation.loadDatabase('a1dataset.txt')
minsup = 400
# get frequent Itemset from external library
freqItemSet = aprioriFromExternalLib.getFreqItemSet(data, minsup)
print("freq item set are")
print(freqItemSet)

# count the occurenct of each freq item
dataWithFreq = dict()
for itemSet in freqItemSet:
    dataWithFreq[tuple(itemSet)] = basicOperation.count(itemSet, data)

print("\ndata with freq")
print(dataWithFreq)

# find closed and max itemset
closedItemSet = list()
maxItemSet = list()
for x, y in dataWithFreq.items():
    targetSet = set(x)
    freq = y
    isClosedFreqItemSet = True
    isMaxSet = True
    for p, q in dataWithFreq.items():
        comparingSet = set(p)
        comparingfreq = q
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

print("\nmaxSet is")
print(maxItemSet)