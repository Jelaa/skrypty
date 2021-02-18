import pandas as pd


def get_planned_flights_from_xlsx():
    df_planned_flights = pd.read_excel(r'C:\Users\aleks\Python\data_scrapper'
                                       r'\venv\Scripts\flights_planner.xlsx',
                                       converters={'DEPART_DATE': str})

    type_list = df_planned_flights['TYPE'].tolist()
    depart_city_list = df_planned_flights['DEPART_CITY'].tolist()
    dest_city_list = df_planned_flights['DEST_CITY'].tolist()
    depart_date_list = df_planned_flights['DEPART_DATE'].tolist()
    for n in range(len(depart_date_list)):
        depart_date_list[n] = depart_date_list[n][:-9]
    days_list = df_planned_flights['DAYS'].tolist()
    return type_list, depart_city_list, dest_city_list, \
           depart_date_list, days_list


def get_number_of_flights(df_planned_flights):
    index = df_planned_flights.index
    flights_number = len(index)
    return flights_number


def creat_sheet_in_xlsx_file():
    writer = pd.ExcelWriter('found_flights.xlsx', engine='xlsxwriter')


def save_flight_to_xlsx_sheet(df_kayak_list, df_momondo_list, depart_city_list, dest_city_list):
    path = r'C:\Users\aleks\Python\data_scrapper\venv\Scripts\found_flights.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for flight in range(len(df_kayak_list)):
        print(flight)
        sheet_name = depart_city_list[flight] + '-' + dest_city_list[flight]
        df_kayak_list[flight].to_excel(writer, sheet_name=sheet_name, index=False)
        rows = get_number_of_flights(df_kayak_list[flight])
        df_momondo_list[flight].to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=rows + 1)
    writer.save()

