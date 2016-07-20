## Workforce Analytics
## Task 1: What is the relationship between the number of times inventors collaborate and project performance? 


import codecs
import os.path
import csv
import nltk
import timeit
import numpy as np
import operator # to sort dictionaty by value
from collections import OrderedDict # to sort dictionaty by value
from collections import Counter
from collections import defaultdict
from get_ethnicity_list import get_ethnicity_list  # custom function
from herfindahl import herfindahl  # custom function

pnum= []
perf= []
invnum= []
lastname= []

# Read in only relevant patent data: 
# patent_number (pnum), patent_performance (perf), inventor_id (invnum), inventor_lastname (lastname)
# (In this task, we don't need to keep track of the associated firm.)
with open('/PATH/TO/PATENT DATA/D3 patent_data.csv', 'rb') as f:
    next(f) # skip header line
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        pnum.append(row[0])
        perf.append(row[3])
        invnum.append(row[4])
        lastname.append(row[5])


# create a list of pairs: (inventor_ids , patent performance)
invnum_perf=[]
for i in range (len(invnum)):
    invnum_perf.append((invnum[i], int(perf[i])))
    

## Creates list of tuples: (inventor_ids, number of times these inventors appeared together)
cnt = Counter(tuple(l) for l in invnum)
invnum_cnt= [(l, cnt[tuple(l)]) for l in invnum]


## Creates dictionary to sum up the performance of all patents filed under the same group of inventors
invnum_Tperf = defaultdict(int)
for tup in invnum_perf:
    invnum_Tperf[tup[0]] += int(tup[1])


## Creates dictionary with enteries like:  {inventor_ids: (count of collaborations, avg patent performance)}
invnum_count_avgPerf= defaultdict(int)
for k in invnum_count.keys():
    invnum_count_avgPerf[k] = (invnum_count[k], round(float(invnum_Tperf[k])/float(invnum_count[k]),4))


## Creates dictionary with key: inventor_ids and value: ethnicities from lastnames
## To use later for h-index in csv
#from get_ethnicity_list import get_ethnicity_list
invnum_ethni = defaultdict(list)
for k in range(len(invnum)):
    temp_lstnm = list(lastname[k].split(';'))
    temp_eth = get_ethnicity_list(temp_lstnm)
    invnum_ethni[invnum[k]]= temp_eth
        

## Creates dictionaty with key: inventor_ids and value: size of team
## To distinguish between single and group patents
team_size = defaultdict(int)
for k in invnum_count_avgPerf.keys():
    team_size[k] = k.count(";")+1


## Export Restults to CSV
## CSV format of: inventor_ids, number of collaborations, average patent performance
import csv
with open('/PATH/TO/WRITE/OUTCOME/invnum_count_avgPerf.csv','wb') as f:
    writer = csv.writer(f)
    header = 'invnum', 'colab', 'avgPerf'
    writer.writerow(header)
    for k in invnum_count_avgPerf.keys():
        col_count= invnum_count_avgPerf[k][0]
        col_perf=  invnum_count_avgPerf[k][1]
        temp_row = k, col_count, col_perf 
        writer.writerow(temp_row)


import csv
with open('/PATH/TO/WRITE/OUTCOME/soloInv_count_avgPerf.csv','wb') as f:
    writer = csv.writer(f)
    header = 'invnum', 'colab', 'avgPerf'
    writer.writerow(header)
    for k in invnum_count_avgPerf.keys():
        if len(k) ==10:
            col_count= invnum_count_avgPerf[k][0]
            col_perf=  invnum_count_avgPerf[k][1]
            temp_row = k, col_count, col_perf 
            writer.writerow(temp_row)


#from herfindahl import herfindahl
import csv
with open('/PATH/TO/WRITE/OUTCOME/teamInv_count_avgPerf_size_hindex.csv','wb') as f:
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
