import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("https://listwithclever.com/research/best-taco-cities-2022/")
soup = BeautifulSoup(page.content, 'html.parser')

# Obtain information from tag <table>
tables = soup.find_all('table')
tacoTable=tables[2]
# print(tacoTable)

# Obtain every title of columns with tag <th>
headers = []
for i in tacoTable.find_all('strong'):
    title = i.text
    if title=="-":
        break
    headers.append(title)
# print(headers)

# Create a dataframe
tacoDF = pd.DataFrame(columns = headers)

# Create a for loop to fill mydata
for j in tacoTable.find_all('tr')[2:]:
    row_data = j.find_all('td')
#     print(len(row_data))
    if len(row_data)!=8:
        continue
    row = [i.text for i in row_data]
    length = len(tacoDF)
    tacoDF.loc[length] = row

#split city,state column into separate columns
tacoDF[['City', 'State']] = tacoDF['State'].str.split(',', expand=True)

# send df to csv for later use
tacoDF.to_csv('tacoRate.csv')