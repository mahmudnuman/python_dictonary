from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import time

page =30000

#this scrapper is incomplete


now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "medex_medicine_info_" + str(tobe_added) +".csv"

with open(name,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Brand Name","Power","Manufacturer","Unit Price"]
    thewriter.writerow(header)
    for p in range(1,page):


        time.sleep(5)

        url = "https://medex.com.bd/brands/" +str(p)

        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        lists = soup.find_all('div',class_="container")
        #print(lists)
        
        for list in lists:
            brand_name = list.find('h1',class_="page-heading-1-l").text.replace('\n', '')
            type = list.find('small',class_="h1-subtitle").text.replace('\n', '')
            
            #print(brand_name)
            #print(type)
            #exit()
            
            power = list.find('span',class_="grey-ligten").text.replace('\n', '')
            generics = list.find('div',class_="col-xs-12").text.replace('\n', '')
            manufacturer = list.find('span',class_="data-row-company").text.replace('\n', '')
            price = list.find('span',class_="package-pricing").text.replace('\n', '')
            info = [brand_name,power,manufacturer,price]
            thewriter.writerow(info )
            
            
            
print("Scrapped Successfully")