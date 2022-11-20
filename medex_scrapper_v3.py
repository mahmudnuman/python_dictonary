from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import time

page =41

#this scrapper is incomplete, this comment will be removed when tested and done


now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "medex_medicine_info_with_brand_url_" + str(tobe_added) +".csv"

with open(name,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Brand Name","Power","URL","Manufacturer","Unit Price"]
    thewriter.writerow(header)
    for p in range(1,page):
        time.sleep(7)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        url = "https://medex.com.bd/brands?page=" +str(p)
        page = requests.get(url,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')   
        lists = soup.find_all('a',class_="hoverable-block")    
        for list in lists:            
            brand_name = list.find('div',class_="data-row-top").text.strip()
            power = list.find('span',class_="grey-ligten").text.strip()
            link = list['href']
            manufacturer = list.find('span',class_="data-row-company").text.strip()
            price = list.find('span',class_="package-pricing").text.strip() 
            info = [brand_name,power,link,manufacturer,price]
            thewriter.writerow(info )
            
            
            
print("Scrapped Successfully")