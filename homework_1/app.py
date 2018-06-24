# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 19:10:34 2016

@author: Umbertojunior
"""

from tkinter import *
#from PIL import ImageTk,Image as i
#from alg import *

import lib2 as lb
import pandas as pd
import re
import csv
import numpy as np
import importlib
np.set_printoptions(precision=2)
importlib.reload(lb)

#%%
l=open('listdoc.txt','r', encoding='utf-8-sig')
a=l.read()
ListaDocs=eval(a)
l.close()

h=open('words.txt', 'r')
b=h.read()
wordF=eval(b)
h.close()
#%%

tfidf_matrix=lb.matrixTfIdf(ListaDocs.values(),wordF)
#print('Questa è una matrice di dimensioni',tfidf_matrix.shape)

#%%
g= open('invertedInd.txt', 'r')
lec=g.read()
inverted=eval(lec)
g.close()

recipes=pd.read_csv("ricettecontitolo.csv",sep='\t')

f= open('Namerecip.txt', 'r', encoding='utf-8-sig')
lect=f.read()
Num_Ricetta=eval(lect)
f.close()
#%%
#rank_q=lb.ranklist(input(),inverted,wordF,tfidf_matrix,recipes)
#[(Num_Ricetta[rank_q[i][0]],'#',rank_q[i][0]) for i in range(len(rank_q))][:10]
#recipes.loc[6304]










state = ''
buttons = []
tp=['Vegetarian','lactose intolerant', 'I eat everything']
#im = i.open('C:/Users/Umbertojunior/Desktop/sapienza.png')

def callback(event):
    veg=''
    if var.get()==0:
        veg='VV '
    s=v.get()    
    new = Tk()
    new.title('results')
    new.geometry()
    tit= Label(new, text='please choose what recipies do you want to visualize')
    tit.pack()
    list1= Listbox(new)
    response=lb.ranklist(veg+s,inverted,wordF,tfidf_matrix,recipes)
    
    for el in response:
        list1.insert(END, Num_Ricetta[el[0]])
   # list1.bind('<Button-1>', op)
    list1.pack()
    ovv= Label(new, text=q)
    ovv.pack()
    new.mainloop()

def op(event):
    answ= Tk()
    answ.geometry('1000x500+300+50')
        
    answ.mainloop()

def onPress(i):
    global state
    state = i
    for btn in buttons:
        btn.deselect()
    buttons[i].select()
    

app = Tk()
app.geometry('800x300+300+200')
app.title(string='search engine for recipes')



l= Label(app, text='Hello this is the search engine for recipes created by Emanuele Conti, Valerio Rossini ed Umberto Junior Mele',font='Helvetica',fg="blue", bd= 5,cursor='mouse').pack()

var=IntVar()
for i in range(len(tp)):
    rad = Radiobutton(app, text=str(tp[i]), variable=var, 
                            value=str(i), command=(lambda i=i: onPress(i)) )
    rad.pack()
    buttons.append(rad)

v = StringVar()
contents= Entry(app, textvariable=v, bd =5)
contents.pack()

v.set("a default value")
contents.bind('<Return>', callback) 

b = Button(app, text="find", width=10)
b.pack()
b.bind('<Button-1>', callback)




 

 












app.mainloop()
