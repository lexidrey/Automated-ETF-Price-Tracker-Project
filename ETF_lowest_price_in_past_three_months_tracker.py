import requests
import pprint
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from api_data import api_data

def get_message_1(ETF_data, ETF):

    message_1 = ""
    new_lowest_price = False

    daily_prices = ETF_data['Time Series (Daily)']
    #daily_prices = ETF_data

    #pprint.pprint(daily_prices)

    all_dates = list(daily_prices.keys()) # List of strings

    # We will be checking if today's current price of an ETF/stock is less than or equal to the lowest closing price of that ETF/stock from the past 3 months
    # We want to send a notification if the current price has reached the lowest it has been in the past 3 months

    # We only want to look at data from the last 3 months
    today = date.today() # Get today's date
    #print(today)
    date_three_months_ago = today - relativedelta(months=3) # Subtract exactly 3 months
    #print(date_three_months_ago)

    # Keeping only dates for the last 3 months, but they are originally strings, so we need to convert to objects before we compare
    # Using Python list comprehension (shorter syntax)
    all_dates = [
        d for d in all_dates
        if datetime.strptime(d, '%Y-%m-%d').date() >= date_three_months_ago
    ]

    #print(all_dates)

    highest_price_date = all_dates[0] # i.e., '2026-09-25'
    highest_price = float(daily_prices[highest_price_date]['4. close']) # i.e., '711.6450'
    #highest_price_data = {highest_price_date: highest_price}
    lowest_price_date = all_dates[0] # i.e., '2026-09-25'
    lowest_price = float(daily_prices[lowest_price_date]['4. close']) # i.e., '706.1750'
    #lowest_price_data = {lowest_price_date: lowest_price}
    for d in all_dates:
        close = float(daily_prices[d]['4. close'])
        if close > highest_price:
            highest_price = close
            highest_price_date = d
        if close < lowest_price:
            lowest_price = close
            lowest_price_date = d

    highest_price_date_object = datetime.strptime(highest_price_date, '%Y-%m-%d') # Parse the string into a datetime object
    highest_price_day = int(highest_price_date_object.strftime("%d")) # Remove the zero from before the day
    formatted_highest_price_date = f"{highest_price_date_object:%B} {highest_price_day}, {highest_price_date_object:%Y}"

    lowest_price_date_object = datetime.strptime(lowest_price_date, '%Y-%m-%d')
    lowest_price_day = int(lowest_price_date_object.strftime("%d"))
    formatted_lowest_price_date = f"{lowest_price_date_object:%B} {lowest_price_day}, {lowest_price_date_object:%Y}"

    print("DATE OF HIGHEST PRICE IN PAST 3 MONTHS: " + formatted_highest_price_date)
    message_1 += f"DATE OF HIGHEST PRICE IN PAST 3 MONTHS: {formatted_highest_price_date}\n"
    print(f"HIGHEST PRICE: ${highest_price:.2f}")
    message_1 += f"HIGHEST PRICE: ${highest_price:.2f}\n"
    print("DATE OF LOWEST PRICE IN PAST 3 MONTHS: " + formatted_lowest_price_date)
    message_1 += f"DATE OF LOWEST PRICE IN PAST 3 MONTHS: {formatted_lowest_price_date}\n"
    print(f"LOWEST PRICE: ${lowest_price:.2f}")
    message_1 += f"LOWEST PRICE: ${lowest_price:.2f}\n"

    price_now = daily_prices[all_dates[0]]['4. close']
    price_now_float = float(price_now)
    print(f"PRICE NOW: ${price_now_float:.2f}")
    message_1 += f"PRICE NOW: ${price_now_float:.2f}\n"

    if price_now_float <= lowest_price:
        new_lowest_price = True
        message_1 += f"The price of {ETF} is the lowest that it has been in 3 months! You should buy {ETF} now!"

    return message_1, new_lowest_price