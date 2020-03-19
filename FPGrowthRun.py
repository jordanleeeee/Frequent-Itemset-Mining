from basicOperation import loadDatabase
# import time


# the tree node of FP tree
class TreeNode:
    def __init__(self, key, parentNode):
        self.key = key  # item
        self.value = 1  # frequency (default is 1)
        self.childNode = dict()
        self.parentNode = parentNode
        self.linkage = None  # linked to another node with same key

    def freqIncrease(self):
        self.value += 1


# get list of frequent item( length ), the list is sorted base on frequency
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


def getOrderedFrequentItems(data, freqItem):
    table = list()
    for item in data:
        oneDataSet = list()
        for i in freqItem:
            if i in item:
                oneDataSet.append(i)
        table.append(oneDataSet)
    return table


def updateLinkage(headOfLinkedList, newNode):
    while headOfLinkedList.linkage is not None:
        headOfLinkedList = headOfLinkedList.linkage
    headOfLinkedList.linkage = newNode


# update the FP tree
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


# build the FP tree, and return the HeadLinkTabls as well as the root of the tree
def buildTree(itemTable, freqItem):
    # construct the node link table
    headLinkTable = dict()
    for i in freqItem:  # initialize node link table
        headLinkTable[i] = None

    # create tree
    treeRoot = TreeNode("NULL", None)
    # update the tree
    for itemset in itemTable:
        updateTree(itemset, treeRoot, headLinkTable)
    # treeRoot.printTree()
    return headLinkTable, treeRoot


'''
store all mined frequent in the freq_itemsets
data is all the transction, posPattern is previous pattern, when first call posPattern is None
freq_itemsets is a set that will store all mined frequent item
'''
def FPGrowth(data, minsup, posPattern, freq_itemsets):
    freqItem = getFrequentItem(data, minsup)
    filteredSortedItemTable = getOrderedFrequentItems(data, freqItem)
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
# start = time.time()
minsup = 400
freq_itemsets = set()
FPGrowth(data, minsup, None, freq_itemsets)
print("result is")
result = list()
for items in freq_itemsets:
    result.append(list(items))
print(result)
print(len(result))
#
# duration = time.time() - start
# print(duration)
