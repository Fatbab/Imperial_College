## Given a list of lastnames, we get corresponding ethnicities based on values from pickle file: D4name_ethnicity.pkl

import jellyfish
import pickle

## Load pickle file
pkl_file = open('/PATH/TO/D4name_ethnicity.pkl','rb')
D4name_ethnicity=pickle.load(pkl_file)
pkl_file.close()

## Create a dictionary with key: metaphonic version of lastnames from D4name_ethnicity and value: ethnicity.
D4name_ethnicity_meta ={}    
for k in D4name_ethnicity.keys():    
    D4name_ethnicity_meta[jellyfish.metaphone(unicode(k))]= D4name_ethnicity[k]    

## Matches metaphonic version of items from input_list to the dictionary we have from previous step.   
## Returns a list of corresponding ethnicites, where unmatched items are marked 'other'.
def get_ethnicity_list(input_list):
    output_list =[]
    for i in input_list:
        temp = jellyfish.metaphone(unicode(i))
        if D4name_ethnicity_meta.has_key(temp):
            output_list.append(D4name_ethnicity_meta[temp])
        else:
            output_list.append('other')

    return output_list
