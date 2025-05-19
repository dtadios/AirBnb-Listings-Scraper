from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import time

# todo: Selenium code for navigating to multiple pages
# Use API for IP rotation
# Done: Get property descriptions from one page
driver = webdriver.Chrome()

driver.get("https://www.airbnb.com/s/tokyo/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-05-01&monthly_length=3&monthly_end_date=2025-08-01&price_filter_input_type=2&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change")
time.sleep(5)


html = driver.page_source
driver.quit()

# Parsing one page
soup = BeautifulSoup(html,'html.parser')


# priceClass = "umg93v9 atm_7l_rb934l atm_cs_1peztlj atm_rd_14k51in atm_cs_kyjlp1__1v156lz dir dir-ltr"
# cutPriceClass = "umuerxh atm_7l_dezgoh atm_rd_us8791 atm_cs_1529pqs__oggzyc atm_cs_kyjlp1__1v156lz dir dir-ltr"
allData = soup.find_all("div",{"itemprop" : "itemListElement"})
l = []
o = {}

for i in range(0,len(allData)):
    try:
        o["property-title"]=allData[i].find('div',{'data-testid':'listing-card-title'}).text.lstrip().rstrip()
    except:
        o["property-title"]=None
    try:
        o["rating"]=allData[i].find('div',{'class':'t1a9j9y7'}).text.split()[0]
    except:
        o["rating"]=None
    try:
        o["price"]=allData[i].find('span',{"class":"umg93v9 atm_7l_rb934l atm_cs_1peztlj atm_rd_14k51in atm_cs_kyjlp1__1v156lz dir dir-ltr"}).text.lstrip().rstrip().split()[0]
    except:
        o["price"]=None
    try:
        o["cut-price"]=allData[i].find('span',{'class':'umuerxh atm_7l_dezgoh atm_rd_us8791 atm_cs_1529pqs__oggzyc atm_cs_kyjlp1__1v156lz dir dir-ltr'}).text.lstrip().rstrip().split()[0]
    except:
        o["cut-price"]=None
    l.append(o)
    o={}
    



