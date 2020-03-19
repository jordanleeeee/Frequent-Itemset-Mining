# Frequent Itemset Mining

##### Here provide three ways of do frequent Itemset Mining

First one is Apriori algorithm (in aprioriRun.py),
The concept of Apriori algorithm are as follows:

```
Let k=1
Generate frequent itemsets of length 1
Repeat until no new frequent itemsets are identified
    step1: Generate length (k+1) candidate itemsets from length k frequent itemsets
    step2: Prune candidate itemsets containing subsets of length k that are infrequent
    step3: Count the support of each candidate by scanning the DB
            and eliminate candidates that are infrequent, leaving only those that are frequent
```

Apriori algorithm is not very efficient. In step3 have to scan the whole database many time
its running time growth exponentially with size of transaction.
<br/>

Second way is Apriori algorithm with use of hash tree(in hashTreeRun.py),
the algorithm is same as the first one except the step3. Doing counting the
support of each candidate by storing each candidate in a hashTree structure and scan the 
database once. This method is much faster
</br>

Third way is FP growth(FPGrowthRun.py). This is a tree based algorithm 
and is also a efficient way to do the job, its running time growth just linearly with size of transaction.
The concept of FP growth algorithm are as follows:
```
Step1: Deduce the ordered frequent items. For items with the same frequency, the order is given by the alphabetical order.
Step2: Construct the FP-tree from the above data
Step3: From the FP-tree above, construct the FP-conditional tree for each item (or itemset).
Step4: Determine the frequent patterns.
```


#### Here also provide program to mine max and closed frequent itemset (closeAndMaxSetMining.py)
An itemset is closed if none of its immediate supersets
has the same support as the itemset.</br>

An itemset is maximal frequent if none of its immediate supersets is
frequent.</br>
