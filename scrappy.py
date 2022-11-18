from bs4 import BeautifulSoup
import requests
from csv import writer


page =30



with open('amsterdam_housing.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ["Title","Location","Price","Area","Room"]
    thewriter.writerow(header)
    for p in range(1,page):


        url = "https://www.pararius.com/apartments/amsterdam/page-" +str(p)

      #url = "https://www.pararius.com/apartments/amsterdam?ac=1"
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        lists = soup.find_all('section',class_="listing-search-item")
        for list in lists:
            title = list.find('a',class_="listing-search-item__link--title").text.replace('\n', '')
            location = list.find('div',class_="listing-search-item__sub-title").text.replace('\n', '')
            price = list.find('div',class_="listing-search-item__price").text.replace('\n', '')
            area = list.find('li',class_="illustrated-features__item--surface-area").text.replace('\n', '')
            room = list.find('li',class_="illustrated-features__item--number-of-rooms").text.replace('\n', '')
            info = [title,location,price,area,room]
            thewriter.writerow(info )


print("Scrapped Successfully")