from basicOperation import loadDatabase


def equal(itemset1, itemset2):
    for i in range(len(itemset1)):
        if itemset1[i] != itemset2[i]:
            return False
    return True


def check(itemset1, itemset2):
    for i in range(len(itemset1) - 1):
        if itemset1[i] != itemset2[i]:
            return False
    return True


# check whether an itemset appear in a record or not
def find_in_record(itemset, record):
    for i in itemset:
        if i not in record:
            return False
    return True


# merging two itemsets, keeping the new itemset sorted
def generate_candidate(itemset1, itemset2):
    newitemset = list()
    for i in range(len(itemset1) - 1):
        newitemset.append(itemset1[i])
    if (itemset1[-1] < itemset2[-1]):
        newitemset.append(itemset1[-1])
        newitemset.append(itemset2[-1])
        return newitemset
    else:
        newitemset.append(itemset2[-1])
        newitemset.append(itemset1[-1])
        return newitemset


# generate candidates of size (k+1) by merging two frequent itemsets of size k
def generate_candidates(old_candidates):
    new_candidates = list()
    for i in range(len(old_candidates)):
        for j in range(i + 1, len(old_candidates)):
            if check(old_candidates[i], old_candidates[j]):
                newitemset = generate_candidate(old_candidates[i], old_candidates[j])
                #                 print(newitemset)
                new_candidates.append(newitemset)
    return new_candidates


# check whether a itemset has infrequent subsets
def check_subset(itemset, old_candidates):
    for i in range(len(itemset)):
        subset = [itemset[j] for j in range(len(itemset))]
        del subset[i]
        find = False
        for A in old_candidates:
            if (equal(subset, A)):
                find = True
                break
        if find == False:
            return False
    return True


# prune candidates whick has infrequent subsets
def prune(candidates, old_candidates):
    after_prune = list()
    for itemset in candidates:
        if check_subset(itemset, old_candidates):
            after_prune.append(itemset)
    return after_prune


# count the support of an itemset
def count(itemset, data):
    counter = 0
    for record in data:
        if find_in_record(itemset, record):
            counter = counter + 1
    return counter


# generate the frequent items
def generate_item(data, minsup):
    items = {}
    for record in data:
        for i in record:
            if i in items:
                items[i] = items[i] + 1
            else:
                items[i] = 1
    freq_items = list()
    for item in items:
        if items[item] >= minsup:
            freq_items.append([item])
    return freq_items


def apriori(data, minsup):
    #     generate frequent itemsets of size 1
    Lk = generate_item(data, minsup)
    freq_itemsets = [i for i in Lk]
    while (len(Lk) > 0):
        #         generate candidate itemsets of size (k+1) based on the frequent itemsets of size k
        Cknext = generate_candidates(Lk)
        #         prune candidate itemsets of size (k+1) which has infrequent subsets according to step 2
        Cknext = prune(Cknext, Lk)
        Lk = list()
        for itemset in Cknext:
            #             count the support of candidate itemsets by scanning the dataset, and eliminate the infrequent ones
            if count(itemset, data) >= minsup:
                Lk.append(itemset)
                freq_itemsets.append(itemset)
    return freq_itemsets

data = loadDatabase('a1dataset.txt')
freqItem = apriori(data, 400)
print(freqItem)
print(len(freqItem))