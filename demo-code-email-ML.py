# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 13:46:15 2022

@author: AS00340968
"""

import os
import pickle
import re
from re import search
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types

from bs4 import BeautifulSoup
import InsertDB
import test_panda_processing


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
#our_email = 'shedron3@gmail.com'
mia_email = 'resmiatisari03@gmail.com'


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            #flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.json", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

service =gmail_authenticate()

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def parse_parts(service, parts, message):
    """
    Utility function that parses the content of an email partition
    """
    result=[]
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            
               
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                
                parse_parts(service, part.get("parts"), message)
                
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:

                    filename = "index.html"
                    with open(filename, "wb") as f:
                        f.write(urlsafe_b64decode(data))

                    html_page = open("index.html", "r")
                    soup = BeautifulSoup(html_page, "html.parser")

                    html_text = soup.get_text()
                    data=html_text.split()
                                        
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                if not filename:
                    filename = "index.html"
                    with open(filename, "wb") as f:
                        f.write(urlsafe_b64decode(data))

                    html_page = open("index.html", "r")
                    soup = BeautifulSoup(html_page, "html.parser")

                    html_text = soup.get_text()
                    data=html_text.split()
                    
                    if not (search("Menunggu",message)):
                        
                        
                        if  (search("Konfirmasi Pembayaran Tagihan IndiHome",message)):
                
                            posisi = data.index('Rp.')  
                            value=data[posisi+1]
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                                                                                    
                   
                        if  (search("Mandiri Utama Finance",message)):
                            posisi = data.index('Bayar')  
                            value=(data[posisi+1])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            
                            
                        if  (search("PBB",message)):
                            posisi = data.index('Pembayaran')  
                            value=(data[posisi+1])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            
                            
                        if  (search("Pembayaran",message))and (search("lazada.co.id",message)):
                            posisi = data.index('dibayar')  
                            value=(data[posisi+4])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            
                        if  (search("Konfirmasi",message))and (search("shopee.co.id",message)):
                             posisi = data.index('Dibayarkan:')  
                             value=(data[posisi+2])
                             category = test_panda_processing.predict_Text(message)
                             result=[category,value]
                            
                        
                        if (search("Kesehatan",message)):
                            posisi = data.index('Total')
                            value=(data[posisi+2])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            

                        if(search("tagihan air",message)):
                            posisi = data.index('Total')
                            value=(data[posisi+2])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            

                        if(search("Listrik",message)):
                            posisi = data.index('Total')
                            value=(data[posisi+1])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            

                        if(search("Kartu Kredit",message)):
                            posisi = data.index('Pembayaran')
                            value=(data[posisi+1])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            
                                                          
                        if(search("ZALORA",message)):
                            posisi = data.index('Total')
                            value=(data[posisi+4])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                            
                            
                        if(search("Pascabayar",message)):
                         
                            posisi = data.index('Total')
                            value=(data[posisi+2])
                            category = test_panda_processing.predict_Text(message)
                            result=[category,value]
                    
                
                return result                 	
                    
            else:
                
                print('we leave it for next case study')
                # attachment other than a plain text or HTML

                return result     

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    email_from=""
    email_to=""
    subject =""
    Date =""
   
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            
            if name.lower() == 'from':
                # we print the From address
                email_from = value
            if name.lower() == "to":
                # we print the To address
                email_to = value
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                subject = value
              


               
            if name.lower() == "date":
                # we print the date when the message was sent
                #print("Date:", value)
                Date=value
                
                
    wildcard= subject +' '+ email_from  +' '+email_to                              
    if (search("pembayaran",wildcard)) or (search("Pembayaran",wildcard)) :
        if not (search("Menunggu",wildcard)):
                    
                    print("To:", email_to)
                    print("From:", email_from)
                    print("Date:", Date)
                    print("Subject:", subject)
                    result = parse_parts(service, parts, wildcard)
                    print(result)
                    if  result is not None:
                        
                        if len(result) >0:
                            category=result[0]
                            amount=re.sub("\D","",result[1])
                            allResult=[(email_from,email_to,subject,"EMPTY",Date,category,amount)]
                            hasil=InsertDB.save(allResult)
        
                        
    
results = search_messages(service, "subject:Pembayaran")
print(f"Found {len(results)} results.")
# for each email matched, read it (output plain/text to console & save HTML and attachments)
for msg in results:
    read_message(service, msg)






