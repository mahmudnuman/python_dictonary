from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import validators
import time
import random
import json


page =85

#https://www.skytowner.com/explore/beautiful_soup_next_sibling_property

now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "medex_medicine_info_with_generic_url_" + str(tobe_added) +".json"
json_object=[]
    # header = [
    #           "Generic Name",
    #           "URL",
    #           "Indications",
    #           "Pharmacology",
    #           "Dosage",
    #           "Administration",
    #           "Interaction",
    #           "Contradictions",
    #           "Side Effects",
    #           "Pregnancy & Lactation",
    #           "Precautions & Warning",
    #           "Therapeutic Class",
    #           "Storage Condtions"
    #           ]
    # thewriter.writerow(header)

for p in range(1,page):
    num = random.randint(6, 10)
    json_data=[]
    time.sleep(num)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    url = "https://medex.com.bd/generics?page=" +str(p)
    page = requests.get(url,headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')   
    lists = soup.find_all('a',class_="hoverable-block")  
    for list in lists:
        data = {}            
        generic_name = list.find('div',class_="dcind-title").text.strip()
        link = list['href']
        if validators.url(link):
            time.sleep(7)
            details_page = requests.get(link,headers=headers)
            details_soup = BeautifulSoup(details_page.content,'html.parser')   
            detail_lists = details_soup.find_all('div',class_="ac-body")
            header_lists = details_soup.find_all('h4',class_="ac-header")
            data['name'] = generic_name
            data['link'] = link
            for detail,header in zip(detail_lists,header_lists):
                    head = header.text.strip()
                    det = detail.text.strip()
                    data[head]=det
            json_data.append(data)

    json_object.append(json_data)
                           
with open(name, "w") as outfile:
    outfile.write(json.dumps(json_object,indent=4))
     
            
print("Scrapped Successfully")