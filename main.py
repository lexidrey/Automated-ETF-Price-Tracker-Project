import requests
from ETF_lowest_price_in_past_three_months_tracker import get_message_1
from ETF_significant_percent_drop_from_highest_ten_day_price_tracker import get_message_2
from send_ETF_price_tracker_email import send_email
import requests
import os
from dotenv import load_dotenv
import pprint
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from api_data import api_data

def get_ETF_data(ETF):

    # Locally: It looks for a .env file and loads its variables into your environment.
    # On GCP: If there is no .env file, it simply does nothing. It does not throw an error.
    load_dotenv()

    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ETF,
        "outputsize": "compact", # returns latest 100 data points
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    url = 'https://www.alphavantage.co/query'

    response = requests.get(url, params=params)
    data = response.json()

    return data

def main():

    ETF = "VOO"

    ETF_data = get_ETF_data(ETF)
    #ETF_data = api_data
    message_1, new_lowest_price = get_message_1(ETF_data, ETF)
    message_2, significant_price_drop = get_message_2(ETF_data, ETF)

    print(message_1)
    print(message_2)

    email_body = ""
    print(new_lowest_price)
    print(significant_price_drop)

    if new_lowest_price or significant_price_drop:
        email_body += f"Hello! This is an automated message regarding the {ETF} ETF.\n\n"

    if new_lowest_price and significant_price_drop:
        email_body += f"{ETF} PRICE UPDATE:\n\n{message_1}\n\n{message_2}"
    elif new_lowest_price:
        email_body += f"{ETF} IS AT THE LOWEST PRICE IT HAS BEEN IN THE PAST 30 DAYS:\n\n{message_1}"
    elif significant_price_drop:
        email_body += f"{ETF} HAS DROPPED SIGNIFICANTLY IN PRICE OVER THE PAST 10 DAYS:\n\n{message_2}"

    if email_body != "":
        send_email("ETF Price Tracker Update", email_body)

if __name__ == "__main__":
    main()