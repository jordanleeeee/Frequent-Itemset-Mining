from basicOperation import loadDatabase
import time


# generate the frequent items of length 1
class TreeNode:
    def __init__(self, key, parentNode):
        self.key = key              # item
        self.value = 1              # frequency (default is 1)
        self.childNode = dict()
        self.parentNode = parentNode
        self.linkage = None

    def freqIncrease(self):
        self.value += 1


def getFrequentItem(data, minsup):
    dictionary = dict()
    for record in data:
        for i in record:
            if i in dictionary:
                dictionary[i] += 1
            else:
                dictionary[i] = 1

    sorted_d = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    freq_items = list()
    for item in sorted_d:
        if item[1] < minsup:
            break
        freq_items.append(item[0])
    return freq_items


def getFilteredSortedFrequentTable(data, freqItem):
    table = list()
    for item in data:
        oneDataSet = list()
        for i in freqItem:
            if i in item:
                oneDataSet.append(i)
        table.append(oneDataSet)
    return table


def updateLinkage(currentNode, targetNode):
    while currentNode.linkage is not None:
        currentNode = currentNode.linkage
    currentNode.linkage = targetNode


def updateTree(itemset, parentNode, headLinkTable):
    if len(itemset) == 0:
        return
    # add first item in the itemset to the tree
    item = itemset[0]
    # update the count of a particular child node if already have such child
    if item in parentNode.childNode:
        parentNode.childNode[item].freqIncrease()
    # if no such child
    else:
        parentNode.childNode[item] = TreeNode(item, parentNode)
        # link the node to head link table when the linkage in head link table in None
        if headLinkTable[item] is None:
            headLinkTable[item] = parentNode.childNode[item]
        # link the node to the end of the linked list of such item
        else:
            updateLinkage(headLinkTable[item], parentNode.childNode[item])
    # add next item in the itemset to the tree(if any)
    if len(itemset) - 1 > 0:
        updateTree(itemset[1::], parentNode.childNode[item], headLinkTable)


def buildTree(itemTable, freqItem):
    # construct the node link table
    headLinkTable = dict()
    for i in freqItem:  # initialize node link table
        headLinkTable[i] = None

    # create tree
    treeRoot = TreeNode("NULL", None)
    for itemset in itemTable:
        updateTree(itemset, treeRoot, headLinkTable)
    # treeRoot.printTree()
    return headLinkTable, treeRoot


def FPGrowth(data, minsup, posPattern, freq_itemsets):
    freqItem = getFrequentItem(data, minsup)
    filteredSortedItemTable = getFilteredSortedFrequentTable(data, freqItem)
    headLinkTable, treeRoot = buildTree(filteredSortedItemTable, freqItem)

    # base case of the recursion
    if len(treeRoot.childNode) == 0:
        return

    # update freq itemset
    if posPattern is not None:
        for item, freq in headLinkTable.items():
            oneItemset = list()
            oneItemset.append(item)
            for i in posPattern:
                oneItemset.append(i)
            freq_itemsets.add(tuple(sorted(oneItemset)))
    else:
        for length1Item in freqItem:
            freq_itemsets.add(tuple([length1Item]))

    # recursively call FPGrowth to mine freq pattern
    for item, relatedTreeNode in headLinkTable.items():
        newPosPattern = list()
        newPosPattern.append(item)
        if posPattern is not None:
            newPosPattern.extend(posPattern)
        newRecord = list()
        targetNode = relatedTreeNode
        while targetNode is not None:
            freq = targetNode.value
            previousNodes = list()
            parent = targetNode.parentNode
            while parent.key != "NULL":
                previousNodes.append(parent.key)
                parent = parent.parentNode
            for i in range(freq):
                newRecord.append(previousNodes)
            targetNode = targetNode.linkage
        FPGrowth(newRecord, minsup, newPosPattern, freq_itemsets)


data = loadDatabase('a1dataset.txt')
start = time.time()
minsup = 400
freq_itemsets = set()
FPGrowth(data, minsup, None, freq_itemsets)
print("result")
result = list()
for items in freq_itemsets:
    result.append(list(items))
print(result)
print(len(result))
duration = time.time() - start
print(duration)
