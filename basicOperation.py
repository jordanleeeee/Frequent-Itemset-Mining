def loadDatabase(path):
    database = open(path, 'r')
    data = list()
    line = database.readline()
    while line != "":
        dataSet = list(map(int, line.split()))
        data.append(dataSet)
        line = database.readline()
    return data


def findInRecord(itemset, record):
    for i in itemset:
        if i not in record:
            return False
    return True


def count(itemset, data):
    counter = 0
    for record in data:
        if findInRecord(itemset, record):
            counter += 1
    return counter
