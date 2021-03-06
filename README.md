# Workforce Analytics Assignment   
(Imperial College London - Business School - Feb 2016)   

#### Task1: What is the relationship between the number of times inventors collaborate and project performance? (colab-perf.py)
#### Task2: What is the relationship between the ethnic composition of a firm and the likelihood that an inventor will move to that firm? (move-ethni.py) 

## Dataset:   
D1: Firm Profiles (too large and has not been directly used so is not uploaded)    
D2: Firm Level Data   
D3: Patent Data    
D4: Surnames and Ethnicities reference file    

## Notes:    
1. Herfindahl index is a measure for diversity of sets.  Let 1-Herfindahl be h-index.    
2. Every team is assigned an h-index based on members ethnicities. Ethinicity is implied from metaphonic version of team members' last names.    
3. Data obtained here is later imported to R for Possion regression. Since we have count data, Poisson is the suitable model.

## New Coding Tips:    
1. Sort dictionary by key in python. (key, value)    
2. Collapse a list of lists into one list.    
3. Use of tuple.    
4. Use of Counter.    
5. Use of jellyfish.metaphone.    
