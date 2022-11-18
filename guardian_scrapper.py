from bs4 import BeautifulSoup
import requests
from csv import writer
import time



with open('guardian_news.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Title","URL"]
    thewriter.writerow(header)
    
    url = "https://www.theguardian.com/uk"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    lists=soup.find_all('h3',class_="fc-item__title")
    t=0
    for list in lists:
        title=list.find('span',class_="js-headline-text").text
        url=list.find('a',class_="fc-item__link")["href"]
        data=[title,url]
        thewriter.writerow(data)
print("Scrapped Successfully")


        