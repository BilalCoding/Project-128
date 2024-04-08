from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

time.sleep(10)

scraped_data = []

def scrape_data():
        page = requests.get(START_URL)
        soup = BeautifulSoup(page.content, "html.parser")

        dwarf_star_table = soup.find("table", attrs={"class", "wikitable"})
        temp_list = []
        table_body = dwarf_star_table.find("tbody")
        table_rows = table_body.find_all("tr")

        for row in table_rows:
            table_cols = row.find_all('td')

            for col_data in table_cols:
                data = col_data.text.strip()
                temp_list.append(data)

            scraped_data.append(temp_list)
            print(scraped_data)

scrape_data()

final_data = []

for i in range(0, len(scraped_data)):
    names = scraped_data[i][0]
    distance = scraped_data[i][5]
    mass = scraped_data[i][8]
    radius = scraped_data[i][9]

    required_data = [names, distance, mass, radius]
    final_data.append(required_data)

print(final_data)

headers = ['Name', 'Distance', 'Mass', 'Radius']  
dwarf_star_df = pd.DataFrame(final_data, columns=headers)
dwarf_star_df.to_csv('scraped_data.csv', index=True, index_label="id")