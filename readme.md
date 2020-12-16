# Running the Script

Just run the main.py file.
The output folder and file names can be changed under the config section of the file.

# Folder Structure
1. data -> Contains the data files for this task
2. output -> It gets generated when the script is executed successfully. Contains the output in csv format (see the "Output csv Files" section)
3. sample_output -> Should the code not work for some reason, I included the output files the code is supposed to generate from earlier runs.

# Output csv Files

## 1. monthly_action
1. This file is about the detailed action of each month
2. The file contains 11 columns: MONTH, DATE, SYMBOL, IND_CODE, BUY_PRICE, BACK_LOW, BACK_VWAP, CUM_RETUN (%), REALIZED_PCT (%), REALIZED_RETURN, ACTION 
2. BUY_PRICE: vwaps of symbols' first day in each month 
3. CUM_RETURN: cumulative return. Formula: (BACK_LOW - BUY_PRICE) / BUY_PRICE
4. REALIZED_PCT: realized percentage. Formula: (BACK_VWAP - BUY_PRICE) / BUY_PRICE
5. ACTION: actions for each symbol. 
    1. STOPSELL: the symbol is triggered by the stop rule (when the cumulative return is below -5%) and sold on the day  
    2. SELL: the symbol is not triggered by the stop rule and sold on the first day of the next month.
 6. REALIZED_RETURN (in cash): 
    1. If the symbol is sold based on the stop rule: the minimum of the -5% cutoff value and the vwap return of the day
    2. If the symbol is sold on the first day of next month: realized return = vwap on the next month's first day - buy price

### 2. daily_action
1. This file contains the detailed action breakdown per instrument for each day
2. The table contains 10 columns: MONTH, DATE, SYMBOL, IND_CODE, BUY_PRICE, BACK_LOW, BACK_VWAP, CUM_RETUN (%), REALIZED_PCT (%), ACTION 
3. ACTION: 
    1. KEEP: we keep the stock on the given day
    2. STOPSELL: as described in monthly_action above
    3. X: used after a STOPSELL. It means that no action is applicable for that day.
    4. SELL: as described in monthly_action above

### 3. portfolio_return
1. The total portfolio return of each month as the sum of all the realised returns for the month.
