## Herfindahl Code
## my code
'''
def herfindahl(diversity_list):
    diversity_list.sort()
    #n = len(diversity_list)
    similarity_list=[]
    similarity_dict={}
    while (diversity_list):
        personality = diversity_list[0]
        k=1
        for j in range (1, len(diversity_list)):
            if diversity_list[j] == personality:
                k= k+1
            else:
                diversity_list.remove(personality)        
                break 
                
        similarity_list.append(k)
        similarity_dict[personality] =k
    
    
    for i in range
    
    
    return (similarity_list, similarity_dict)
'''

## Class Code
from collections import Counter
def herfindahl(input_list):
    cntry_cnt = Counter(input_list)
    vals = cntry_cnt.values()
    prob=0
    for val in vals:
        prob= prob+(val/float(sum(vals)))**2
    return prob