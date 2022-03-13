#Install and import of all necessary libraries and packages
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import sqlite3
import investpy

#Searching for current palm oil price in MYR
#Checking a scraping permission
url1 = 'https://markets.businessinsider.com/commodities/palm-oil-price'
response1 = requests.get(url1)
print("Status is", response1.status_code)
if response1.status_code == 200:
    print("You can scrape this url")
else:
    print("You can't scrape this url")

#Define the request.get function into text
pages1 = requests.get(url1)
pages1.text

#Use a parser to make text more readable
soup1 = BeautifulSoup(pages1.text, 'lxml')
soup1
soup1.find('span', class_= 'price-section__current-value')
price1 = soup1.find('span', class_ = 'price-section__current-value')
price1.text
float(price1.text)

#Searching for current zinc price in USD
#Checking a scraping permission
url2 = 'https://markets.businessinsider.com/commodities/zinc-price'
response2 = requests.get(url2)
print("Status is", response2.status_code)
if response2.status_code == 200:
    print("You can scrape this url")
else:
    print("You can't scrape this url")

#Define the request.get function into text
pages2 = requests.get(url2)
pages2.text

#Use a parser to make text more readable
soup2 = BeautifulSoup(pages2.text, 'lxml')
soup2
soup2.find('span', class_= 'price-section__current-value')
price2 = soup2.find('span', class_ = 'price-section__current-value')
price2.text
float(price2.text)

#Searching for current MYR/USD exchange rate
#Checking a scraping permission
url3 = 'https://markets.businessinsider.com/currencies/usd-myr'
response3 = requests.get(url3)
print("Status is", response3.status_code)
if response3.status_code == 200:
    print("You can scrape this url")
else:
    print("You can't scrape this url")

#Define the request.get function into text
pages3 = requests.get(url3)
pages3.text

# Use a parser to make text more readable
soup3 = BeautifulSoup(pages3.text, 'lxml')
soup3
soup3.find('span', class_= 'price-section__current-value')
price3 = soup3.find('span', class_ = 'price-section__current-value')
price3.text
float(price3.text)

#Searching for current RUB/USD exchange rate
#Checking a scraping permission
url4 = 'https://markets.businessinsider.com/currencies/rub-usd'
response4 = requests.get(url4)
print("Status is", response4.status_code)
if response4.status_code == 200:
    print("You can scrape this url")
else:
    print("You can't scrape this url")

#Define the request.get function into text
pages4 = requests.get(url4)
pages4.text

# Use a parser to make text more readable
soup4 = BeautifulSoup(pages4.text, 'lxml')
soup4
soup4.find('span', class_= 'price-section__current-value')
price4 = soup4.find('span', class_ = 'price-section__current-value')
price4.text
float(price4.text)

#Searching for current Freightos Baltic Index (FBX): Global Container Freight Index
#Checking a scraping permission
url5 = 'https://en.macromicro.me/charts/35158/fbx-global-container-index'
response5 = requests.get(url5)
print("Status is", response5.status_code)
if response5.status_code == 200:
    print("You can scrape this url")
else:
    print("You can't scrape this url")

#Define the request.get function into text
pages5 = requests.get(url5)
pages5.text

#Use a parser to make text more readable
soup5 = BeautifulSoup(pages5.text, 'lxml')
soup5
soup5.find('span', class_= 'val')
price5 = soup5.find('span', class_ = 'val')
price5.text
float(price5.text.replace(',',''))

#Zinc stearate price calculation
z=(((float(price1.text)/float(price3.text)+50+float(price5.text.replace(',',''))/28)*1.36*17.984+float(price2.text)*1.15*2.736)/20+20000*float(price4.text))*1.2
z0=str(round(z,2))
print("Zinc stearate price in USD is", z0)

#Create SQLite database
conn = sqlite3.connect('znst2.sqlite')
c = conn.cursor()

#Scrape historical data for palm oil price in INR and put them in SQLite database
df1 = investpy.get_commodity_historical_data(commodity='MCX Crude Palm Oil',
from_date='01/01/2020',
to_date='31/12/2022')
df1.to_sql('CPO', conn)

#Scrape historical data for zinc price in USD and put them in SQLite database
df2 = investpy.get_commodity_historical_data(commodity='zinc',
from_date='01/01/2020',
to_date='31/12/2022')
df2.to_sql('ZINC', conn)

#Scrape historical data for USD/INR exchange rate and put them in SQLite database
df3 = investpy.get_currency_cross_historical_data(currency_cross='USD/INR',
from_date='01/01/2020',
to_date='31/12/2022')
df3.to_sql('USDINR', conn)

#Scrape historical data for USD/RUB exchange rate and put them in SQLite database
df4 = investpy.get_currency_cross_historical_data(currency_cross='USD/RUB',
from_date='01/01/2020',
to_date='31/12/2022')
df4.to_sql('USDRUB', conn)

#Scrape historical data for container index and put them in SQLite database
df5 = investpy.indices.get_index_historical_data(index='DJ Containers & Packaging',
country='United States',
from_date='01/01/2020',
to_date='31/12/2022')
df5.to_sql('CONTAINERINDEX', conn)

#Make a price calculation based on historical data and put data in SQLite database  
df6 = (((df1.iloc[:, 0:1]*100/df3.iloc[:, 0:1]+50+df5.iloc[:, 0:1]*0.7)*1.36*17.984+df2.iloc[:, 0:1]*1.15*2.736)/20+20000/df4.iloc[:, 0:1])*1.15
df6.to_sql('ZNST', conn)

#Make a plot of price changes time series
df6.plot()
plt.show()
