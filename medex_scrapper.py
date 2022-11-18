from bs4 import BeautifulSoup
import requests
from csv import writer
import time

page =30000



with open('medex_medicine_informations.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Brand Name","Power","Manufacturer","Unit Price"]
    thewriter.writerow(header)
    for p in range(1,page):


      
        url = "https://medex.com.bd/brands?page=" +str(p)

        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        print(soup)
        exit
        lists = soup.find_all('a',class_="hoverable-block")
        print(len(lists))
        for list in lists:
            brand_name = list.find('div',class_="data-row-top").text.replace('\n', '')
            power = list.find('span',class_="grey-ligten").text.replace('\n', '')
           # generics = list.find('div',class_="col-xs-12").text.replace('\n', '')
            manufacturer = list.find('span',class_="data-row-company").text.replace('\n', '')
            price = list.find('span',class_="package-pricing").text.replace('\n', '')
            info = [brand_name,power,manufacturer,price]
            thewriter.writerow(info )
            #time.sleep(30)
            
            
            
print("Scrapped Successfully")