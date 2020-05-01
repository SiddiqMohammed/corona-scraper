from bs4 import BeautifulSoup
from lxml import html
import time
import requests

# from firebase import firebase
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# initializations 
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#Reading the JSON file
with open('serviceAccountKey.json') as f:
  data = json.load(f)
  
url = data["url"]
Database_link = data["Database_link"]
put_link = data["put_link"]
x = ''




def updates():
    # time.sleep(5)

    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")

    listed = []
    listed1 = []
    text_list = ['Mild', 'Serious', 'Recovered', 'Deaths', 'Active', 'Closed', 'Total']
    i = 0
   
   
    for my_tag in soup.find_all(class_="number-table"):
        listed.append(my_tag.text.strip())

    for i in range(len(listed)):
        x = listed[i]
        x = x.replace(",", "")
        listed1.append(int(x))

    
    listed1.append(listed1[0] + listed1[1])
    listed1.append(listed1[2] + listed1[3])
    listed1.append(listed1[4] + listed1[5])

    print(listed1)
    i = 0

    while i < len(listed1):
        # result = firebase.put(put_link, "'{}'".format(text_list[i]), listed1[i])
        #adding first data
        doc_ref = db.collection('data').document('lgtq2xqlRv40YirvlJ8n')
        
        doc_ref.update({text_list[i] : listed1[i]})
        i += 1

    



#Main Function Starts Seperate Which Will Be Useful If Adding Functions In The Future
def Start():
    updates()


#Running The Code Forever
while True:
    Start()     
    print("updated")
    time.sleep(10)  #1800s = 30mins

#Running The Code For A Specific Number Of times Or Specific Amount Of Time
# for i in range(1):       #Number Of Times
#     time.sleep(1)    #Time In Seconds 
#     Start()
#     print("update")
