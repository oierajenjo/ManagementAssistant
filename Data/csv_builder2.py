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
html = open(file, 'r', encoding='utf-8').read()
# print(html)
# soup = BeautifulSoup(html, "html.parser")

data = {}
soup = BeautifulSoup(html, "lxml")
table = soup.find("table", attrs={"id": "opTableDetalle"})
table_filtered = table.tbody.find_all("tr")


# Get all the headings of Lists
headings = []

for td in table_filtered[0].find_all("td"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.b.text.replace('\n', ' ').strip())

# Get all the tables contained in "gdp_table"
for table, heading in zip(table_filtered[1].find_all("table"), headings):
    # Get headers of table i.e., Rank, Country, GDP.
    t_headers = []
    for th in table.find_all("th"):
        # remove any newlines and extra spaces from left and right
        t_headers.append(th.text.replace('\n', ' ').strip())

    # Get all the rows of table
    table_data = []
    for tr in table.tbody.find_all("tr"):  # find all tr's from table's tbody
        t_row = {}
        # Each table row is stored in the form of
        # t_row = {'Rank': '', 'Country/Territory': '', 'GDP(US$million)': ''}

        # find all td's(3) in tr and zip it with t_header
        for td, th in zip(tr.find_all("td"), t_headers):
            t_row[th] = td.text.replace('\n', '').strip()
        table_data.append(t_row)

    # Put the data for the table with his heading.
    data[heading] = table_data


# Step 4: Export the data to csv
for topic, table in data.items():
    # Create csv file for each table
    with open(f"{topic}.csv", 'w') as out_file:
        headers = [
            "",
            "",
            "Ventas",
            "",
            "",
            "Cancelaciones",
            "",
            ""
        ]  # == t_headers
        writer = csv.DictWriter(out_file, headers)
        writer.writeheader()
        headers = [
            "Día",
            "Juego",
            "Importe",
            "Trans.",
            "Apuestas",
            "Importe",
            "Trans.",
            "Apuestas"
        ]  # == t_headers
        writer = csv.DictWriter(out_file, headers)
        # write the header
        writer.writeheader()
        for row in table:
            if row:
                writer.writerow(row)






# Step 4: Export the data to csv
"""
For this example let's create 3 seperate csv for 
3 tables respectively
"""
for topic, table in data.items():
    # Create csv file for each table
    with open(f"{topic}.csv", 'w') as out_file:
        # Each 3 table has headers as following
        headers = [
            "Country/Territory",
            "GDP(US$million)",
            "Rank"
        ]  # == t_headers
        writer = csv.DictWriter(out_file, headers)
        # write the header
        writer.writeheader()
        for row in table:
            if row:
                writer.writerow(row)









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
