import requests
import os
import pprint
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from api_data import api_data

def get_message_2(ETF_data, ETF):

    message_2 = ""
    significant_price_drop = False

    daily_prices = ETF_data['Time Series (Daily)']
    #daily_prices = ETF_data

    #pprint.pprint(daily_prices)

    all_dates = list(daily_prices.keys()) # List of strings

    # We will be checking if today's current price of an ETF/stock is less than or equal to the lowest closing price of that ETF/stock from the past 3 months
    # We want to send a notification if the current price has reached the lowest it has been in the past 3 months

    # We only want to look at data from the last 3 months
    today = date.today() # Get today's date
    #print(today)
    date_ten_days_ago = today - relativedelta(days=10) # Subtract exactly 3 months
    #print(date_ten_days_ago)

    # Keeping only dates for the last 3 months, but they are originally strings, so we need to convert to objects before we compare
    # Using Python list comprehension (shorter syntax)
    all_dates = [
        d for d in all_dates
        if datetime.strptime(d, '%Y-%m-%d').date() >= date_ten_days_ago
    ]

    #print(all_dates)

    highest_price_date = all_dates[0] # i.e., '2026-09-25'
    highest_price = float(daily_prices[highest_price_date]['4. close']) # i.e., '711.6450'
    for d in all_dates:
        close = float(daily_prices[d]['4. close'])
        if close > highest_price:
            highest_price = close
            highest_price_date = d

    highest_price_date_object = datetime.strptime(highest_price_date, '%Y-%m-%d') # Parse the string into a datetime object
    highest_price_day = int(highest_price_date_object.strftime("%d")) # Remove the zero from before the day
    formatted_highest_price_date = f"{highest_price_date_object:%B} {highest_price_day}, {highest_price_date_object:%Y}"

    print("DATE OF HIGHEST PRICE IN PAST 10 DAYS: " + formatted_highest_price_date)
    message_2 += f"DATE OF HIGHEST PRICE IN PAST 10 DAYS: {formatted_highest_price_date}\n"
    print(f"HIGHEST PRICE: ${highest_price:.2f}")
    message_2 += f"HIGHEST PRICE: ${highest_price:.2f}\n"

    price_now = float(daily_prices[all_dates[0]]['4. close'])
    print(f"PRICE NOW: ${price_now:.2f}")
    message_2 += f"PRICE NOW: ${price_now:.2f}\n"

    dollar_amount_change = highest_price - price_now
    percent_drop = (highest_price - price_now) / highest_price * 100
    print(f"{ETF} dropped by {percent_drop:.2f}% (${dollar_amount_change:.2f}) since {formatted_highest_price_date}.")
    message_2 += f"{ETF} dropped by {percent_drop:.2f}% (${dollar_amount_change:.2f}) since {formatted_highest_price_date}.\n"

    if percent_drop >= 4.0:
        significant_price_drop = True
        message_2 += f"You should buy {ETF} now, as you will be buying at a nice discount!"
        
    return message_2, significant_price_drop