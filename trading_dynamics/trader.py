from typing import Dict, Any
from collections import defaultdict
import threading
import logging
from trading_dynamics import belief_models


class Trader:
    holdings: Dict[str, float]

    def __init__(self, name: str, cash: float = 0):
        self.name = name
        self.holdings = defaultdict(lambda: 0)
        self.cash = cash
        self.committed_cash = 0
        self.committed_holdings = defaultdict(lambda: 0)
        self.market_beliefs = {}

        self.logger = logging.Logger(f"{name}")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def analyze_market(self, market, t):
        market.clear_all_open_orders(self)
        self.committed_cash = 0
        self.committed_holdings = defaultdict(lambda: 0)
        internal_value = self.market_beliefs[market.stock_name].sample(t)
        if self.cash - self.committed_cash > internal_value:
            self.submit_buy_order(market, internal_value - 0.5)
        if self.holdings[market.stock_name] - self.committed_holdings[market.stock_name] >= 1:
            self.submit_sell_order(market, internal_value + 0.5)

    def can_buy(self, price):
        return self.cash >= price

    def buy(self, stock_name, price):
        self.logger.debug(f"Trader {self.name} buying {stock_name} for {price}")
        self.committed_cash -= price
        self.cash -= price
        self.holdings[stock_name] += 1

    def can_sell(self, stock_name):
        return self.holdings[stock_name] >= 1

    def sell(self, stock_name, price):
        self.logger.debug(f"Trader {self.name} selling {stock_name} for {price}")
        self.committed_holdings[stock_name] -= 1
        self.holdings[stock_name] -= 1
        self.cash += price

    def submit_buy_order(self, market, limit):
        self.logger.debug(f"Trader {self.name} submitting buy order for {market.stock_name} for {limit}")
        self.committed_cash += limit
        market.add_buy_order(limit, self)

    def submit_sell_order(self, market, limit):
        self.logger.debug(f"Trader {self.name} submitting sell order for {market.stock_name} for {limit}")
        self.committed_holdings[market.stock_name] += 1
        market.add_sell_order(limit, self)
