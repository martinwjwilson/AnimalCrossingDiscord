"""
Populate the critterpedia database from the Polygon website
"""

import sqlite3
import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.polygon.com/animal-crossing-new-horizons-switch-acnh-guide/2020/3/23/21190775/fish-locations-times-month-day-list-critterpedia")
src = result.content
soup = BeautifulSoup(src, 'lxml')

# get all fish
rows = soup.find_all("tr")[2:] # get all rows
all_fish = []
for row in rows:
    all_fish.append(row.find_all("td")) # add each row to list of fish

# print out information on each fish
for fish in all_fish:
    print(f"Name: {fish[1].text}")
    print(f"Location: {fish[2].text}")
    print(f"Size: {fish[3].text}")
    print(f"Value: {fish[4].text}")
    print(f"Time: {fish[5].text}")
    print(f"Month: {fish[6].text}")
    print("\n")
