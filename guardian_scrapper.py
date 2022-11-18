from bs4 import BeautifulSoup
import requests
from csv import writer
import time


localtime = time.localtime()
tobe_added = time.strftime("%I_%M_%S_%p", localtime)
name= "guardian_news_" + str(tobe_added) +".csv"

with open(name,'w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Title","URL"]
    thewriter.writerow(header)
    
    url = "https://www.theguardian.com/uk"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    lists=soup.find_all('h3',class_="fc-item__title")
    for list in lists:
        title=list.find('span',class_="js-headline-text").text
        url=list.find('a',class_="fc-item__link")["href"]
        data=[title,url]
        thewriter.writerow(data)
print("Scrapped Successfully")

