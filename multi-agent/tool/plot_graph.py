import os
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from typing import Annotated, List, Tuple
from pandas import DateOffset
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests
api_key="LS5RN88HLIZU7NOH"


def plot_stock_price_chart(
    ticker_symbol: Annotated[
        str, "Ticker symbol of the stock (e.g., 'AAPL' for Apple)"
    ],
    start_date: Annotated[
        str, "Start date of the historical data in 'YYYY-MM-DD' format"
    ],
    end_date: Annotated[
        str, "End date of the historical data in 'YYYY-MM-DD' format"
    ],
    save_path: Annotated[str, "File path where the plot should be saved"],
) -> str:
    """
    Plot a stock price chart using mplfinance for the specified stock and time period,
    and save the plot to a file.
    """
    # Fetch historical data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True)
    if stock_data.empty:
        print("No data found for the given date range.")
        return
    

    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label=ticker_symbol+' Stock Price')
    plt.title('Nvidia Stock Price Movement')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.save(save_path)
    return f"{ticker_symbol} chart saved to <img {save_path}>"


def get_price(ticker_symbol: str):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker_symbol}&outputsize=full&apikey={api_key}"
    response = requests.request("GET", url)
    result=response.json()
    result=result['Time Series (Daily)']
    df = pd.DataFrame.from_dict(result).T

    # Rename columns for better readability
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']


    # Convert index to datetime
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()


    # Convert data types
    df = df.astype({
        'Open': 'float',
        'High': 'float',
        'Low': 'float',
        'Close': 'float',
        'Volume': 'int'
    })

    return df




    


