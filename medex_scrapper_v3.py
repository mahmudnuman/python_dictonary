from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import time
import random

page =10



now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "medex_medicine_info_with_brand_url_" + str(tobe_added) +".csv"

with open(name,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Brand Name","Power","URL","Manufacturer","Unit Price"]
    thewriter.writerow(header)
    for p in range(1,page):
        num = random.randint(7, 20)

        time.sleep(num)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        url = "https://medex.com.bd/brands?page=" +str(p)
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')   
        lists = soup.find_all('a',class_="hoverable-block")    
        for list in lists:            
            brand_name = list.find('div',class_="data-row-top").get_text
            power = list.find('span',class_="grey-ligten").get_text
            link = list['href']
            manufacturer = list.find('span',class_="data-row-company").get_text
            price = list.find('span',class_="package-pricing").get_text
            info = [brand_name,power,link,manufacturer,price]
            thewriter.writerow(info )
            
            
            
print("Scrapped Successfully")