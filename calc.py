# Calculates the cumulative return percentage based on the lowest price of the day and the cost (buy price)
def cumulative_return_pct(lowest_price, buy_price):
    return ((lowest_price - buy_price) / buy_price) * 100

# Calculates the realized return based on the volume-weighted average price of the day and the cost (buy price)
def realized_return_pct(vwap, buy_price):
    return ((vwap - buy_price) / buy_price) * 100

# Calculates the realized return in cash units (HKD, USD) as the minimum of the -5% cutoff value and the vwap return of the day
def realised_return(month, symbol, buy_price, rp, action, first_day_table):
    if action == 'STOPSELL':
        cr = -0.05 * buy_price
        rr = (rp / 100) * buy_price

        return min(cr,rr)
        
    if action == 'SELL':
        sell_price = first_day_table[(first_day_table['MONTH'] == month+1) & (first_day_table['SYMBOL'] == symbol)]['BACK_VWAP'].values[0]
        return (sell_price - buy_price)
        
    # If we hit this part we had an error    
    return 'N/A'