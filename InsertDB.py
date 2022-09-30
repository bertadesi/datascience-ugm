# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 12:22:09 2022

@author: AS00340968
"""

import mysql.connector


db=mysql.connector.connect(user="datascience_ugm",passwd=,host="db4free.net",database='datascience_ugm')

my_cursor=db.cursor()

def save(result):

    # adding a common query to insert all the students
    query = "INSERT INTO tbl_master_extract(from_email,to_email,subject,body,receive_date,category,amount) VALUES(%s,%s,%s,%s,%s,%s,%s)" # adding a common query to insert all the v
    #list containing the information about the students in tuple form

    # from datetime import datetime
    # now = datetime.now()
    # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    # stds = [("shedron3@gmail.com","shedron3@gmail.com","Test Subject",'Body',formatted_date)] 
 
    my_cursor.executemany(query,result)
    db.commit()
    hasil =my_cursor.rowcount 
    return hasil

def pullReport():
    
      
    my_cursor.execute("SELECT category, sum(amount) as total FROM tbl_master_extract where 1 group by category order by total")
    hasil=my_cursor.fetchall()
    
    
    for row in hasil:
        
        
        Detail_Category=[]
        Sum_Amount=[]
            
        Detail_Category=Detail_Category.append(row[0])
        Sum_Amount =Sum_Amount.append(row[1])
        # print(row['category'])
    
    return hasil
    
