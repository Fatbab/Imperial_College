## Workforce Analytics
## What is the relationship between the number of times inventors 
## collaborate and project performance? 



import codecs
import os.path
import csv
import nltk
import timeit
import numpy as np

#import itertools

import operator # to sort dictionaty by value
from collections import OrderedDict # to sort dictionaty by value
from collections import Counter

pnum= []
#firm= []
#year= []
perf= []
invnum_column= []
lastname= []
#cntries= []

with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/Data/D3 patent_data.csv', 'rb') as f:
    next(f) # skip header line
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        pnum.append(row[0])
        #firm.append(row[1])
        #year.append(row[2])
        perf.append(row[3])
        invnum_column.append(row[4])
        lastname.append(row[5])
        #cntries.append(row[6])



#print invnum_column[:5]

invnum = []
for i in range (len(invnum_column)):
    #print invnum_column[i]
    #invnum.append(invnum_column[i].split(";"))
    invnum.append(invnum_column[i])

#print "invnum: %s" %invnum[:5]
#print "len: %i" %len(invnum)
#print "*************"

invnum_perf=[]
for i in range (len(invnum_column)):
    #invnum_perf.append([invnum_column[i].split(";")]+list(pref[i]))
    invnum_perf.append((invnum_column[i], int(perf[i])))
    
#print "invnum_perf: %s" %invnum_perf[:5]
#print "len: %i" %len(invnum_perf)
#print "*************"


## Creates list of lists
#cnt = Counter([tuple(l) for l in invnum])
#invnum_count= [[l] + [cnt[tuple(l)]] for l in invnum]

## Creates list of tuples
cnt = Counter(tuple(l) for l in invnum)
invnum_cnt= [(l, cnt[tuple(l)]) for l in invnum]
#print "invnum_count: %s" %invnum_count[:5]
#print "len: %i" %len(invnum_count)
#print invnum_count[0][0]
#print invnum_count[0][1]

## create dict of invnum_count
from collections import defaultdict
invnum_count = defaultdict(int)
for tup in invnum_cnt:
    invnum_count[tup[0]] +=int(tup[1])
#print "*************"
#print "invnum_count: %s" %invnum_count.items()[:5]
#print "len: %i" %len(invnum_count)


## create dict for invnum and total performance
from collections import defaultdict
invnum_Tperf = defaultdict(int)
for tup in invnum_perf:
    invnum_Tperf[tup[0]] += int(tup[1])
#print "*************"
#print "invnum_Tperf: %s" %invnum_Tperf.items()[:5]
#print "len: %i" %len(invnum_Tperf)


## create dict for (invnum, count, avgPerf)
from collections import defaultdict
invnum_count_avgPerf= defaultdict(int)
for k in invnum_count.keys():
    invnum_count_avgPerf[k] = (invnum_count[k], round(float(invnum_Tperf[k])/float(invnum_count[k]),4))
#print "*************"
#print "invnum_count_avgPerf: %s" %invnum_count_avgPerf.items()[:5]
#print "len: %i" %len(invnum_count_avgPerf)




## dictionary with key: invnum and value: lastname
## to use later for h-index in csv

from get_ethnicity_list import get_ethnicity_list
#invnum_ethni = dict((key, []) for key in invnum)
invnum_ethni = defaultdict(list)
for k in range(len(invnum)):
    temp_lstnm = list(lastname[k].split(';'))
    temp_eth = get_ethnicity_list(temp_lstnm)
    invnum_ethni[invnum[k]]= temp_eth
        

## dictionaty with key: invnum and value: size
team_size = defaultdict(int)
for k in invnum_count_avgPerf.keys():
    team_size[k] = k.count(";")+1



## export count_perf to CSV:


import csv
with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/IndividualAssignment/Q1-a/csv-created/invnum_count_avgPerf.csv','wb') as f:
    writer = csv.writer(f)
    header = 'invnum', 'colab', 'avgPerf'
    writer.writerow(header)
    for k in invnum_count_avgPerf.keys():
        col_count= invnum_count_avgPerf[k][0]
        col_perf=  invnum_count_avgPerf[k][1]
        temp_row = k, col_count, col_perf 
        writer.writerow(temp_row)


import csv
with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/IndividualAssignment/Q1-a/csv-created/soloInv_count_avgPerf.csv','wb') as f:
    writer = csv.writer(f)
    header = 'invnum', 'colab', 'avgPerf'
    writer.writerow(header)
    for k in invnum_count_avgPerf.keys():
        if len(k) ==10:
            col_count= invnum_count_avgPerf[k][0]
            col_perf=  invnum_count_avgPerf[k][1]
            temp_row = k, col_count, col_perf 
            writer.writerow(temp_row)


from herfindahl import herfindahl

import csv
with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/IndividualAssignment/Q1-a/csv-created/teamInv_count_avgPerf_size_hindex.csv','wb') as f:
    writer = csv.writer(f)
    header = 'invnum', 'colab', 'avgPerf', 'size', 'hindex'
    writer.writerow(header)
    for k in invnum_count_avgPerf.keys():
            if len(k) >10:
                col_count= invnum_count_avgPerf[k][0]
                col_perf=  invnum_count_avgPerf[k][1]
                col_size= team_size[k]
                col_hindex = round(1-herfindahl(invnum_ethni[k]),4)
                temp_row = k, col_count, col_perf, col_size, col_hindex 
                writer.writerow(temp_row)
