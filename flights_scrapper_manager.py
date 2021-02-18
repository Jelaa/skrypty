from kayak_flights_scrapper import *
from momondo_flights_scrapper import *
from excel_manager import *

type_list, depart_city_list, dest_city_list, \
depart_date_list, days_list = get_planned_flights_from_xlsx()
flight_kayak_list = []
flight_momondo_list = []
agents = ["Firefox/66.0.3", "Chrome/73.0.3683.68", "Edge/16.16299"]


for flight in range(len(type_list)):
    agent = agents[(flight % len(agents))]
    if type_list[flight] == 'ONE_WAY':
        #print(type_list[flight])
        flight_kayak = kayak_flights_search_oneway(depart_city_list[flight], dest_city_list[flight],
                                                   depart_date_list[flight], agent)

        flight_momondo = momondo_flights_search_oneway(depart_city_list[flight], dest_city_list[flight],
                                                       depart_date_list[flight], agent)
        flight_kayak_list.append(flight_kayak)
        flight_momondo_list.append(flight_momondo)
    else:
        flight_kayak = kayak_flights_search_return(depart_city_list[flight], dest_city_list[flight],
                                                   depart_date_list[flight], days_list[flight], agent)

        flight_momondo = momondo_flights_search_return(depart_city_list[flight], dest_city_list[flight],
                                                       depart_date_list[flight], days_list[flight], agent)
        flight_kayak_list.append(flight_kayak)
        flight_momondo_list.append(flight_momondo)

save_flight_to_xlsx_sheet(flight_kayak_list, flight_momondo_list, depart_city_list, dest_city_list)
