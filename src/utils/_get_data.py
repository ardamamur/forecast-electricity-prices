from entsoe import EntsoePandasClient
from dwdweather import DwdWeather
import datetime
import pandas as pd


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



    def _set_station(self, station_ids):
        self.station_ids = station_ids

    def _set_dates(self, start, end):
        self.start = start
        self.end = end
    
    def _set_country_code(self, country_code):
        self.country_code = country_code

    def _get_weather_data_from_api(self):
        '''
        Get weather data from DWD
        '''
        raise Exception('Not implemented yet')

    def _get_weather_data_from_file(self):
        '''
        https://open-meteo.com/
        I used the above website to get the weather data for the cities. Currently,
        I downladed the data manually from the webapp. I will automate this process
        later.
        '''

        df_berlin = pd.read_csv("src/data/berlin.csv")
        df_frankfurt = pd.read_csv("src/data/frankfurt.csv")
        df_munich = pd.read_csv("src/data/munich.csv")

        df_dict = {
            'berlin': df_berlin,
            'frankfurt': df_frankfurt,
            'munich': df_munich
        }

        for city, df in df_dict.items():
            df['city_name'] = city  # add a new column with city name
        # use pd.concat to combine the dataframes
        combined_df = pd.concat(df_dict.values(), ignore_index=True)
        return combined_df


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
        elif data_name == 'weather_data':
            data = self._get_weather_data_from_file()
        elif data_name == 'weather_data_from_api':
            data = self._get_weather_data_from_api()
        else:
            raise Exception('Data name is not correct/not available')
    
        #data = pd.to_datetime(data.index)
        return data

    def _resample_data(self, data, freq):
        '''
        Resample the data
        '''
        # Resample the data
        data = data.resample(freq).mean()
        return data

    def _remove_data_from_dict(self, data_dict, data_name):
        '''
        Remove data from dictionary
        '''
        # Remove data from dictionary
        data_dict.pop(data_name)
        return data_dict

    def _lag_dataframe(self, data, lag):
        '''
        Lag the data
        '''
        # Lag the data
        data = data.shift(lag)
        return data