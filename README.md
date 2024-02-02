# Day Ahead Electricity Price Forecasting

## Background
You are in control of a fleet of batteries and wish to operate the batteries in the optimal way to make a profit. As part of your operations, it is ideal if
you can predict the day ahead electricity prices before they are published. Day-ahead electricity prices in Europe are the prices at which electricity is
bought and sold a day before it is actually consumed. These prices help market participants plan their electricity production and consumption based on
anticipated supply and demand, as well as other factors like weather conditions and regulations.
Day-ahead electricity prices for day D, are determined through an auction process and are typically published on the previous day, D-1. The prices are
usually made available around midday to provide market participants with sufficient time to plan their electricity activities for the upcoming day.
By predicting the day-ahead electricity prices before the auction takes place you can gain an advantage. It would enable you to make informed
decisions regarding trading strategies, potentially leading to improved profitability and better utilization of your battery fleet.

## Modeling Task

Our task is to develop a predictive model that forecasts day-ahead electricity prices in the Germany -LU region. The model should utilize historical
data and weather information.
You can access get data about prices, energy production and consumption from the ENTSOE transparency https://transparency.entsoe.eu/
The data can be accessed through this python library: https://pypi.org/project/entsoe-py/0.2.2/ and the provided token.
From the ENTSOE website you will have access to:
Actual load data, Load forecast data, Actual generation data, Generation forecast data, Wind and solar generation forecast
When predicting the day ahead prices for day D, only the actual load and generation data for day D-2, will be available, this should be taken into
account during pre-processing. The available load and generation forecast will include values up to day D. The ENTSOE service contains many
different data columns. For this task only use load and generation data, ignore transmission, etc.
You should use data from 01.01.2023 to up and including the 01.06.23 for training and validation.
Weather data for Berlin, Frankfurt and Munich can also be used in the models, it can accessed with https://pypi.org/project/dwdweather2/ or
alternative.