from selenium import webdriver
from bs4 import BeautifulSoup as soup
from datetime import date, timedelta, datetime
import requests
import numpy as np
import pandas as pd
import time
import re


def kayak_flights_search_return(departure_city, destination_city, departure_date, days_of_stay, agent):

    return_date = datetime.strptime(departure_date, '%Y-%m-%d').date() + timedelta(days_of_stay)
    return_date = return_date.strftime('%Y-%m-%d')

    url = "https://www.kayak.pl/flights/" + departure_city + "-" + destination_city + "/" + departure_date \
          + "/" + return_date + "?sort=bestflight_a"

    chrome_options = webdriver.ChromeOptions()
    #agents = "Chrome/73.0.3683.68"
    chrome_options.add_argument('--user-agent=' + agent + '"')
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome("C:/Users/aleks/Python/data_scrapper/venv/Scripts/chromedriver.exe",
                              options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    driver.implicitly_wait(20)
    driver.get(url)
    kayak_page = soup(driver.page_source, "html.parser")

    start_flight = kayak_page.body.find_all('li', attrs={'class': 'flight with-gutter'})

    start_departure_time = []
    for li in start_flight:
        div_top = li.find_all('div', attrs={'class': 'top'})
        for div in div_top:
            depart_time_span = div.find_all('span', attrs={'class': 'depart-time base-time'})
            for span in depart_time_span:
                start_departure_time.append(span.getText())

    start_arrival_time = []
    for li in start_flight:
        div_top = li.find_all('div', attrs={'class': 'top'})
        for div in div_top:
            arrival_time_span = div.find_all('span', attrs={'class': 'arrival-time base-time'})
            for span in arrival_time_span:
                start_arrival_time.append(span.getText())

    start_flight_duration_time = []
    for li in start_flight:
        div_duration = li.find_all('div', attrs={'class': 'section duration allow-multi-modal-icons'})
        for div in div_duration:
            start_flight_duration_time.append(div.getText().translate({ord('\n'): None}))

    # start_next_day_arrival = []

    start_changes_number = []
    for li in start_flight:
        span_stops = li.find_all('span', attrs={'class': 'stops-text'})
        for span in span_stops:
            start_changes_number.append(span.getText().translate({ord('\n'): None}))

    start_airlines = []
    for li in start_flight:
        div_carriers = li.find_all('div', attrs={'class': 'leg-carrier'})
        for div in div_carriers:
            img = div.find('img', alt=True)
            start_airlines.append(img['alt'][:-5])

    end_flight = kayak_page.body.find_all(lambda tag: tag.name == 'li' and
                                          tag.get('class') == ['flight'])

    end_departure_time = []
    for li in end_flight:
        div_top = li.find_all('div', attrs={'class': 'top'})
        for div in div_top:
            depart_time_span = div.find_all('span', attrs={'class': 'depart-time base-time'})
            for span in depart_time_span:
                end_departure_time.append(span.getText())

    end_arrival_time = []
    for li in end_flight:
        div_top = li.find_all('div', attrs={'class': 'top'})
        for div in div_top:
            arrival_time_span = div.find_all('span', attrs={'class': 'arrival-time base-time'})
            for span in arrival_time_span:
                end_arrival_time.append(span.getText())

    end_flight_duration_time = []
    for li in end_flight:
        div_duration = li.find_all('div', attrs={'class': 'section duration allow-multi-modal-icons'})
        for div in div_duration:
            end_flight_duration_time.append(div.getText().translate({ord('\n'): None}))

    # end_next_day_arrival = []

    end_changes_number = []
    for li in end_flight:
        span_stops = li.find_all('span', attrs={'class': 'stops-text'})
        for span in span_stops:
            end_changes_number.append(span.getText().translate({ord('\n'): None}))

    end_airlines = []
    for li in end_flight:
        div_carriers = li.find_all('div', attrs={'class': 'leg-carrier'})
        for div in div_carriers:
            img = div.find('img', alt=True)
            end_airlines.append(img['alt'][:-5])

    flight_price = []
    div_price = kayak_page.find_all('div', attrs={'class': 'Flights-Results-FlightPriceSection right-alignment sleek'})
    for div in div_price:
        span_price = div.find_all('span', attrs={'class': 'price-text'})
        for span in span_price:
            flight_price.append(span.getText().translate({ord('\n'): None})[:-4])

    site = []
    for flight in range(len(start_departure_time)):
        site.append('kayak')

    df_kayak = pd.DataFrame({'start_departure_time': start_departure_time, 'start_arrival_time': start_arrival_time,
                               'start_flight_duration_time': start_flight_duration_time, 'start_changes_number':
                               start_changes_number, 'end_departure_time': end_departure_time, 'end_arrival_time':
                               end_arrival_time, 'end_flight_duration_time': end_flight_duration_time,
                               'end_changes_number': end_changes_number, 'flight_price': flight_price, 'site': site})

    return df_kayak


def kayak_flights_search_oneway(departure_city, destination_city, departure_date, agent):

    url = "https://www.kayak.pl/flights/" + departure_city + "-" + destination_city + "/" + departure_date \
          + "?sort=bestflight_a"

    chrome_options = webdriver.ChromeOptions()
    #agents = "Chrome/73.0.3683.68"
    chrome_options.add_argument('--user-agent=' + agent + '"')
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome("C:/Users/aleks/Python/data_scrapper/venv/Scripts/chromedriver.exe",
                              options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    driver.implicitly_wait(20)
    driver.get(url)
    kayak_page = soup(driver.page_source, "html.parser")

    start_flight = kayak_page.body.find_all('li', attrs={'class': 'flight'})

    start_departure_time = []
    for li in start_flight:
        div_top = li.find_all('div', attrs={'class': 'top'})
        for div in div_top:
            depart_time_span = div.find_all('span', attrs={'class': 'depart-time base-time'})
            for span in depart_time_span:
                start_departure_time.append(span.getText())

    start_arrival_time = []
    for li in start_flight:
        div_top = li.find_all('div', attrs={'class': 'top'})
        for div in div_top:
            arrival_time_span = div.find_all('span', attrs={'class': 'arrival-time base-time'})
            for span in arrival_time_span:
                start_arrival_time.append(span.getText())

    start_flight_duration_time = []
    for li in start_flight:
        div_duration = li.find_all('div', attrs={'class': 'section duration allow-multi-modal-icons'})
        for div in div_duration:
            start_flight_duration_time.append(div.getText().translate({ord('\n'): None}))

    # start_next_day_arrival = []

    start_changes_number = []
    for li in start_flight:
        span_stops = li.find_all('span', attrs={'class': 'stops-text'})
        for span in span_stops:
            start_changes_number.append(span.getText().translate({ord('\n'): None}))

    start_airlines = []
    for li in start_flight:
        div_carriers = li.find_all('div', attrs={'class': 'leg-carrier'})
        for div in div_carriers:
            img = div.find('img', alt=True)
            start_airlines.append(img['alt'][:-5])

    flight_price = []
    div_price = kayak_page.find_all('div', attrs={'class': 'Flights-Results-FlightPriceSection right-alignment sleek'})
    for div in div_price:
        span_price = div.find_all('span', attrs={'class': 'price-text'})
        for span in span_price:
            flight_price.append(span.getText().translate({ord('\n'): None})[:-4])

    site = []
    for flight in range(len(start_departure_time)):
        site.append('kayak')

    df_kayak = pd.DataFrame({'start_departure_time': start_departure_time, 'start_arrival_time': start_arrival_time,
                             'start_flight_duration_time': start_flight_duration_time, 'start_changes_number':
                              start_changes_number, 'flight_price': flight_price, 'site': site})

    return df_kayak

