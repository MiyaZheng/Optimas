# main.py
# This is the main script. Run this script to generate the output for the coding task.

import pandas as pd 
import numpy as np 
import time
from datetime import datetime
import os
# Calculations for cumulative return and realised return
import calc
# Helper functions for data manipulation
import helpers

# Config
# Input
PREDICTION_DATA = r'data/prediction_test.csv'
DAILY_DATA = r'data/daily_test.csv'
# Output folder
OUTPUT_DIR = 'output'
# Output file names
DAILY_ACTION_CSV = 'daily_action.csv'
MONTHLY_ACTION_CSV = 'monthly_action.csv'
MONTHLY_PORTFOLIO_RETURN_CSV = 'monthly_portfolio_return.csv'
# Turn off Pandas copy warning
pd.options.mode.chained_assignment = None  # default='warn'

print('Reading data..')

prediction = pd.read_csv(PREDICTION_DATA) 
daily = pd.read_csv(DAILY_DATA)

print('Done.')

print('Processing data..')
uni_date = prediction["DATE"].unique()

top_df = helpers.select_top_instruments(uni_date, prediction)

# Adding a month column for joining later
top_df["MONTH"] = pd.to_datetime(top_df['DATE']).dt.to_period('M')
daily["MONTH"] = pd.to_datetime(daily['DATE']).dt.to_period('M')

# Get table that contains instrument data on the first day of each month
day_1_df = helpers.create_day_1_table(daily)

# Merging the top stocks and daily data into a combined dataframe
combined_df = pd.merge(pd.merge(top_df, day_1_df, on = ["SYMBOL", "MONTH"], how='left'), daily, on = ["SYMBOL", "MONTH"], how='left')
combined_df = combined_df[["MONTH", "DATE", "SYMBOL", "IND_CODE", "BACK_VWAP_x", "BACK_LOW_y", "BACK_VWAP_y"]]
combined_df.rename(columns = {"BACK_VWAP_x": "BUY_PRICE", "BACK_LOW_y": "BACK_LOW", "BACK_VWAP_y": "BACK_VWAP"}, inplace=True)

# Adding a cumulative return and realized return column to the combined dataframe
combined_df['CUM_RETURN (%)'] = combined_df.apply(lambda row: calc.cumulative_return_pct(row['BACK_LOW'], row['BUY_PRICE']), axis=1)
combined_df['REALIZED_PCT (%)'] = combined_df.apply(lambda row: calc.realized_return_pct(row['BACK_VWAP'], row['BUY_PRICE']), axis=1)

print('Done.')

print('Calculating the daily action breakdown for instruments and their realised return for every month..')
# For storing all the monthly and daily data
monthly_action_df =pd.DataFrame()
daily_action_df =pd.DataFrame()

months = combined_df['MONTH'].unique()
for month in months:
    monthly_data = combined_df[combined_df['MONTH'] == month]

    # Create and populate a dictionary where the symbol is the key and the value is a boolean.
    # First, all the values are initialised as False. If an instrument is stop-sold, its corresponding value in the dictionary
    # will be set to True.
    sold_early = {}
    symbols = monthly_data['SYMBOL'].unique()
    last_day = monthly_data['DATE'].tail(1).to_string(index=False).strip()
    for symbol in symbols:
        sold_early[symbol] = False

    # Add a column to show the day-to-day breakdown of what happens to a given instrument
    monthly_data["ACTION"] = monthly_data.apply(lambda x: helpers.get_action(symbol=x['SYMBOL'], cumulative_return=x['CUM_RETURN (%)'], 
    date=x['DATE'], last_day=last_day, sold_early=sold_early), axis=1)

    # Get the final action (SELL or STOPSELL) for every instrument for the given month
    monthly_output_df = monthly_data[monthly_data["ACTION"].isin(["STOPSELL", "SELL"])]

    # Calculate the realized return of every instrument as the minimum of the -5% cutoff and the realized return percentage
    monthly_output_df["REALIZED_RETURN"] = monthly_output_df.apply(lambda row: calc.realised_return(month=row['MONTH'], symbol=row['SYMBOL'], 
    buy_price=row['BUY_PRICE'], rp=row['REALIZED_PCT (%)'], action=row['ACTION'], first_day_table=day_1_df), axis=1)

    # Append the current month to the dataframe
    monthly_action_df = pd.concat([monthly_action_df, monthly_output_df], axis=0, ignore_index=True)
    daily_action_df = pd.concat([daily_action_df, monthly_data], axis=0, ignore_index=True)

new_cols = [col for col in monthly_action_df.columns if col != 'ACTION'] + ['ACTION']
monthly_action_df = monthly_action_df[new_cols]

print('Done')

print('Creating the final portfolio return table..')

# Create the final monthly portfolio return table
portfolio_return_df = pd.DataFrame({"PORTFOLIO_RETURN": monthly_action_df.groupby("MONTH")["REALIZED_RETURN"].agg('sum')})

print('Done.')

print('Writing output as csv files..')

# Output dataframe as csv file
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

daily_action_df.to_csv(OUTPUT_DIR + '/' + DAILY_ACTION_CSV)
monthly_action_df.to_csv(OUTPUT_DIR + '/' + MONTHLY_ACTION_CSV)
portfolio_return_df.to_csv(OUTPUT_DIR + '/' + MONTHLY_PORTFOLIO_RETURN_CSV)

print('Done. \nThe script executed successfully. Check the ' + '\'' + OUTPUT_DIR + '\'' + ' folder for the generated csv files.')








