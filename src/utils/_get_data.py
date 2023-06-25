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
        # Empty list to store the data
        self.dw = DwdWeather(resolution="hourly")
        data = []


        # Get data for each city
        for city, station_id in self.station_ids.items():
            print(f"Getting weather data for {city}...")
            timestamp = self.start
            res = None
            while timestamp <= self.end:
                # Query data for specific station and timestamp
                res = self.dw.query(station_id, timestamp)
                
                # Check if data is not None
                if res is not None:
                    # Add city name, timestamp and weather data to the list
                    row = [city, timestamp] + list(res.values())
                    data.append(row)
                
                # Increment timestamp by one hour
                timestamp += datetime.timedelta(hours=1)

            if res is not None:    
                # Column names: city, timestamp, and weather data keys
                columns = ["City", "Timestamp"] + list(res.keys())
                # Convert the list to a DataFrame
                df = pd.DataFrame(data, columns=columns)
                # Pivot the DataFrame
                pivot_df = df.pivot(index='Timestamp', columns='City')
            else:
                pivot_df = pd.DataFrame()

        return pivot_df

    def _get_weather_data_from_file(self, weather_data_path):
        '''
        
        1) Air Temperature: Temperature has a direct effect on electricity demand. 
            High temperatures can lead to increased air conditioning use, while low temperatures can increase heating demand.
        2) Wind Speed: Wind speed can affect the generation of wind power. 
            Higher wind speeds generally lead to more wind power generation, which can lower electricity prices.
        3) Visibility: Poor visibility could indicate weather conditions like fog or heavy precipitation, 
            which might impact solar power generation.
        4) Wind Direction: This could impact wind power generation, 
            although its impact may not be as substantial as wind speed.
        '''

        df = pd.read_csv(weather_data_path, index_col=0, parse_dates=True)
        # relevant_columns = [
        #     'air_temperature_200', 'visibility_value', 'wind_speed', 'wind_direction',
        #     'air_temperature_200.1', 'visibility_value.1', 'wind_speed.1', 'wind_direction.1',
        #     'air_temperature_200.2', 'visibility_value.2', 'wind_speed.2', 'wind_direction.2'
        # ]

        # relevant_columns = [
        #     'air_temperature_200', 'air_temperature_200.1', 'air_temperature_200.2',
        #     'relative_humidity_200', 'relative_humidity_200.1', 'relative_humidity_200.2',
        #     'cloudiness_total_cover', 'cloudiness_total_cover.1', 'cloudiness_total_cover.2',
        #     'sun_duration', 'sun_duration.1', 'sun_duration.2',
        #     'visibility_value', 'visibility_value.1', 'visibility_value.2',
        #     'wind_speed', 'wind_speed.1', 'wind_speed.2',
        #     'wind_direction', 'wind_direction.1', 'wind_direction.2',
        #     'pressure_msl', 'pressure_msl.1', 'pressure_msl.2'
        # ]

        # df = df[relevant_columns]
        df = df.iloc[2:]
        # Rename columns for clarity
        # df.columns = ['air_temperature_berlin', 'visibility_berlin', 'wind_speed_berlin', 'wind_direction_berlin',
        #             'air_temperature_frankfurt', 'visibility_frankfurt', 'wind_speed_frankfurt', 'wind_direction_frankfurt',
        #             'air_temperature_munich', 'visibility_munich', 'wind_speed_munich', 'wind_direction_munich']

        # conver all .1 to 

        # df.columns = ['air_temperature_berlin', 'air_temperature_frankfurt', 'air_temperature_munich',
        #             'relative_humidity_berlin', 'relative_humidity_frankfurt', 'relative_humidity_munich',
        #             'cloudiness_total_cover_berlin', 'cloudiness_total_cover_frankfurt', 'cloudiness_total_cover_munich',
        #             'sun_duration_berlin', 'sun_duration_frankfurt', 'sun_duration_munich',
        #             'visibility_berlin', 'visibility_frankfurt', 'visibility_munich',
        #             'wind_speed_berlin', 'wind_speed_frankfurt', 'wind_speed_munich',
        #             'wind_direction_berlin', 'wind_direction_frankfurt', 'wind_direction_munich',
        #             'pressure_msl_berlin', 'pressure_msl_frankfurt', 'pressure_msl_munich']
        

        df.index = pd.DatetimeIndex(df.index).tz_localize('Europe/Berlin', nonexistent='shift_forward')
        df = df.astype(float)
        cities = list(self.station_ids.keys())

        # Create a list to hold the dataframes
        dfs = []

        for city in cities:
            # Subset df for each city
            df_temp = df[[col for col in df.columns if city in col]].copy()

            # Rename columns to remove city names
            df_temp.columns = [col.replace(f'_{city}','') for col in df_temp.columns]
            
            # Add a 'city' column
            df_temp['city'] = city
            
            # Add the temporary df to the list of dataframes
            dfs.append(df_temp)

        # Concatenate all the dataframes in the list
        # The keys argument will create a multi-index, where the first level of the index is the city and the second level is the original timestamp index
        df_melted = pd.concat(dfs)

        # Reset the index to make 'city' a column, while keeping timestamp as index
        #df_melted.reset_index(level=0, inplace=True)
    
        
        return df_melted

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
        elif data_name == 'weather_data_from_file':
            #data = pd.read_csv('/home/mamur/EON/forecast-electricity-prices/src/data/weather_data.csv', index_col=0, parse_dates=True)
            #data = self._get_weather_data()
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