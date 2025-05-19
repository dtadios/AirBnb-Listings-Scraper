import sqlite3
from sqlite3 import Error
from selenium_scrape import l
# todo: watch youtube sqlite video
# todo: fix selenium double opening url
# add listings to db 
def add_listing(listing):
    property_title = listing['property-title']
    rating = listing['rating']
    price = listing['price']
    cut_price = listing['cut_price']
    c.execute("INSERT INTO employees VALUES (property_title, rating, price, cut_price)")
    connection.commit()
    
def create_db():
    c.execute("""CREATE TABLE listings ( 
            property_title text,
            rating text,
            price text,
            cut_price text
            )""")

if __name__ == "__main__":
    connection = None
    try:
        connection = sqlite3.connect(':memory:')
    except Error as e:
        print(f"The error '{e}' occurred")
        
    c = connection.cursor()
# c.execute("SELECT * FROM employees WHERE last='John'")
# print(c.fetchone())

    connection.close()
    print(l)