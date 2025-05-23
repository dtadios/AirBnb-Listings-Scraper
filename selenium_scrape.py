from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# todo: Fix get_multiple_items() returning only 3 lists with one property each
# todo: Rotate IPs
# todo: configure Git


# Done: Navigated to multiple pages

def get_listings(url = None):
    """ 
    Takes
    """
    driver = webdriver.Chrome()
    url = "https://www.airbnb.com/s/tokyo/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-05-01&monthly_length=3&monthly_end_date=2025-08-01&price_filter_input_type=2&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change"
    driver.get(url)
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Close"]'))).click() # wait until close is interactable
    
    pages_html = []
    for i in range(3):
        current_url = driver.current_url
        driver.get(current_url)
        html = driver.page_source  
        soup = BeautifulSoup(html,'html.parser')
        one_page_html = soup.find_all("div",{"itemprop" : "itemListElement"}) # gets html of one page
        pages_html.append(one_page_html)
        sleep_time = random.uniform(5,10)
        time.sleep(sleep_time)

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//a[@aria-label="Next"]'))).click()    # wait until next is interactable

    driver.quit()
    # for i in range(len(pages_html)):
    #     print(f"Page{i}__________________________________________________")
    #     print(pages_html[i])
    return pages_html

def get_items(property_list: list):
    """ 
    Input: One page of html
    Returns: List of dictionaries containing each properties's details
    """
    l = []
    o = {}
    
    for i in range(0,len(property_list)): # rewrite to iterate through pages_html
        try:
            o["property-title"]=property_list[i].find('div',{'data-testid':'listing-card-title'}).text.lstrip().rstrip()
        except:
            o["property-title"]=None
        try:
            o["rating"]=property_list[i].find('div',{'class':'t1a9j9y7'}).text.split()[0]
        except:
            o["rating"]=None
        try:
            o["price"]=property_list[i].find('span',{"class":"umg93v9 atm_7l_rb934l atm_cs_1peztlj atm_rd_14k51in atm_cs_kyjlp1__1v156lz dir dir-ltr"}).text.lstrip().rstrip().split()[0]
        except:
            o["price"]=None
        try:
            o["cut-price"]=property_list[i].find('span',{'class':'umuerxh atm_7l_dezgoh atm_rd_us8791 atm_cs_1529pqs__oggzyc atm_cs_kyjlp1__1v156lz dir dir-ltr'}).text.lstrip().rstrip().split()[0]
        except:
            o["cut-price"]=None
        l.append(o)
        o={}
        
    return l

def get_multiple_items(pages_html: list):
    for page in pages_html:
        print(get_items(page))

# get_listings()
get_multiple_items(get_listings())