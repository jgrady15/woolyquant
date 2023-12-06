import os
import ctypes
from datetime import datetime

import boto3
import logging
from botocore.exceptions import ClientError
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import ALPACA_CONFIG

def fast_atof(s):
    return ctypes.c_float(float(s)).value

ticker = "TSLA"
trading_client = TradingClient(api_key=ALPACA_CONFIG["API_KEY"], secret_key=ALPACA_CONFIG["API_SECRET"], paper=True)
account = trading_client.get_account()
asset = trading_client.get_asset(symbol_or_asset_id=ticker)

if asset.tradable:
    try:
        curr_pos = trading_client.get_open_position(symbol_or_asset_id=ticker)
        
        # TODO: We can save this somewhere
        today = str(datetime.today())
        
        # boto3 calls to dynamodb 
        dynamodb = boto3.resource("dynamodb")
        dynamodb.Table("woolyquant_cria_trading_bot")
        response = dynamodb.get_item(
            Key = {
                'Date': today[0:10],
                'TickerSymbol': ticker
            }
        )
        
        prev_closing_price = fast_atof(response['ClosingPrice'])
        curr_price = fast_atof(curr_pos.current_price)
        
        # Buy stop, we rake in our profits and sell half of what we have.
        if curr_price > (prev_closing_price * 1.05):
            if curr_pos.qty // 2 > 0:
                market_order_data = MarketOrderRequest(
                        symbol="AAPL",
                        qty=curr_pos.qty//2,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.DAY
                        )
                market_order = trading_client.submit_order(order_data=market_order_data)
        
        # Limit loss, we buy to cash in and hold our stronger position
        if curr_price < (prev_closing_price * 0.95):
            market_order_data = MarketOrderRequest(
                                symbol="AAPL",
                                qty=10,
                                side=OrderSide.BUY,
                                time_in_force=TimeInForce.DAY
                                )
            market_order = trading_client.submit_order(order_data=market_order_data)
    except ClientError as e:
        logging.error(e)
        # s3 = boto3.resource("s3")
        
        
        