from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# todo: Rotate IPs

# Done: Fixed get_multiple_items() returning only 3 lists with one property each
# Done: Configured Git

def get_listings(url = None):
    """ 
    Takes
    """
    driver = webdriver.Chrome()
    url = "https://www.airbnb.com/s/tokyo/homes?refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-05-01&monthly_length=3&monthly_end_date=2025-08-01&price_filter_input_type=2&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change"
    driver.get(url)
    
    # Wait for and close the initial popup
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Close"]'))).click()
    
    pages_html = []
    for i in range(3):
        # Wait for listings to be present on the page
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[itemprop="itemListElement"]'))
        )
        
        # Add a small delay to ensure all dynamic content is loaded
        time.sleep(3)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        one_page_html = soup.find_all("div", {"itemprop": "itemListElement"})
        pages_html.append(one_page_html)
        
        # Don't click next on the last iteration
        if i < 2:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next"]'))
            )
            next_button.click()
            
            # Wait for the URL to change and page to start loading
            time.sleep(random.uniform(5, 10))

    driver.quit()
    return pages_html

def get_items(property_list: list):
    """ 
    Input: One page of html
    Returns: List of dictionaries containing each properties's details
    """

    properties = []
    
    for property_item in property_list:
        property_data = {}
        
        # Extract property title
        title_elem = property_item.find('div', {'data-testid': 'listing-card-title'})
        property_data["property-title"] = title_elem.text.strip() if title_elem else None
        
        # Extract rating - using a more general selector
        rating_elem = property_item.find('span', {'class': lambda x: x and 'r1dxllyb' in x})
        property_data["rating"] = rating_elem.text.split()[0] if rating_elem else None
        
        # Extract current price - using a more general selector
        price_elem = property_item.find('span', {'class': lambda x: x and 'a8jt5op' in x})
        property_data["price"] = price_elem.text.strip().split()[0] if price_elem else None
        
        # Extract original price (if discounted) - using a more general selector
        cut_price_elem = property_item.find('span', {'class': lambda x: x and 'umuerxh' in x})
        property_data["cut-price"] = cut_price_elem.text.strip().split()[0] if cut_price_elem else None
        
        properties.append(property_data)
    
    return properties

def get_multiple_items(pages_html: list):
    for page in pages_html:
        print(get_items(page))

# get_listings()
get_multiple_items(get_listings())