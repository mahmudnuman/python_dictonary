from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import validators
import time
import random

page =2

#https://www.skytowner.com/explore/beautiful_soup_next_sibling_property

now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "medex_medicine_info_with_generic_url_" + str(tobe_added) +".csv"

with open(name,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = [
              "Generic Name",
              "URL",
              "Indications",
              "Pharmacology",
              "Dosage",
              "Administration",
              "Interaction",
              "Contradictions",
              "Side Effects",
              "Pregnancy & Lactation",
              "Precautions & Warning",
              "Therapeutic Class",
              "Storage Condtions"
              ]
    thewriter.writerow(header)
    for p in range(1,page):
        num = random.randint(6, 10)

        time.sleep(num)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        url = "https://medex.com.bd/generics?page=" +str(p)
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')   
        lists = soup.find_all('a',class_="hoverable-block")    
        for list in lists:            
            generic_name = list.find('div',class_="dcind-title").text.strip()
            link = list['href']
            if validators.url(link):
                time.sleep(7)
                details_page = requests.get(link,headers=headers)
                details_soup = BeautifulSoup(details_page.content,'html.parser')   
                detail_lists = details_soup.find_all('div',class_="ac-body")
                print(detail_lists)
                print(len(detail_lists))
                for i in range(len(detail_lists)):
                     print (i, end = " ")
                # exit()
                # indications = detail_lists[0].text.strip()
                # pharmacology = detail_lists[1].text.strip()
                # dosage = detail_lists[2].text.strip()
                # administration = detail_lists[3].text.strip()
                # interaction = detail_lists[4].text.strip()
                # contradictions = detail_lists[5].text.strip()
                # side_effects = detail_lists[6].text.strip()
                # pregnancy_and_lactation = detail_lists[7].text.strip()
                # precautions_and_Warning = detail_lists[8].text.strip()
                # therapeutic_class = detail_lists[9].text.strip()
                # storage_condtions = detail_lists[10].text.strip()
                
                # print(generic_name)
                # print(link)
                # exit()
                continue
                info = [
                        generic_name,
                        link,
                        indications,
                        pharmacology,
                        dosage,
                        administration,
                        interaction,
                        contradictions,
                        side_effects,
                        pregnancy_and_lactation,
                        precautions_and_Warning,
                        therapeutic_class,
                        storage_condtions
                        ]
                
                thewriter.writerow(info )
            
            
exit()
            
print("Scrapped Successfully")