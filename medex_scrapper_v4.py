from bs4 import BeautifulSoup
import requests
from datetime import datetime
import validators
import time
import random
import json
import pandas as pd
import os

# Configuration
BASE_URL = "https://medex.com.bd"
PAGES_TO_SCRAPE = 3
MIN_DELAY = 6
MAX_DELAY = 8
DETAIL_DELAY = 7
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def random_delay(min_sec, max_sec):
    time.sleep(random.randint(min_sec, max_sec))

def scrape_generic_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

def process_generic(generic):
    data = {}
    generic_name = generic.find('div', class_="dcind-title").text.strip()
    link = generic['href']
    
    if not validators.url(link):
        link = BASE_URL + link if not link.startswith(BASE_URL) else link
    
    data['name'] = generic_name
    data['link'] = link
    
    # Scrape generic details
    random_delay(MIN_DELAY, MAX_DELAY)
    details_soup = scrape_generic_page(link)
    if details_soup:
        detail_lists = details_soup.find_all('div', class_="ac-body")
        header_lists = details_soup.find_all('h4', class_="ac-header")
        for detail, header in zip(detail_lists, header_lists):
            data[header.text.strip()] = detail.text.strip()
    
    return data, link, generic_name

def process_brands(link, generic_name):
    b_link = f"{link}/brand-names" if not link.endswith('/brand-names') else link
    random_delay(MIN_DELAY, MAX_DELAY)
    
    try:
        # Get brand table
        tables = pd.read_html(b_link)
        if not tables:
            return None
            
        # Get additional brand info
        bresponse = requests.get(b_link, headers=HEADERS)
        bsoup = BeautifulSoup(bresponse.content, 'html.parser')
        all_trs = bsoup.findAll("tr", class_="brand-row")
        
        # Prepare data
        records = []
        companies = []
        generics = []
        generic_urls = []
        
        for tr in all_trs:
            records.append(tr['data-href'])
            companies.append(tr['data-company'])
            generics.append(generic_name)
            generic_urls.append(link)
        
        # Enhance the DataFrame
        df = tables[0]
        df['Brand Url'] = records
        df['Generic Name'] = generics
        df['Generic Url'] = generic_urls
        df['Company Id'] = companies
        return df.fillna(0)
    except Exception as e:
        print(f"Error processing brands: {e}")
        return None

def main():
    timestamp = get_timestamp()
    generic_filename = f"medex_medicine_info_with_generic_url_{timestamp}.json"
    brand_filename = f"brand_informations_{timestamp}.csv"
    
    json_data = []
    
    for page_num in range(1, PAGES_TO_SCRAPE + 1):
        print(f"Processing page {page_num}")
        random_delay(MIN_DELAY, MAX_DELAY)
        
        url = f"{BASE_URL}/generics?page={page_num}"
        soup = scrape_generic_page(url)
        if not soup:
            continue
            
        generics = soup.find_all('a', class_="hoverable-block")
        
        for generic in generics:
            generic_data, link, generic_name = process_generic(generic)
            json_data.append(generic_data)
            
            # Process brand names
            brand_df = process_brands(link, generic_name)
            if brand_df is not None:
                # Write header only for first page
                header = not os.path.exists(brand_filename)
                brand_df.to_csv(brand_filename, mode='a', index=False, header=header)
    
    # Save generic data
    with open(generic_filename, "w") as outfile:
        json.dump(json_data, outfile, indent=4)
    
    print("Scraping completed successfully")

if __name__ == "__main__":
    main()
