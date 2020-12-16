import pandas as pd 

# Helper function to select the top 10 instruments for each month. 
# For each industry we select at most 3 instruments.
def select_top_instruments(dates, prediction_table):
    top_df = []
    for date in dates:
        df_1 = prediction_table[prediction_table["DATE"] == date].sort_values(["pred_y"], ascending=False)
        df_2 = df_1.groupby("IND_CODE").head(3).reset_index(drop = True)
        df_3 = df_2.head(10).reset_index(drop = True)
        top_df.append(df_3)
    return pd.concat(top_df, axis=0)

# Helper function to create a table that contains the instrument data for every instrument
# on the first day of each month
def create_day_1_table(daily_data_table):
    first_day = daily_data_table.groupby(pd.to_datetime(daily_data_table["DATE"]).dt.to_period('m')).head(1)
    day_list = list(first_day["DATE"])

    return daily_data_table[daily_data_table["DATE"].isin(day_list)]

# Helper function to determine what action to take for a symbol on a given day: keep it (KEEP), sell it on the first day of the 
# next month (SELL), sell it early because it hit the -5% threshold (STOPSELL) or no action is applicable because it has
# already been sold early (X)
def get_action(symbol, cumulative_return, date, first_day, last_day, sold_early):
    if sold_early[symbol]:
        return 'X'
    
    if cumulative_return < -5 and date != first_day:
        sold_early[symbol]= True
        return 'STOPSELL'
    
    if date == last_day:
        return 'SELL'
    
    return 'KEEP'