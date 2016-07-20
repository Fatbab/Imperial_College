## Herfindahl Function: Sum(rate_i)^2 
## rate_i being the number of times item i appears in a list divided by the total number of items in the list.
## So the funstion assigns a single float number to every input list.
## The more diverse a list, the smaller the result. The more homogenous the list, the larger the result.
## For diversity measures, we take 1-herfindahl so diverse list get larger values.
## Code is from Tufool AlNuaimi's lecture notes (http://www.imperial.ac.uk/people/t.alnuaimi)

from collections import Counter

def herfindahl(input_list):
    cntry_cnt = Counter(input_list)
    vals = cntry_cnt.values()
    prob=0
    for val in vals:
        prob= prob+(val/float(sum(vals)))**2
    return prob
