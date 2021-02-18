from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup as soup
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import time
import re

airports = {
    "Warszawa": "WAW",
    "Krakow": "KRK",
    "Katowice": "KAT",
    "Gdansk": "GDN",
    "Moskwa": "MOW",
    "Londyn": "LON",
    "Paryz": "PAR",
    "Amsterdam": "AMS",
    "Frankfurt": "FRA",
    "Mallorca": "PMI",
    "Madryt": "MAD",
    "Mediolan": "MIL",
    "Petersburg": "LED",
    "Rzym": "ROM",
    "Monachium": "MUC",
    "Ateny": "ATH",
    "Dublin": "DUB",
    "Berlin": "BER",
    "Teneryfa": "TCI",
    "Wieden": "VIE",
    "Malaga": "AGP",
    "Zurych": "ZRH",
    "Sztokholm": "STO",
    "Bruksela": "BRU",
    "Hamburg": "HAM",
    "Edynburg": "EDI",
    "Lizbona": "LIS",
    "Wenecja": "VCE",
    "Lyon": "LYS"
}


def find_airport(city):
    if city not in airports.keys():
        print("There is no " + city + " "
              + "ariport in data base")
        return 0
    else:
        return 1


def find_anywhere():
    all_airports = []
    for aiport in airports:
        all_airports.append(airports[aiport])
    return all_airports


def look_up_flights(departure_city, arrival_city, departure_date, visit_days, requests):
    global results

    end_date = datetime.strptime(departure_date, '%Y-%m-%d').date() + timedelta(visit_days)
    end_date = end_date.strftime('%Y-%m-%d')

    #url = "https://www.kayak.com/flights/" + departure_city + "-" + destination + "/" + departure_date \
    #      + "/" + end_date + "?sort=bestflight_a&fs=stops=0"

    url = "https://www.momondo.pl/flight-search/" + departure_city + "-" + arrival_city + "/" + departure_date \
          + "/" + end_date + "?sort=bestflight_a"

    chrome_options = webdriver.ChromeOptions()
    agents = ["Firefox/66.0.3", "Chrome/73.0.3683.68", "Edge/16.16299"]
    print("User agent: " + agents[(requests % len(agents))])
    chrome_options.add_argument('--user-agent=' + agents[(requests % len(agents))] + '"')
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome("C:/Users/aleks/Python/data_scrapper/venv/Scripts/chromedriver.exe",
                              options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    driver.implicitly_wait(20)
    driver.get(url)

    # Check if Kayak thinks that we're a bot
    time.sleep(5)
    flights_page = soup(driver.page_source, "html.parser")

    if flights_page.find_all('p')[0].getText() == "Please confirm that you are a real KAYAK user.":
        print("Kayak knows I'm a bot, so let's wait a bit and try again")
        driver.close()
        time.sleep(20)
        return "fail"

    time.sleep(20)  # wait 20s for page to load
    flights_page = soup(driver.page_source, "html.parser")

    departure_times = flights_page.find_all('span', attrs={'class': 'depart-time base-time'})
    arrival_times = flights_page.find_all('span', attrs={'class': 'arrival-time base-time'})
    meridies_times = flights_page.find_all('span', attrs={'class': 'time-meridiem meridiem'})
    price_list = flights_page.find_all('div', attrs={'class': re.compile(
        'Common-Booking-MultiBookProvider (.*)multi-row Theme-featured-large')})

    departure_time = []

    for div in departure_times:
        departure_time.append(div.getText()[:-1])

    arrival_time = []

    for div in arrival_times:
        arrival_time.append(div.getText()[:-1])

    meridies_time = []

    for div in meridies_times:
        meridies_time.append(div.getText())

    price = []
    for div in price_list:
        price.append(int(float(div.a.span.getText().translate({ord('\n'): None})[
                     1:])))

    departure_time = np.asarray(departure_time)
    departure_time = departure_time.reshape(int(len(departure_time) / 2), 2)
    arrival_time = np.asarray(arrival_time)
    arrival_time = arrival_time.reshape(int(len(arrival_time) / 2), 2)
    meridies_time = np.asarray(meridies_time)
    meridies_time = meridies_time.reshape(int(len(meridies_time) / 4), 4)
    price = np.asarray(price)

    df = pd.DataFrame({"departure_city": departure_city,
                       "arrival_city": arrival_city,
                       "departure_date": departure_date,
                       "end_date": end_date,
                       "currency": "USD",
                       "price": price,
                       "deptime_o": [m + str(n) for m, n in zip(departure_time[:, 0], meridies_time[:, 0])],
                       "arrtime_d": [m + str(n) for m, n in zip(arrival_time[:, 0], meridies_time[:, 1])],
                       "deptime_d": [m + str(n) for m, n in zip(departure_time[:, 1], meridies_time[:, 2])],
                       "arrtime_o": [m + str(n) for m, n in zip(arrival_time[:, 1], meridies_time[:, 3])]
                       })

    results = pd.concat([results, df], ignore_index=True, sort=False)

    driver.close()  # close page
    time.sleep(15)  # wait 15s until next request

    return "success"


# Create an empty dataframe
results = pd.DataFrame(columns=['departure_city', 'arrival_city', 'departure_date', 'end_date', 'currency',
                                'price', 'deptime_o', 'arrtime_d' 'deptime_o', 'arrtime_d'])
requests = 0

destinations = input("Enter destinations: ")
if destinations == "anywhere":
    destinations = find_anywhere()

start_dates = ['2021-09-06']

for destination in destinations:
    for start_date in start_dates:
        requests = requests + 1
        while look_up_flights('ZRH', destination, start_date, 3, requests) != "success":
            requests = requests + 1

# find minimum price for each destination-startdate-combination
results_agg = results.groupby(['arrival_city', 'departure_date'])['price'].min().reset_index().rename(
    columns={'min': 'price'})

results.to_csv(r'C:\Users\aleks\Python\data_scrapper\venv\Scripts\flights.csv', header=True)
read_flights = pd.read_csv(r'C:\Users\aleks\Python\data_scrapper\venv\Scripts\flights.csv')
read_flights.to_excel(r'C:\Users\aleks\Python\data_scrapper\venv\Scripts\flights.xlsx', index=None, header=True)

