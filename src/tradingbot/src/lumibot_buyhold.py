from config import ALPACA_CONFIG
from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class BuyHold(Strategy):
    def initialize(self):
        self.sleeptime = "5M"
        self.minutes_before_closing = 15

    def on_trading_iteration(self):
        if self.first_iteration:
            symbol = "SPY"
            # price = self.get_last_price(symbol)
            quantity = 50
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)

if __name__=="__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = BuyHold(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy=strategy)
        trader.run_all()
    else:
        start = datetime(2020,1,1)
        end = datetime(2023,12,1)
        BuyHold.backtest(
            YahooDataBacktesting,
            start,
            end
        )