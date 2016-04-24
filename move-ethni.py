## What is the relationship between the ethnic composition of a firm and 
## the likelihood that an inventor will move to that firm? 

import codecs
import os.path
import csv
import nltk
import timeit
import numpy as np

import itertools

import operator # to sort dictionaty by value
from collections import OrderedDict # to sort dictionaty by value
from collections import Counter

#pnum= []
firm= []
year= []
#perf= []
#invnum_column= []
lastname= []
#cntries= []

with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/Data/D3 patent_data.csv', 'rb') as f:
    next(f) # skip header line
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        #pnum.append(row[0])
        firm.append(row[1])
        year.append(row[2])
        #perf.append(row[3])
        #invnum_column.append(row[4])
        lastname.append(row[5])
        #cntries.append(row[6])

## put all inventors in firm-year baskets
from collections import defaultdict
firm_inv = defaultdict(list)
for i in range (len(lastname)):
    #print invnum_column[i]
    firm_inv[firm[i]+"-"+year[i]].append(lastname[i].split(";"))
    
## order the dict by key, to preserve chronological order of firm inventor size
import collections 
ordered_firm_inv = collections.OrderedDict(sorted(firm_inv.items()))

## to collaps multiple inventor lists into one for every firm-year key
firm_yr_inv = dict((key, []) for key in ordered_firm_inv.keys())
for k in ordered_firm_inv.keys():
    firm_yr_inv[k]=list(set(itertools.chain.from_iterable(ordered_firm_inv[k]))) 

## new dict with key: firm and value: chronical list of inventors
firm_ord_inv =defaultdict(list)
for k in firm_yr_inv.keys():
    firm_ord_inv[k[:-5]].append(firm_yr_inv[k])    

## new dict with key: firm and value: chronically ordered list of #additional inventors 
firm_turnover = defaultdict(list)

## new dict with key: firm, value: list of h-index for every gone year
firm_herf = defaultdict(list)

from herfindahl import herfindahl

for k in firm_ord_inv.keys():
    if len(firm_ord_inv[k])==1:
        firm_turnover[k].append(0)
        firm_herf[k].append(0)
    else:     
        for i in range(1, len(firm_ord_inv[k])):
            temp = len(set(firm_ord_inv[k][i]) - set(firm_ord_inv[k][i-1]))  
            firm_turnover[k].append(temp)
            firm_herf[k].append( round(1-herfindahl(firm_ord_inv[k][i-1]),4) )
    
####### 
## now we compute herfindahl for the composition of the firm at each year
## so when 118 new inventors joined XLN in year1, what the h-index been in year0


## get R&D budget data from  "D2 firm_level_data.csv" file
firm_rd = defaultdict(float)
import csv
with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/Data/D2 firm_level_data.csv', 'rb') as f:
    next(f) # skip header line
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        firm_rd[row[0]]=row[3]


## write firm, turnover, h-index, R&D budget
with open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/IndividualAssignment/Q1-a/csv-created/turnover_herf.csv','wb') as f:
    writer = csv.writer(f)
    header = 'firm', 'budget', 'turnover', 'hindex'
    writer.writerow(header)
    for k in firm_turnover.keys():       
        col_firm = k
        col_rd = firm_rd[k]
        for i in range(len(firm_turnover[k])):
            col_turnover= firm_turnover[k][i]
            col_hindex=  firm_herf[k][i]
            temp_row = col_firm, col_rd, col_turnover, col_hindex
            writer.writerow(temp_row)
