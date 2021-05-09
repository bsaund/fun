import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from scipy import stats
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


def get_batch_of_100_stock(symbols, types=('quote',)):
    if len(symbols) > 100:
        raise RuntimeError("Cannot query more than 100 stocks at a time")
    symbols_string = ','.join(symbols)
    types_str = ','.join(types)
    api_url = f'{get_base_api_url()}/stable/stock/market/batch?symbols={symbols_string}&types={types_str}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url)
    if data.status_code != 200:
        raise RuntimeError(f"Error, api request returned {data.status_code} for request{api_url}")
    return data.json()


# def get_stats(symbols):
#     api_url = f'{get_base_api_url()}/stable/stock/{symbol}/stats/?token={IEX_CLOUD_API_TOKEN}'
#     data = requests.get(api_url)
#     if data.status_code != 200:
#         raise RuntimeError(f"Error, api request returned {data.status_code} for request{api_url}")
#     return data.json()


def get_stocks(symbols, types=('quote',)):
    d = dict()
    for group in chunks(symbols, 100):
        d.update(get_batch_of_100_stock(group, types))
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

    # print(df)
    return df


def build_stats_dataframe():
    print("Building stats dataframe")
    stocks = get_stocks(list(load_sp500()['Ticker']), types=('stats', 'price'))
    columns = ['Ticker', 'Stock Price', 'One-Year Price Return', 'Number of Shares to Buy']
    df = pd.DataFrame(columns=columns)
    for tkr, data in stocks.items():
        stats = data['stats']
        df = df.append(
            pd.Series([
                tkr, data['price'], stats['year1ChangePercent'], 'N/A'
            ], index=columns),
            ignore_index=True
        )

    df.sort_values('One-Year Price Return', ascending=False, inplace=True)
    return df


def fill_with_even_allocation(df, portfolio_total):
    investment_per_stock = portfolio_total / len(df)
    for ind in df.index:
        df.loc[ind, 'Number of Shares to Buy'] = math.floor(investment_per_stock / df.loc[ind, 'Stock Price'])
    return df


def wip_batch():
    # batches = chunks(load_sp500()['Ticker'], 10)
    # get_batch_stock(list(next(batches)))
    data = get_stocks(list(load_sp500()['Ticker']))
    print(len(data.keys()))


def main():
    # stock = get_stock('AAPL')
    # print(stock['latestPrice'])
    df = build_dataframe()
    df = fill_with_even_allocation(df, 1_000_000)
    print(df)


def wip():
    # data = get_stocks(list(load_sp500()['Ticker']), types=('stats',))
    df = build_stats_dataframe()
    df = fill_with_even_allocation(df, 1_000_000)
    print(df)


if __name__ == "__main__":
    wip()
    # main()
