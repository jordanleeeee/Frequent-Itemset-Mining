from basicOperation import findInRecord


class TreeNode:
    def __init__(self, hashKey, level, bucketSize):
        self.subNode = list()
        for i in range(hashKey):
            self.subNode.append(None)
        self.hashKey = hashKey
        self.bucketSize = bucketSize
        self.level = level

    # store all frequent item set in freqItemSet
    def getFreqItemSet(self, freqItemSet, minsup):
        for node in self.subNode:
            if isinstance(node, TreeNode):
                node.getFreqItemSet(freqItemSet, minsup)
            elif node is None:
                continue
            else:
                for x, y in node.items():
                    if y >= minsup:
                        freqItemSet.append(list(x))

    def __update(self, transaction, partialTransaction):
        record = list()
        for i in range(len(partialTransaction)):
            targetingIndex = partialTransaction[i] % self.hashKey
            # if not yet go though the sub node yet, go though it
            if targetingIndex not in record:
                record.append(targetingIndex)
                node = self.subNode[targetingIndex]
                if isinstance(node, TreeNode):
                    node.__update(transaction, partialTransaction[i+1::])
                elif node is None:
                    continue
                # reached a leaf, do comparison to every item set in the leaf
                else:
                    for x, y in node.items():
                        if findInRecord(x, transaction):
                            node[x] += 1

    def updateFreqOfLeaf(self, transaction):
        self.__update(transaction, transaction)

    def addChildren(self, newList):
        target = newList[self.level] % self.hashKey
        if isinstance(self.subNode[target], TreeNode):
            self.subNode[target].addChildren(newList)
        else:
            if self.subNode[target] is None:
                self.subNode[target] = dict()
            # when bucket is full
            if len(self.subNode[target]) == self.bucketSize:
                # cannot split anymore, just simple add it to the leaf
                if self.level + 1 == len(newList):
                    self.subNode[target][tuple(newList)] = 0
                # can split the tree, then split it, add it to the node
                else:
                    temp = self.subNode[target].copy()
                    self.subNode[target] = TreeNode(self.hashKey, self.level + 1, self.bucketSize)
                    for i in temp:
                        self.subNode[target].addChildren(i)
                    self.subNode[target].addChildren(newList)
            # when bucket is not full
            else:
                self.subNode[target][tuple(newList)] = 0
