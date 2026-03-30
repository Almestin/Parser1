from os import link

from bs4 import BeautifulSoup
import requests
start_year = 2020
end_year = 2022
start_price = 1000
end_price = 20000
url = ("https://auto.ria.com/search/?search_type=1&"
       "category=1&all[0].any[0]."
       f"year[0]={start_year}&all[1].any[0]."
       f"year[1]={end_year}"
       "fuel[0]=1&"
       "price[0]=1&"
       f"price[1]={start_price}&"
       f"price[2]={end_price}&"
       "gearbox[0]=1&"
       "abroad=0&"
       "customs_cleared=1")
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

all_names = soup.find_all("div", class_ = 'common-text size-16-20 titleS fw-bold mb-4')
all_prices = soup.find_all("span", class_ = 'common-text titleM c-green')
all_links = soup.find_all("a", class_ = 'link product-card horizontal')

#item_name1 = soup.find("div",class_ = 'common-text size-16-20 titleS fw-bold mb-4').text.strip()
#item_price1 = soup.find("span", class_ = 'common-text titleM c-green').text.strip()
#item_link = soup.find("a", class_ = 'link product-card horizontal')["href"]

#print(item_name1)
#print(item_price)
#print("auto.ria.com" +  item_link)

for item_name, item_price, item_link in zip(all_names, all_prices, all_links):
    print(item_name.text.strip()," / ", item_price.text.strip()," / ", "auto.ria.com" + item_link["href"])