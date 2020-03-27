import os
# from urllib import urlopen
from bs4 import BeautifulSoup

import csv

# path = 'C:\\Users\\ajent\\OneDrive - Universidad de Deusto\\UNI\\ASIGNATURAS\\CURSO5\\CURSO5-2\\TFGII\\Tienda'

files = []
titles = []
# r=root, d=directories, f = files
for r, d, f in os.walk(""):
    for file in f:
        if '.html' in file:
            files.append(os.path.join(r, file))
            titles.append(os.path.splitext(os.path.basename(file))[0])

file = files[0]
print(file)
html = open(file, 'r', encoding='utf-8').read().replace('.', '').replace(',', '.')
# print(html)
soup = BeautifulSoup(html, "html.parser")
# soup = BeautifulSoup(html, "lxml")


table = soup.find("table", attrs={"id": "opTableDetalle"})

############
## HEADER ##
############
headers = table.find("thead").findAll("tr")
headers_all = []
for head in headers:
    header_list = []
    for th in head.findAll(['th', 'td']):
        if th.has_attr("colspan"):
            span = int(th["colspan"])
            header_list.append(th.text.replace('\xa0', ' '))
            for i in range(1, span):
                header_list.append(' ')
        else:
            header_list.append(th.text.replace('\xa0', ' '))
    headers_all.append(header_list)

############
## DATA ##
############
# print(table)
data = table.find("tbody", attrs={"class": "Detalle"})
data_all = []
for tr in data.findAll('tr'):
    data_line = []
    for td in tr.findAll('td'):
        data_line.append(td.text)
    # data_line.append('\n')
    data_all.append(data_line)

# print(data_all)


for title in titles:
    print(title)
    with open(f'{str(title)}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in headers_all:
            writer.writerow(row)
        for row in data_all:
            writer.writerow(row)
        # writer.close()

# header = headers.
# table = soup.find("table")
# print(table)

# # The first tr contains the field names.


# print(headings)
# output_rows = []
# for table_row in table.findAll('tr'):
#     columns = table_row.findAll('td')
#     output_row = []
#     for column in columns:
#         output_row.append(column.text)
#     output_rows.append(output_row)
#
# with open(f'output.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     for row in output_rows:
#         writer.writerow(row)

# # importing the libraries
#
# # Step 3: Analyze the HTML tag, where your content lives
# # Create a data dictionary to store the data.
# data = {}
# # Get the table having the class wikitable
# gdp_table = soup.find("table", attrs={"class": "wikitable"})
# gdp_table_data = gdp_table.tbody.find_all("tr")  # contains 2 rows
#
# # Get all the headings of Lists
# headings = []
# for td in gdp_table_data[0].find_all("td"):
#     # remove any newlines and extra spaces from left and right
#     headings.append(td.b.text.replace('\n', ' ').strip())
#
# # Get all the 3 tables contained in "gdp_table"
# for table, heading in zip(gdp_table_data[1].find_all("table"), headings):
#     # Get headers of table i.e., Rank, Country, GDP.
#     t_headers = []
#     for th in table.find_all("th"):
#         # remove any newlines and extra spaces from left and right
#         t_headers.append(th.text.replace('\n', ' ').strip())
#
#     # Get all the rows of table
#     table_data = []
#     for tr in table.tbody.find_all("tr"):  # find all tr's from table's tbody
#         t_row = {}
#         # Each table row is stored in the form of
#         # t_row = {'Rank': '', 'Country/Territory': '', 'GDP(US$million)': ''}
#
#         # find all td's(3) in tr and zip it with t_header
#         for td, th in zip(tr.find_all("td"), t_headers):
#             t_row[th] = td.text.replace('\n', '').strip()
#         table_data.append(t_row)
#
#     # Put the data for the table with his heading.
#     data[heading] = table_data
#
# # Step 4: Export the data to csv
# """
# For this example let's create 3 seperate csv for
# 3 tables respectively
# """
# for topic, table in data.items():
#     # Create csv file for each table
#     with open(f"{topic}.csv", 'w') as out_file:
#         # Each 3 table has headers as following
#         headers = [
#             "Country/Territory",
#             "GDP(US$million)",
#             "Rank"
#         ]  # == t_headers
#         writer = csv.DictWriter(out_file, headers)
#         # write the header
#         writer.writeheader()
#         for row in table:
#             if row:
#                 writer.writerow(row)


# print(output_rows)
# with open('output.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(output_rows)
#
# datasets = []
# for row in table.find_all("tr")[1:]:
#     dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
#     datasets.append(dataset)
#
# print(datasets)


# for f in files:
#     title = files.
#     print(title)


#     # text = urlopen(f).read()
#     soup = BeautifulSoup(f)
#     table = soup.get_text().find("tbody", attrs={"class": "Detalle"})
#
#     # The first tr contains the field names.
#     headings = [th.get_text() for th in table.find("tr").find_all("th")]
#
#     datasets = []
#     for row in table.find_all("tr")[1:]:
#         dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
#         datasets.append(dataset)
#
#     print(datasets)

# for f in files:
#     print(f)
#
# for t in titles:
#     print(t)
