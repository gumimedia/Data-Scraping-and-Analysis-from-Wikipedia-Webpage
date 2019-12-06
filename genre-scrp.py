import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import re
import csv

#command to create a structure of csv file in which we will populate our scraped data
# with open('Opencodez_Articles.csv', mode='w') as csv_file:
#    fieldnames = ['Link', 'Title', 'Genre']
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    writer.writeheader()
#Creating an empty lists of variables
book_link = []
book_title = []
book_genre = []


response = requests.get(
    "https://en.wikipedia.org/wiki/List_of_best-selling_books")
soup = BeautifulSoup(response.text, "html.parser")
new_div = soup.new_tag('div')
new_div.string = "unknown"
tables = soup.find_all("table", class_="wikitable sortable")

data = []

for table in tables:
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all("a")
        data.append([ele['href'] for ele in cols])


#filtering and selecting specific data
dataf = list(filter(None, data[:103]))
for datalink in dataf:
    book_link.append(datalink[0])

# print(book_link)


def bookid(webpage, bookslink):
    for j in bookslink:
        book_page = webpage + j
        response = requests.get(book_page)
        soup = BeautifulSoup(response.content, "html.parser")
        soup_title = soup.find_all("h1", {"class": "firstHeading"})
        l_gen = []
        tabs = soup.find_all("table", {"class": "infobox"})
        for tab in tabs:
            links = tab.find_all(lambda tag:tag.name=="th" and "Genre" in tag.text)
            for lin in links:
                l_gen.append(lin.next_sibling)
        list_gen = []
        for st in soup_title:
           book_title.append(st.text)
        list_gen.append(l_gen)
        for div in list_gen:
            if len(div)==0:
                div.append(new_div)
            for eldiv in div:
                book_genre.append(eldiv.text)

bookid("https://en.wikipedia.org", book_link)
dataframes = []
for comb in range(len(book_link)):
    dframe = []
    dframe.append(book_link[comb])
    dframe.append(book_title[comb])
    dframe.append(book_genre[comb])
    dataframes.append(dframe)

dtf = pd.DataFrame(dataframes, columns=["Book Link", "Book Title", "Genre"])
dtf['Genre'] = dtf['Genre'].str.replace(r"\n", ", ")
dtf['Genre'] = [x.lstrip(',\n').rstrip(' \n[]12,') for x in dtf['Genre']]


print(dtf)
# print(len(book_link))
# print(len(book_title))


export_csv = dtf.to_csv(r'wikigenre.csv', sep='\t', header=True, index=0)
