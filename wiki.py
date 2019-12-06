import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


response = requests.get(
    "https://en.wikipedia.org/wiki/List_of_best-selling_books")
soup = BeautifulSoup(response.text, "html.parser")


tables = soup.find_all("table", class_="wikitable sortable")

data = []

for table in tables:
    rows = table.find_all('tr')

    for row in rows:
        for sup in row.find_all('sup'):
            sup.decompose()
        [td.text for td in row('td')]
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
        

#filtering and selecting specific data
dataf = list(filter(None, data[:103]))

# Create the pandas DataFrame
df = pd.DataFrame(dataf, columns=[
                  'Title', 'Author', 'Language', 'Year', 'Approximate Sales', 'Genre'])

# overwriting column for data cleaning
df['Approximate Sales'] = [x.lstrip('–<>').rstrip(' mill copies in USSR U.S.') for x in df['Approximate Sales']]
df['Approximate Sales'] = df['Approximate Sales'].replace('65–150', '150')
df['Approximate Sales'] = df['Approximate Sales'] + '000000'
df['Title'] = df['Title'].str.replace(r"\(.*\)", "")
filter = df['Approximate Sales'] == '150'
df["Genre"].fillna("Unknown", inplace=True)

# printing only filtered columns
df.where(filter).dropna()

print(df)

export_csv = df.to_csv(r'wikidataframe.csv', header=True, index=0)


