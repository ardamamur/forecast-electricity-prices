from entsoe import EntsoePandasClient
import pandas as pd
import argparse
import os

class DataHandler:
    def __init__(self) -> None:
        '''
        Initialize the DataHandler class
        '''
        self.api_key = '1134c6e2-51f3-419f-bd6d-189faec8df3f'
        self.client = EntsoePandasClient(api_key=self.api_key)

        self.series_data_columns = {
            'day_ahead_prices': 'day_ahead_price',
            'generation_forecast': 'forecasted_generation',
        }

    def _set_data_settings(self, country_code, start, end):
        self.country_code = country_code
        self.start = start
        self.end = end

    def _get_data(self, data_name):

        '''
        Get data from ENTSOE
        '''
        # Based on the data_name, get the data from ENTSOE, by using switch case
        '''
        Available data:
            load_data = client.query_load(country_code, start=start_date,end=end_date)
            load_forecast = client.query_load_forecast(country_code, start=start_date,end=end_date)
            generation_data = client.query_generation(country_code, start=start_date,end=end_date)
            generation_forecast = client.query_generation_forecast(country_code, start=start_date,end=end_date)
            wind_and_solar_forecast = client.query_wind_and_solar_forecast(country_code, start=start_date,end=end_date)
            day_ahead_prices = client.query_day_ahead_prices(country_code, start=start_date,end=end_date)
        '''

        # load data by using switch case

        if data_name == 'load_data':
            data = self.client.query_load(self.country_code, start=self.start,end=self.end)
        elif data_name == 'load_forecast':
            data = self.client.query_load_forecast(self.country_code, start=self.start,end=self.end)
        elif data_name == 'generation_data':
            data = self.client.query_generation(self.country_code, start=self.start,end=self.end)
        elif data_name == 'generation_forecast':
            data = self.client.query_generation_forecast(self.country_code, start=self.start,end=self.end)
            data = data.to_frame()
            data.columns = [self.series_data_columns[data_name]]
        elif data_name == 'wind_and_solar_forecast':
            data = self.client.query_wind_and_solar_forecast(self.country_code, start=self.start,end=self.end)
        elif data_name == 'day_ahead_prices':
            data = self.client.query_day_ahead_prices(self.country_code, start=self.start,end=self.end)
            data = data.to_frame()
            data.columns = [self.series_data_columns[data_name]]
        else:
            raise Exception('Data name is not correct/not available')
    
        #data = pd.to_datetime(data.index)
        return data



