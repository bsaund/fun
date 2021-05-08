import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
import timeit

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


def get_batch_of_100_stock(symbols):
    if len(symbols) > 100:
        raise RuntimeError("Cannot query more than 100 stocks at a time")
    symbols_string = ','.join(symbols)
    api_url = f'{get_base_api_url()}/stable/stock/market/batch?symbols={symbols_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url)
    if data.status_code != 200:
        raise RuntimeError(f"Error, api request returned {data.status_code} for request{api_url}")
    return data.json()

def get_stocks(symbols):
    d = dict()
    for group in chunks(symbols, 100):
        d.update(get_batch_of_100_stock(group))
    return d


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def build_dataframe():

    columns = ['Ticker', 'Stock Price', 'Market Cap', 'Number of Shares to Buy']
    df = pd.DataFrame(columns=columns)
    print('query url')
    stocks = get_stocks(list(load_sp500()['Ticker']))
    print('load up df')
    for tkr, data in stocks.items():
        # print(f'Getting {tkr}')
        quote = data['quote']
        df = df.append(
            pd.Series([
                tkr, quote['latestPrice'], quote['marketCap'], 'N/A'
            ], index=columns),
            ignore_index=True
        )
    print('printing')

    print(df)



def wip_batch():
    # batches = chunks(load_sp500()['Ticker'], 10)
    # get_batch_stock(list(next(batches)))
    data = get_stocks(list(load_sp500()['Ticker']))
    print(len(data.keys()))


def main():
    # stock = get_stock('AAPL')
    # print(stock['latestPrice'])
    build_dataframe()


if __name__ == "__main__":
    wip_batch()
    # load_sp500()
    # main()
    # print(f'total time: {timeit.timeit(main)}')
