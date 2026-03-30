from bs4 import BeautifulSoup
import requests
import csv
import random
import time
import pandas as pd
import openpyxl

data = []


def check_input_data(input_message, error_message, start_range, end_range, default_value):
    while True:
        input_data = input(input_message).strip()
        if not input_data:
            return default_value
            break
        try:
            if start_range <= (value := int(input_data)) <= end_range:
                result = int(value)
                return result
                break

        except ValueError:
            pass

        print(error_message)


print("Enter search data")
print("#" * 100)
start_year = check_input_data("Minimum year of vehicle production (1900-2026): ", "Enter a valid year!", 1900, 2026,
                              1900)
end_year = check_input_data("Maximum year of vehicle production (1900-2026): ", "Enter a valid year!", 1900, 2026, 2026)
start_price = check_input_data("Minimum price (>0): ", "Enter a valid price!", 0, 100000, 1)
end_price = check_input_data("Maximum price (1-100000000): ", "Enter a valid price!", 0, 100000000, 1)

url_rio = ("https://auto.ria.com/search/?search_type=1&"
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def parse_rio(url, last_page=10):
    for page in range(1, last_page + 1):
        url = f"{url}&p={page}"
        print(f"Parsing page: {page}")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        all_names = soup.find_all("div", class_='common-text size-16-20 titleS fw-bold mb-4')
        all_prices = soup.find_all("span", class_='common-text titleM c-green')
        all_links = soup.find_all("a", class_='link product-card horizontal')

        for item_name, item_price, item_link in zip(all_names, all_prices, all_links):
            print(item_name.text.strip(), " | ", item_price.text.strip(), " | ", "auto.ria.com" + item_link["href"])

        print("_" * 100)

        for item_name, item_price, item_link in zip(all_names, all_prices, all_links):
            data.append([item_name.text.strip(), item_price.text.strip(), "auto.ria.com" + item_link["href"]])

        time.sleep(random.randint(1, 6))
    return data


print("#" * 100)

parse_rio(url_rio, 3)

with open('data_output.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerows(data)

df = pd.DataFrame(data)
df.to_excel('data_output.xlsx', index=False, sheet_name="Parsing_from_AutoRio")
