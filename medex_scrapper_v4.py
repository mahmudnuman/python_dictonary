from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import validators
import time
import random
import json
import pandas as pd


page =3

#https://www.skytowner.com/explore/beautiful_soup_next_sibling_property

now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "medex_medicine_info_with_generic_url_" + str(tobe_added) +".json"
json_object=[]

for p in range(1,page):
    num = random.randint(6, 10)
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
            json_object.append(data)
            
        b_link=link +'/brand-names'
        time.sleep(7)
        tables=pd.read_html(b_link)
        file=tables[0]
        time.sleep(7)
        response = requests.get(b_link,headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_trs = soup.findAll("tr",class_="brand-row")
        record = []
        generic =[]
        generic_url =[]
        gen_link=link
        for tr in all_trs:
            blink = tr['data-href']
            record.append(blink)
            generic.append(generic_name)
            generic_url.append(gen_link)
        file['Brand Url'] = record
        file['Generic Name'] = generic
        file['Generic Url'] = generic_url
        file = file.fillna(0)
        bname= "from_generics_to_brand_informations" + str(tobe_added) +".json"

        file.to_csv('brand_informations.csv', mode='a', index=False, header=False)
           # file.to_json(bname,orient='records')


            
                           
with open(name, "w") as outfile:
    outfile.write(json.dumps(json_object,indent=4))
     
            
print("Scrapped Successfully")