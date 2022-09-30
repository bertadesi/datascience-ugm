# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 08:59:51 2022

@author: AS00340968
"""

import InsertDB
import matplotlib.pyplot as plt

hasil=InsertDB.pullReport()

Detail_Category=[]
Sum_Amount=[]
for row in hasil:
    
    print(row[0])
    Detail_Category.append(row[0])
    Sum_Amount.append((row[1]))
    # print(row['category'])
     
print("Label of Category = ", Detail_Category)
print("Sum of Transaction = ", Sum_Amount)
 
 
#Visulizing Data using Matplotlib
plt.barh(Detail_Category, Sum_Amount)
plt.xlabel("Label of Categories")
plt.ylabel("Sum of Amount")
plt.title("Total Expense Spent")
plt.show()
