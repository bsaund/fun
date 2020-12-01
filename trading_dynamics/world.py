import time

from trading_dynamics.trader import Trader
from trading_dynamics.market import SingleMarket
from trading_dynamics import belief_models
from utils.plotter import TimeSeriesPlotter
import math
import logging


def simple_world():
    trader1 = Trader("trader 1", 200.0)
    # trader1.market_beliefs["ABC"] = StaticExactBelief(75)
    trader1.market_beliefs["ABC"] = belief_models.TimeVaryingExactBelief(lambda x: 25 * math.sin(x) + 50)
    trader2 = Trader("trader 2", 50.0)
    trader2.market_beliefs["ABC"] = belief_models.StaticExactBelief(60)
    trader2.holdings["ABC"] = 10
    market = SingleMarket("ABC", last_trade_price=20)

    plotter = TimeSeriesPlotter(["last trade price", "trader 1 cash", "trader 2 cash"], max_time_interval=10,
                                min_time=10)

    data = {"last trade price": market.last_trace_price,
            "trader 1 cash": trader1.cash,
            "trader 2 cash": trader2.cash}
    plotter.update(0, data)

    t0 = time.time()
    t = 0
    while t < 60:
        t = time.time() - t0
        for trader in [trader1, trader2]:
            trader.analyze_market(market, t)

        data = {"last trade price": market.last_trace_price,
                "trader 1 cash": trader1.cash,
                "trader 2 cash": trader2.cash}
        plotter.update(t, data)
        if not plotter.is_open():
            return
        time.sleep(0.03)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    simple_world()
