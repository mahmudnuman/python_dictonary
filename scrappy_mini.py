from bs4 import BeautifulSoup
import requests
from csv import writer
from datetime import datetime
import time




now = datetime.now() # current date and time
tobe_added = now.strftime("%Y-%m-%d-%H-%M-%S")
name= "mini_scrappy_housing" + str(tobe_added) +".csv"

url="https://www.pararius.com/apartments/amsterdam?ac=1"
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
lists=soup.find_all('section',class_="listing-search-item")

with open(name,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Title","Location","Price","Area","Room"]
    thewriter.writerow(header)
    for list in lists:
        title=list.find('a',class_="listing-search-item__link--title").text.replace('\n', '')
        location=list.find('div',class_="listing-search-item__sub-title").text.replace('\n', '')
        price=list.find('div',class_="listing-search-item__price").text.replace('\n', '')
        area=list.find('li',class_="illustrated-features__item--surface-area").text.replace('\n', '')
        room=list.find('li',class_="illustrated-features__item--number-of-rooms").text.replace('\n', '')
        info=[title,location,price,area,room]
        thewriter.writerow(info )
