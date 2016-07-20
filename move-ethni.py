## Task2: What is the relationship between the ethnic composition of a firm and the likelihood that an inventor will move to that firm? 
## Steps: 1) Collect all inventors who filed a patent for a firm, per year
##        2) Diff this list for consequtive years to identify the number of moves between firms

import codecs
import os.path
import csv
import nltk
import timeit
import numpy as np
import itertools
import operator # to sort dictionaty by value
import collections 
from collections import OrderedDict # to sort dictionaty by value
from collections import Counter
from collections import defaultdict
from herfindahl import herfindahl

firm= []
year= []
lastname= []

## Load relative values from CSV file
with open('/PATH/TO/READ/D3 patent_data.csv', 'rb') as f:
    next(f) # skip header line
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        firm.append(row[1])
        year.append(row[2])
        lastname.append(row[5])
        
## Put all inventors in firm-year baskets
## This step relies on the corss-matching of indecies in firm, year and lastname lists.
firm_inv = defaultdict(list)
for i in range (len(lastname)):
    firm_inv[firm[i]+"-"+year[i]].append(lastname[i].split(";"))
    
## Order the previous dict by key. 
## This preserve chronological order and the size will represent the changes in a firm's inventor team size per year.
ordered_firm_inv = collections.OrderedDict(sorted(firm_inv.items()))

## To collaps multiple inventor lists into one for every firm-year key
## Note the resulting dictionaty is sorted by key, as it inherits it from orderd_firm_inv.
firm_yr_inv = dict((key, []) for key in ordered_firm_inv.keys())
for k in ordered_firm_inv.keys():
    firm_yr_inv[k]=list(set(itertools.chain.from_iterable(ordered_firm_inv[k]))) 

## New dict with key: firm and value: chronical list of inventors
## k[:-5] to eliminate the "-YYYY" part from key
firm_ord_inv =defaultdict(list)
for k in firm_yr_inv.keys():
    firm_ord_inv[k[:-5]].append(firm_yr_inv[k])    

## New dict with key: firm and value: chronically ordered list of #additional inventors 
## The diff may be negative, zero or positive. Since we're only observing inventor team's size, a diff of 0 can mean:
## An equal number of ppl left and joined a team in a course of a year. This can be improved in this work.
firm_turnover = defaultdict(list)

## New dict with key: firm, value: list of h-index for every past year
## So when 118 new inventors joined XLN in year1, we know what the h-index for XLN has been in year0
firm_herf = defaultdict(list)
for k in firm_ord_inv.keys():
    if len(firm_ord_inv[k])==1:
        firm_turnover[k].append(0)
        firm_herf[k].append(0)
    else:     
        for i in range(1, len(firm_ord_inv[k])):
            temp = len(set(firm_ord_inv[k][i]) - set(firm_ord_inv[k][i-1]))  
            firm_turnover[k].append(temp)
            firm_herf[k].append( round(1-herfindahl(firm_ord_inv[k][i-1]),4) )
    

## get R&D budget data from  "D2 firm_level_data.csv" file
firm_rd = defaultdict(float)
import csv
with open('/PATH/TO/READ/D2 firm_level_data.csv', 'rb') as f:
    next(f) # skip header line
    reader = csv.reader(f,delimiter=',')
    for row in reader:
        firm_rd[row[0]]=row[3]


## Write to CSV:  firm, turnover, h-index, R&D budget
with open('/PATH/TO/WRITE/turnover_herf.csv','wb') as f:
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
