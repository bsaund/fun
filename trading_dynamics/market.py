from queue import PriorityQueue
import numpy as np


class SingleMarket:
    """Market for a single stock"""

    def __init__(self, stock_name, last_trade_price):
        self.open_buy_orders = []
        self.open_sell_orders = []
        self.stock_name = stock_name
        self.last_trace_price = last_trade_price

    def query_open_orders(self, trader):
        return [("buy", o[0], o[1]) for o in self.open_buy_orders if o[1] == trader] + \
               [("sell", o[0], o[1]) for o in self.open_sell_orders if o[1] == trader]

    def clear_all_open_orders(self, trader):
        self.open_buy_orders = [o for o in self.open_buy_orders if o[1] != trader]
        self.open_sell_orders = [o for o in self.open_sell_orders if o[1] != trader]

    def add_buy_order(self, limit, trader):
        for i, existing_order in enumerate(self.open_sell_orders):
            if limit >= existing_order[0]:
                if self.attempt_trade(existing_order[1], trader, np.mean([existing_order[0], limit])):
                    del self.open_sell_orders[i]
                    return
        self.open_buy_orders.append([limit, trader])

    def add_sell_order(self, limit, trader):
        for i, existing_order in enumerate(self.open_buy_orders):
            if limit <= existing_order[0]:
                if self.attempt_trade(trader, existing_order[1], np.mean([existing_order[0], limit])):
                    del self.open_buy_orders[i]
                    return
        self.open_sell_orders.append([limit, trader])

    def attempt_trade(self, from_trader, to_trader, price) -> bool:
        if not to_trader.can_buy(price) or not from_trader.can_sell(self.stock_name):
            return False

        to_trader.buy(self.stock_name, price)
        from_trader.sell(self.stock_name, price)
        self.last_trace_price = price
        return True
