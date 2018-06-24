import requests
from bs4 import BeautifulSoup
import csv
import time
import final_lib as lb
import importlib
importlib.reload(lb)
#%%
# We create a dict with all the recipes
link_recipes = {}
# We need only the letter 's' and the recipe 'tuscan pest' to find all the recipes
print("search recipes for the letter s")
cnt = requests.get("http://www.bbc.co.uk/food/recipes/search?keywords=s")
count=0
# We put some time delay between request
while str(cnt)!='<Response [200]>' and count<10:
    time.sleep(1)
    count+=1
    cnt = requests.get("http://www.bbc.co.uk/food/recipes/search?keywords=s")
soup = BeautifulSoup(cnt.text , "lxml")
lst=[]
# We find the number of pages of recipes in the website
for link in soup.find_all('a'):
    if link.get("href").startswith('/food/recipes/search?'):
        lst.append(link.contents[0])
if lst:
    maxpage=int(lst[-2])
else:
    maxpage=1
print('There is',maxpage,"recipes page")
i=0
for page in range(1,maxpage+1):
    # We print number page some time
    for i in range(0,748,15):
        if page==i:
            print('pagina numero',page)      
    cnt=requests.get('http://www.bbc.co.uk/food/recipes/search?page='+str(page)+'&keywords=s')
    count=0
    while str(cnt)!='<Response [200]>' and count<10:
        time.sleep(1)
        count+=1
        cnt=requests.get('http://www.bbc.co.uk/food/recipes/search?page='+str(page)+'&keywords=s')
    soup = BeautifulSoup(cnt.text , "lxml")
    # We take all the links of recipes for that page
    for link in soup.find_all("a"):
        if(link.get("href").startswith('/food/recipes/')
           and not link.get('href')=='/food/recipes/'
           and "search" not in link.get('href')):
            link_recipes[link.get('href')] = ""
            i+=1
# We add the last recipe
link_recipes['/food/recipes/tuscanpesto_82385']=""
#%% We write the csv file
#==============================================================================
# f=open('ricelett.txt','w')
# for k in link_recipes.keys():
#     f.write(k+'\n')
# f.close()
#==============================================================================
#%%
# These lines of code need us for opening the list of recipes' link
f=open("ricelett.txt")
allrecipes=[]
for row in csv.reader(f, delimiter='\t'):
    allrecipes.append(row[0])
f.close()
#%%    
# with this function we estract all the info about every single recipe
# and write these in a big csv file named 'ricette.csv'
lb.All_in_CSV(allrecipes)

    
    
    