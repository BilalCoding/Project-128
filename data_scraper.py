# Importing libraries
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# URL of the dwarf planets wikipage
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Halting the program for 10 seconds so that the web browser can load
time.sleep(5)

# Creating an empty list which will hold the data scraped from the wikipage
scraped_data = []

# Function to scrape the data from the wikipage
def scrape_data():
        # Sending a request to open the wikipage
        page = requests.get(START_URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # Finding the tables and storing all the rows' data into table_rows
        dwarf_star_table = soup.find("table", attrs={"class", "wikitable"})
        table_body = dwarf_star_table.find("tbody")
        table_rows = table_body.find_all("tr")

        # Finding the column data in each row
        for row in table_rows:
            table_cols = row.find_all('td')
            # Creating a temporary list to store the column data of one row
            temp_list = []

            # Formatting the column data to be appended into the temp_list
            for col_data in table_cols:
                data = col_data.text.strip()
                temp_list.append(data)

            # Appending the column data of one row into the scraped_data list
            scraped_data.append(temp_list)

# Calling the scrape_data function
scrape_data()

# Creating a list to store the useful data
final_data = []

# Iterating through each dwarf star and storing its name, distance, mass and radius
# If the value is missing, the value stored would be "NaN"
for dwarf_star_data in scraped_data:
    try:
        names = dwarf_star_data[0]
    except:
        names = "NaN"
    try:
        distance = dwarf_star_data[5]
    except:
        distance = "NaN"
    try:
        mass = dwarf_star_data[8]
    except:
        mass = "NaN"
    try:
        radius = dwarf_star_data[9]
    except:
        radius = "NaN"
    
    # Creating a list to store the values of one dwarf star to be appended to the final_data list
    required_data = [names, distance, mass, radius]
    final_data.append(required_data)

# The final data list would be a 2D array
print(final_data)

# Creating a CSV file to store the final_data list
headers = ['Name', 'Distance', 'Mass', 'Radius']  
dwarf_star_df = pd.DataFrame(final_data, columns=headers)
dwarf_star_df.to_csv('scraped_data.csv', index=True, index_label="id")
