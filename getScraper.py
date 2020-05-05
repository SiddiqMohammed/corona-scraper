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



countries_ws = []


with open('codes2.json') as f:
    save = list(json.load(f).items())

with open('codes2.json') as f:
    codes = list(json.load(f))

with open('cc.json') as f:
    countries = list(json.load(f))

page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

def updates():

    listed = []
    listed1 = []
    text_list = ['Mild', 'Serious', 'Recovered', 'Deaths', 'Active', 'Closed', 'Total']
    i = 0
   
   
    for my_tag in soup.find_all(class_="number-table"):
        x = my_tag.text.strip()
        x = x.replace(",", "")
        listed1.append(int(x))
    

    listed1.append(listed1[0] + listed1[1])
    listed1.append(listed1[2] + listed1[3])
    listed1.append(listed1[4] + listed1[5])

    i = 0

    while i < len(listed1):
        #adding first data
        doc_ref = db.collection('data').document('lgtq2xqlRv40YirvlJ8n')
        
        doc_ref.update({text_list[i] : listed1[i]})
        i += 1

    global yeet
    yeet += 1




def updates_each_country():
    #Updating total cases for each country 
    country_values = []

    j = 0

    while j < len(countries):

        remComma = soup.find("td", text=countries[j]).find_next_sibling("td").text
        remComma = remComma.replace(",", "")
        country_values.append(remComma)
        j += 1

    i = 0
    j = 0
    new_dict = []
    flag = 0

    for i in range(len(countries)):
        for j in range(len(codes)):
            if(countries[i] == codes[j]):
                new_dict.append(save[j][1])
    

    i = 0
    while i < len(countries):
        #adding first data
        doc_ref = db.collection('data').document('mm')
        # doc_ref.delete()
        doc_ref.update({new_dict[i] : country_values[i]})
        i += 1
    


yeet = 0

#Running The Code Forever
while True:
    updates()     
    print("updated main numbers")
    if (yeet == 24):
        updates_each_country()
        print("updated each country")
        yeet = 0
    time.sleep(3600)  #1800s = 30mins   3600s = 1hr     86400 = 1day

#Running The Code For A Specific Number Of times Or Specific Amount Of Time
# for i in range(1):       #Number Of Times
#     time.sleep(1)    #Time In Seconds 
#     Start()
#     print("update")
