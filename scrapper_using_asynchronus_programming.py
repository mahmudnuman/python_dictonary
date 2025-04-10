import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
import validators
import json
import pandas as pd
import os
import random
import time
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from io import StringIO

# Configuration
BASE_URL = "https://medex.com.bd"
PAGES_TO_SCRAPE = 3
MIN_DELAY = 6
MAX_DELAY = 8
DETAIL_DELAY = 7
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
CONCURRENT_REQUESTS = 5  # Be gentle with the server

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except ClientError as e:
        print(f"Error fetching {url}: {e}")
        return None

async def scrape_generic_page(session, url):
    await asyncio.sleep(random.randint(MIN_DELAY, MAX_DELAY))
    html = await fetch(session, url)
    return BeautifulSoup(html, 'html.parser') if html else None

async def process_generic(session, generic):
    data = {}
    generic_name = generic.find('div', class_="dcind-title").text.strip()
    link = generic['href']
    
    if not validators.url(link):
        link = BASE_URL + link if not link.startswith(BASE_URL) else link
    
    data['name'] = generic_name
    data['link'] = link
    
    # Scrape generic details
    details_soup = await scrape_generic_page(session, link)
    if details_soup:
        detail_lists = details_soup.find_all('div', class_="ac-body")
        header_lists = details_soup.find_all('h4', class_="ac-header")
        for detail, header in zip(detail_lists, header_lists):
            data[header.text.strip()] = detail.text.strip()
    
    return data, link, generic_name

async def process_brands(session, link, generic_name, timestamp):
    b_link = f"{link}/brand-names" if not link.endswith('/brand-names') else link
    await asyncio.sleep(random.randint(MIN_DELAY, MAX_DELAY))
    
    try:
        # Get brand table
        async with session.get(b_link) as response:
            html = await response.text()
            tables = pd.read_html(StringIO(html))  # Fixed here
            if not tables:
                return None
                
        # Rest of your function remains the same
        bsoup = BeautifulSoup(html, 'html.parser')
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
        
        # Save to CSV
        brand_filename = f"brand_informations_{timestamp}.csv"
        header = not os.path.exists(brand_filename)
        df.fillna(0).to_csv(brand_filename, mode='a', index=False, header=header)
        
    except Exception as e:
        print(f"Error processing brands: {e}")

async def process_page(session, page_num, timestamp, json_data):
    print(f"Processing page {page_num}")
    url = f"{BASE_URL}/generics?page={page_num}"
    soup = await scrape_generic_page(session, url)
    if not soup:
        return
    
    generics = soup.find_all('a', class_="hoverable-block")
    
    # Process generics concurrently but with limited concurrency
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    
    async def process_one_generic(generic):
        async with semaphore:
            generic_data, link, generic_name = await process_generic(session, generic)
            json_data.append(generic_data)
            await process_brands(session, link, generic_name, timestamp)
    
    await asyncio.gather(*[process_one_generic(generic) for generic in generics])

async def main():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    generic_filename = f"medex_medicine_info_with_generic_url_{timestamp}.json"
    json_data = []
    
    async with ClientSession(headers=HEADERS) as session:
        tasks = [process_page(session, page_num, timestamp, json_data) 
                for page_num in range(1, PAGES_TO_SCRAPE + 1)]
        await asyncio.gather(*tasks)
    
    # Save generic data
    with open(generic_filename, "w") as outfile:
        json.dump(json_data, outfile, indent=4)
    
    print("Scraping completed successfully")

if __name__ == "__main__":
    asyncio.run(main())
