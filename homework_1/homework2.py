
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from string import punctuation
from operator import itemgetter
import pandas as pd
import re
import csv
import numpy as np
import final_lib as lb
import importlib
np.set_printoptions(precision=2)
importlib.reload(lb)
#%%
# We load all the recipes
recipes=pd.read_csv("ricettecontitolo.csv",sep='\t')
# For build the final list of words (for inverted index) we remove the columns: Preptime Cooktime Recipeyield
f=open("ricette.csv","r",encoding='utf-8-sig')
ricette=[]
for row in csv.reader(f, delimiter='\t'):
    if row:
        a=[]
        a.extend(row[:3])
        a.extend(row[6:])
        ricette.append(a)
f.close() 

#%%
# Define some function that we used succesively
stop=stopwords.words('english')    
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
st = LancasterStemmer() 
#%%
# We created a list with all the aliments that contains lactose
Intol=[]
f=open("intol.txt")
for row in csv.reader(f, delimiter='\t'):
    Intol.append(row[0])
f.close()
text_i=" ".join(Intol).lower()  
# Tokenization and stemming
tokens_i=tokenizer.tokenize(text_i)            
Intol_stem=[]
for w in tokens_i:
    Intol_stem.append(st.stem(w))
Intol_stem=set(Intol_stem)
#%%
# We created a new column ILinfo that contains information about the lactose intolerance
recipes.insert(8,"ILinfo",'nan')
for i in range(recipes.shape[0]):
    print(i)
    il=True
    for il in Intol_stem:
        if il in recipes.loc[i][6]:
            il=False
            break
    if(il):
        recipes.iloc[i,8]='Lactose Intolerant'
#%%
#==============================================================================
# # We create this csv file for the application
# with open('recipesfinal.csv', 'w',encoding='utf8') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter='\t')
#     cont=0
#     for k in range(recipes.shape[0]):
#         spamwriter.writerow([recipes.iloc[k,j] for j in range(9)])
#         for i in range(1,11200,15):
#             if(cont==i):
#                 print('sono arrivato a',cont)
#         cont+=1
# csvfile.close()
#==============================================================================
#%%
# We procede by dividing the author name and the vegetarin's info from the rest of dataset (not need preprocessing)
# pos is the list of position of the remaing columns that we preprocess
pos=[0,3,4]
# Num_Ricetta is the dict that assign at every recipe one number
Num_Ricetta={}
# ListaDocs is the dict that assign at every doc (all the info about recipe in the form of a single string) one number
ListaDocs={}
for i in range(len(ricette)):
    # We print number of recipe some time
    for q in range(0,11200,200):
        if i==q:
            print('ricetta numero',q)
    #Asssign number to recipe
    Num_Ricetta[i]=ricette[i][0] 
    # Transform recipe in string in separate ways
    text_i=" ".join(list(itemgetter (*pos)(ricette[i]))).lower()
    tit_i=" ".join(ricette[i][1:3]).lower()
    # Remove punctuation's sign
    for p in punctuation:
        text_i=text_i.replace(p,' ')
        tit_i=tit_i.replace(p,' ')
    # Create list of tokens   
    tokens_i=tokenizer.tokenize(text_i)     
    # Remove stopwords
    doc_i=[i for i in tokens_i if i not in stop]
    # Futher step for cleaning words, for istance removing 1/2 3/4...   
    words_i=[]
    for word in doc_i:
        if bool(re.search(r"[^a-zA-Z0-9àåãåâûùöôòìîèéêñç]",word))!=True:
            words_i.append(word)
    # Stemming         
    stem_i=[]
    for w in words_i:  
        stem_i.append(st.stem(w))
    # We readd the author name and the vegetarin's info 
    stem_i.extend(tit_i.split())
    #Asssign number to doc like key and stemming of a recipe like value
    ListaDocs[i]=" ".join(stem_i)
    
#%%
# Through a function we build the inverted index
inverted=lb.create_index(ListaDocs)
# Final list of words
wordF=list(inverted.keys())
#%%
# Build with a function a tfidf matrix (listadoc length x length wordF) 
tfidf_matrix=lb.matrixTfIdf(ListaDocs.values(),wordF)
print('The shape of tfidf matrix are ',tfidf_matrix.shape)
#%%           
# Run rank_q and make a query, rank_q is a sorted list that contains tuple like this one: (number of recipes,cosine similarity)
rank_q=lb.ranklist(inverted,wordF,tfidf_matrix,recipes)
#%%
# Print the first 10 recipes
[(Num_Ricetta[rank_q[i][0]],'#'+str(rank_q[i][0])) for i in range(len(rank_q))][:10]
recipes.loc[9836]

