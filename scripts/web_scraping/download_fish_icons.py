"""
Download images of all fish
"""

import sqlite3
import requests
from bs4 import BeautifulSoup


result = requests.get("https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)#:~:text=New%20fish%20include%20the%20mahi,Eel%2C%20and%20the%20Rainbow%20Trout.")
src = result.content
soup = BeautifulSoup(src, 'lxml')

all_links = []
table_rows = soup.find_all("tr")[3:83] # get all table rows with the fish info
for table_row in table_rows:
    find_all_td = table_row.find_all("td")
    all_links.append(find_all_td[1].a.img['data-src'])

# for link in all_links:
#     print(link)

# database
conn = sqlite3.connect("../critterpedia.db")
c = conn.cursor()
c.execute("""SELECT * FROM fish""")
all_rows = c.fetchall()
i = 0
for row in all_rows:
    print(all_links[i])
    print(row[0])
    print("\n")
    # c.execute(f"""UPDATE fish SET image = '{all_links[i]}' WHERE name = '{row[0]}'""") # prepare SQL statement
    i += 1

conn.commit() # Commit your changes in the database
