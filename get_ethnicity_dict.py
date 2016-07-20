import jellyfish
import pickle

## Read in the provided file
pkl_file = open('/PATH/TO/D4name_ethnicity.pkl','rb')
D4name_ethnicity=pickle.load(pkl_file)
pkl_file.close()
    
D4name_ethnicity_meta ={}
for k in D4name_ethnicity.keys():
    D4name_ethnicity_meta[jellyfish.metaphone(unicode(k))]= D4name_ethnicity[k]


def get_ethnicity_dict(input_dict):
    firm_ethnicity = dict((key, []) for key in input_dict)
    for k in input_dict.keys(): 
        for i in range (0, len(input_dict[k])):    
            temp_lastname =jellyfish.metaphone(unicode(input_dict[k][i]))
            if D4name_ethnicity_meta.has_key(temp_lastname):
                firm_ethnicity[k].append(D4name_ethnicity_meta[temp_lastname]) 
            else:
                firm_ethnicity[k].append('other')
                
    return firm_ethnicity
