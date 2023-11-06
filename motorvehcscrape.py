import requests
from bs4 import BeautifulSoup
import time
import csv

def commastr_to_int(val):
    return int(val.replace(',', ''))

data_list = []

for year in range(1999, 2023):
    print(year)
    url = f'https://www.oica.net/category/production-statistics/{year}-statistics/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    rows = soup.find_all('tr', class_=['row-19 odd', 'row-31 odd'])
    if year >= 2019:
        rows = soup.find_all('tr', class_=['row-18 even', 'row-30 even'])


    for i in rows:
        country = i.find('td', class_='column-1').text
        cars = commastr_to_int(i.find('td', class_='column-2').text)
        commercial_vehicles = commastr_to_int(i.find('td', class_='column-3').text)
        total = commastr_to_int(i.find('td', class_='column-4').text)
        
        # Store the data
        data = {
            'Year': year,
            'Country': country,
            'Cars': cars,
            'Commercial Vehicles': commercial_vehicles,
            'Total': total,
        }
        data_list.append(data)

    time.sleep(0.1)

headers = ['Year', 'Country', 'Cars', 'Commercial Vehicles', 'Total']

with open('vehicle_production.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)
