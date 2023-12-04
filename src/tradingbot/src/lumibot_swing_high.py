from config import ALPACA_CONFIG
from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class SwingHigh(Strategy):
    data = []
    order_number = 0
    def initialize(self):
        self.sleeptime = "10S"
    
    def on_trading_iteration(self):
        return super().on_trading_iteration()