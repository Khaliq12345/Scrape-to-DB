import sqlite3
import requests
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
import datetime

conn = sqlite3.connect('glasses.db')
c = conn.cursor()

#c.execute('''CREATE TABLE glasses(date Date, brand TEXT, model TEXT, price INT, info TEXT)''')

def getProductData(url):
    headers = {
        'User-Agent': get_random_user_agent()
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    current_date = datetime.datetime.now()
    brand = soup.select_one('.pdp-layout-top-resume-top-left-brand').get_text(strip=True)
    model = soup.select_one('.pdp-layout-top-resume-top-left-model').get_text(strip=True)
    price = soup.select_one('.pdp-layout-top-resume-total-top-content-prices-final').text.replace('$', '').strip()
    desc = soup.select_one('div[aria-label="brand description"]').text.strip()
    c.execute('''INSERT INTO glasses VALUES(?,?,?,?,?)''', (current_date, brand, model, price, desc))
    return brand, model, price, desc, current_date

getProductData('https://www.glasses.com/gl-us/ray-ban/8053672991338')
conn.commit()
print('complete.')

c.execute('''SELECT * FROM glasses''')
results = c.fetchall()
print(len(results))

conn.close()

