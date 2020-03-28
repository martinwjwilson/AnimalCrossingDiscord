"""
Populate the critterpedia database from the Polygon website
"""

import sqlite3
import requests
from bs4 import BeautifulSoup

# database
conn = sqlite3.connect("critterpedia.db")
c = conn.cursor()

# result = requests.get("https://www.polygon.com/animal-crossing-new-horizons-switch-acnh-guide/2020/3/23/21190775/fish-locations-times-month-day-list-critterpedia")
# result = requests.get("https://www.polygon.com/animal-crossing-new-horizons-switch-acnh-guide/2020/3/24/21191276/insect-bug-locations-times-month-day-list-critterpedia")
src = result.content
soup = BeautifulSoup(src, 'lxml')


# get all bugs
rows = soup.find_all("tr")[2:] # get all rows
all_bugs = []
for row in rows:
    all_bugs.append(row.find_all("td")) # add each row to list of bugs

# print out information on each bugs
for bug in all_bugs:
    bug_name = bug[1].text
    if "'" in bug_name:
        bug_name = bug_name.replace("'", "!")
    c.execute(f"""INSERT INTO critterpedia
                (name, type, location, value, time, month)
                VALUES ('{bug_name}', 'Bug', '{bug[2].text}', '{bug[3].text}', '{bug[4].text}', '{bug[5].text}');""")
    conn.commit() # Commit your changes in the database
    print(f"Name: {bug[1].text}")
    print("Type: Bug")
    print(f"Location: {bug[2].text}")
    print(f"Value: {bug[3].text}")
    print(f"Time: {bug[4].text}")
    print(f"Month: {bug[5].text}")
    print("\n")


# get all fish
rows = soup.find_all("tr")[2:] # get all rows
all_fish = []
for row in rows:
    all_fish.append(row.find_all("td")) # add each row to list of fish

# print out information on each fish
for fish in all_fish:
    c.execute(f"""INSERT INTO critterpedia
                (name, type, location, size, value, time, month)
                VALUES ('{fish[1].text}', 'Fish', '{fish[2].text}', '{fish[3].text}', '{fish[4].text}', '{fish[5].text}', '{fish[6].text}');""")
    conn.commit() # Commit your changes in the database
    print(f"Name: {fish[1].text}")
    print("Type: Fish")
    print(f"Location: {fish[2].text}")
    print(f"Size: {fish[3].text}")
    print(f"Value: {fish[4].text}")
    print(f"Time: {fish[5].text}")
    print(f"Month: {fish[6].text}")
    print("\n")
