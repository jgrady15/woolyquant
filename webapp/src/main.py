from datetime import date

import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv

import yfinance as yf
from plotly import graph_objs as go

import bcrypt
import streamlit as st
import streamlit_authenticator as stauth

st.title("Wooly Quant")

_credentials = {
    "usernames": {
        "temp": {
            "name": "Jonathan Ong",
            "password": "t"
        }
    }
}

_auth = stauth.Authenticate(_credentials, "wq_dashboard", "cookiepassword", cookie_expiry_days=14)

try:
    if _auth.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)



_n, _auth_status, _uname = _auth.login("Login", "main")

if _auth_status == False:
    st.error("Invalid login credentials!")

if _auth_status == None:
    st.warning("Please enter in username and password!")
    st.toast(f'{_n}{_uname}')
    
if _auth_status:
    START="2015-01-01"
    TODAY=date.today().strftime("%Y-%m-%d")

    st.title("Wooly Quant Test Web App")

    sample_stocks = ("AAPL", "TSLA", "GME")
    selected_stock = st.selectbox("Select dataset for prediction:", sample_stocks)

    n_years = st.slider("Years of prediction:", 1, 4)
    period = n_years * 365

    @st.cache_data
    def load_ticker(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text("Load data...")
    data = load_ticker(selected_stock)
    data_load_state.text("Done!")

    st.subheader("Raw Data")
    st.write(data.tail())

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
        
    plot_raw_data()

# if st.button('Connect DB'):
#     load_dotenv('./keys.env')
#     trading_client = TradingClient(os.getenv("ALPACA_PK"), os.getenv("ALPACA_SK"), paper=True)
#     account = trading_client.get_account()
#     assets = trading_client.get_asset("AAPL")
#     print(assets, account)
