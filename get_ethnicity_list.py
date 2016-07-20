import jellyfish
import pickle


pkl_file = open('/Users/fatemeh/Documents/Imperial/SpringBlock1/WorkforceAnalytics/Lecture4/Code/inClass/D4name_ethnicity.pkl','rb')
D4name_ethnicity=pickle.load(pkl_file)
pkl_file.close()

D4name_ethnicity_meta ={}
for k in D4name_ethnicity.keys():
    D4name_ethnicity_meta[jellyfish.metaphone(unicode(k))]= D4name_ethnicity[k]


'''
def get_ethnicity_list(input_list):
    output_dict={} #dict((k,'') for k in input_list)
    for k in input_list:
        temp_lastname =jellyfish.metaphone(unicode(k))
        if D4name_ethnicity_meta.has_key(temp_lastname):
            output_dict[k]= D4name_ethnicity_meta[temp_lastname]
        else:
            output_dict[k]= 'other'

    return output_dict
'''

def get_ethnicity_list(input_list):
    output_list =[]
    for i in input_list:
        temp = jellyfish.metaphone(unicode(i))
        if D4name_ethnicity_meta.has_key(temp):
            output_list.append(D4name_ethnicity_meta[temp])
        else:
            output_list.append('other')

    return output_list
