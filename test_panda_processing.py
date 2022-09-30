# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 19:28:27 2022

@author: AS00340968
"""

import pandas as pd
emailcategory = pd.read_csv('email_set_model.csv')

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

model = fasttext.train_supervised('email_set_labelled.txt',epoch=25,lr=1.0,wordNgrams=1)


test_hasil=model.predict('mandiri utama finance',k=1,threshold=0.0,on_unicode_error='strict')

# print(test_hasil)


#print(test_hasil[0][0])

def predict_Text(text):
    
    
    hasil_predict=model.predict(text.lower(),k=1,threshold=0.0,on_unicode_error='strict')
    
    
    return hasil_predict[0][0]


def print_results(model, input_path, k):
    num_records, precision_at_k, recall_at_k = model.test(input_path, k)
    f1_at_k = 2 * (precision_at_k * recall_at_k) / (precision_at_k + recall_at_k)

    print("records\t{}".format(num_records))
    print("Precision@{}\t{:.3f}".format(k, precision_at_k))
    print("Recall@{}\t{:.3f}".format(k, recall_at_k))
    print("F1@{}\t{:.3f}".format(k, f1_at_k))
    print()
    

for k in range(1, 3):
    print('train metrics:')
    print_results(model, 'email_train.txt', k)

    print('test metrics:')
    print_results(model, 'email_valid.txt', k)

