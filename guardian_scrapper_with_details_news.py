from bs4 import BeautifulSoup
import requests
from csv import writer
import time
import validators


localtime = time.localtime()
tobe_added = time.strftime("%I_%M_%S_%p", localtime)
name= "guardian_news_with_details_" + str(tobe_added) +".csv"

with open(name,'w',encoding='utf-8',newline='') as f:
    thewriter = writer(f)
    header = ["Title","URL","News Detail"]
    thewriter.writerow(header)
    
    url = "https://www.theguardian.com/uk"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,"html.parser")
    lists=soup.find_all('h3',class_="fc-item__title")

    for list in lists:
        title=list.find('span',class_="js-headline-text").text
        link=list.find('a',class_="fc-item__link")["href"]
        
        if validators.url(link):
            page=requests.get(link)
            soup=BeautifulSoup(page.content,"html.parser")
            details=soup.find_all('p',class_="dcr-2v2zi4")
            detail_news=""
            
            for detail in details:
                detail_news +=  detail.text
                time.sleep(20)
                



        data=[title,link,detail_news]
        thewriter.writerow(data)
print("Scrapped Successfully")


        