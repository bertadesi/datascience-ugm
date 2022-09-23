# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 19:28:27 2022

@author: AS00340968
"""

import pandas as pd
emailcategory = pd.read_csv('email_set.csv')

from io import StringIO
import csv

import fasttext


col = ['category', 'subject']
emailcategory = emailcategory[col]
emailcategory = emailcategory[pd.notnull(emailcategory['subject'])]
emailcategory.columns = ['category', 'subject']
emailcategory.head()



emailcategory['category']=['__label__'+s.replace(' or ', '$').replace(', or ','$').replace(',','$').replace(' ','_').replace(',','__label__').replace('$$','$').replace('$',' __label__').replace('___','__') for s in emailcategory['category']]
emailcategory['category']

emailcategory['subject']= emailcategory['subject'].replace('\n',' ', regex=True).replace('\t',' ', regex=True)


emailcategory.to_csv(r'email_set_labelled.txt', index=False, sep=' ', header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar=" ")

model = fasttext.train_supervised('email_set_labelled.txt',epoch=25)

test_hasil=model.predict('indihome',k=1,threshold=0.0,on_unicode_error='strict')
#print(test_hasil)

#print(test_hasil[0][0])

def predict_Text(text):
    
    hasil_predict=model.predict(text,k=1,threshold=0.0,on_unicode_error='strict')
    
    
    return hasil_predict[0][0]



# hasil_test = model.test('email_valid.txt',k=1,threshold=0.0)

# print(hasil_test)
