import streamlit as st
from datetime import date

import yfinance as yf
from plotly import graph_objs as go

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller


START="2015-01-01"
TODAY=date.today().strftime("%Y-%m-%d")

st.title("Wooly Quant Test Web App")

ticker_list = ["DPZ", "AAPL", "GOOGL", "GOOG", "BABA", "JNJ", "JPM", "BAC", "TMO",
               "AVGO", "CVX", "DHR", "V", "MA", "COST", "CRM", "DIS", "CSCO", "QCOM", 
               "AMD", "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", 
               "BRK-A", "BRK-B", "MSFT", "AMZN", "NVDA", "TSLA"]

ticker_1 = st.selectbox("Select ticker for prediction:", ticker_list)

n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

@st.cache_data
def load_ticker(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data...")
data = load_ticker(ticker_1)
data_load_state.text("Done!")

st.subheader("Raw Data")
st.write(data.tail())

def plot_candlestick():
    fig = go.Figure()
    fig.add_candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])
    fig.layout.update(title_text="Candlestick Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
    
plot_candlestick()

# Streamlit App
st.title('ARIMA Model')

# ARIMA Model
def plot_arima():
    order = st.sidebar.text_input("ARIMA Order (p,d,q):", "1,1,1")
    st.sidebar.caption("p: the number of lag observations in the model, also known as the lag order.")
    st.sidebar.caption("d: the number of times the raw observations are differenced; also known as the degree of differencing.")
    st.sidebar.caption("q: the size of the moving average window, also known as the order of the moving average.")
    order = tuple(map(int, order.split(',')))

    model = ARIMA(data['Close'], order=order)
    results = model.fit()

    # Forecasting
    forecast_steps = st.sidebar.slider("Forecast Steps", min_value=1, max_value=30, value=10)
    forecast_index = pd.date_range(start=data['Date'].iloc[-1] + pd.DateOffset(1), periods=forecast_steps, freq='D')
    forecast = results.get_forecast(steps=forecast_steps)

    # Visualize Forecast
    fig_forecast = go.Figure()

    # Original time series
    fig_forecast.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Original'))

    # Forecasted values
    fig_forecast.add_trace(go.Scatter(x=forecast_index, y=forecast.predicted_mean, mode='lines', name='Forecast'))

    fig_forecast.update_layout(title='ARIMA Model Forecast', xaxis_title='Date', yaxis_title='Close Price')
    st.plotly_chart(fig_forecast)

plot_arima()

# Function to visualize autocorrelation and partial autocorrelation plots
def plot_acf_pacf(data, column_name):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot ACF (Autocorrelation Function)
    plot_acf(data[column_name], lags=100, ax=ax1)
    ax1.set_title('Autocorrelation Function')

    # Plot PACF (Partial Autocorrelation Function)
    plot_pacf(data[column_name], lags=100, ax=ax2)
    ax2.set_title('Partial Autocorrelation Function')

    st.pyplot(fig)

# Function to check stationarity
def check_stationarity(data, column_name):
    if column_name not in data.columns:
        st.error(f"Column '{column_name}' not found in the DataFrame.")
        return

    result = adfuller(data[column_name].dropna())  # Drop NA values
    st.write('ADF Statistic:', result[0])
    st.write('p-value:', result[1])
    st.write('Critical Values:', result[4])

# Streamlit app
st.title('ARIMA Model Parameter Selection')

# Load your time series data
df = data
# Sidebar for user input
st.sidebar.header('User Input:')
column_name = st.sidebar.selectbox('Select a column:', df.columns)

# Check stationarity and display ACF/PACF plots
st.header('Check Stationarity and ACF/PACF Plots:')
check_stationarity(df, column_name)
plot_acf_pacf(df, column_name)