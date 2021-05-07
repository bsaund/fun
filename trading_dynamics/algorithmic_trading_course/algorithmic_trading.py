import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

from secrets import IEX_CLOUD_API_TOKEN

SANDBOX = True


def load_sp500():
    return pd.read_csv('algorithmic_trading_course/sp_500_stocks.csv')


def get_base_api_url():
    if SANDBOX:
        return 'https://sandbox.iexapis.com'
    return 'https://cloud.iexapis.com'


def get_stock(symbol):
    api_url = f'{get_base_api_url()}/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url)
    if data.status_code != 200:
        raise RuntimeError(f"Error, api request returned {data.status_code} for request{api_url}")
    return data.json()


def build_dataframe():
    columns = ['Ticker', 'Stock Price', 'Market Cap', 'Number of Shares to Buy']
    df = pd.DataFrame(columns=columns)
    print(df)

def repeated_get():
    prices = [get_stock('AAPL')['latestPrice'] for _ in range(100)]
    print(np.mean(prices))


def main():
    stock = get_stock('AAPL')
    print(stock['latestPrice'])


if __name__ == "__main__":
    load_sp500()
    main()
    repeated_get()
