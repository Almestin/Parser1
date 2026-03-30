from os import link

from bs4 import BeautifulSoup
import requests

url = ("https://auto.ria.com/search/?search_type=1&"
       "category=1&all[0].any[0]."
       "year[0]=2023&all[1].any[0]."
       "fuel[0]=1&"
       "price[0]=1&price[1]=777&price[2]=8888&"
       "gearbox[0]=1&"
       "abroad=0&"
       "customs_cleared=1")
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

item_name = soup.find("div",class_ = 'common-text size-16-20 titleS fw-bold mb-4').text.strip()

item_price = soup.find("span", class_ = 'common-text titleM c-green').text.strip()
item_link = soup.find("a", class_ = 'link product-card horizontal')["href"]

print(item_name)
print(item_price)
print("auto.ria.com" +  item_link)