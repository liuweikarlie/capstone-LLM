from IPython.display import Image, display
from datetime import datetime
import autogen
from autogen.coding import LocalCommandLineCodeExecutor
import os
from autogen.cache import Cache

import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from typing import Annotated, List, Tuple
from pandas import DateOffset
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests
import json

api_key="LS5RN88HLIZU7NOH"

def save_markdown_report(report: str, file_path: str):
    with open(file_path, "w") as f:
        f.write(report)
    return f"Report saved to {file_path}"

def get_news_alpha_vintage(ticker_symbol: str):
    url=f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker_symbol}&apikey={api_key}"
    print(url)
    response = requests.request("GET", url)
    result=response.json()
    # print(result)
    result=result['feed']
    if len(result)>0:
        text=""
        titles = [item['title'] for item in result]
        summaries = [item['summary'] for item in result]

        for i in range(len(result)):
            text=text+"[News Title]:"+titles[i]+"[News Content]:"+summaries[i]
        return text
        
    else:
        return 



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
    plt.title(' Stock Price Movement')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
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
    df=df.tail(10)

    return df




    



config_list = [
#     {
#     'model' : 'test2',
#     'api_key':'ebc76beedf89486382e773d3b4cf0b10',
#     'base_url' : 'https://gpgpt.openai.azure.com/',
#     'api_type' : 'azure',
#     'api_version' : '2024-05-01-preview',
#  },
#    {
#     'model': 'llama3-8b-8192', #model here is your model name in the LM studio
#     'api_key': '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',
#     'base_url': "https://api.groq.com/openai/v1",
#     }

# {
#     'model': 'meta/llama3-8b-instruct', 
#     'api_key': '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',
#     'base_url': "https://integrate.api.nvidia.com/v1",
#     }
 {
    'model': 'NotRequired', 
    'api_key': 'NotRequired',
    'base_url': "http://0.0.0.0:4000",
   }


]

tools = [
  
    {
        "function": get_news_alpha_vintage,
        "name": "get_company_news",
        "description": "get company latest news"
    },
    {
        "function":plot_stock_price_chart,
        "name":"plot_stock_price",
        "description":"plot stock price trend in the past month"
    },
    {
        "function":get_price,
        "name":"get_stock_price",
        "description":"get stock price in the past month"
    }
]
config_list = config_list
llm_config={
        "functions": [
            {
                "name": "get_company_news",
                "description": "Get the latest news for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker_symbol": {
                            "type": "string",
                            "description": "Ticker symbol of the company (e.g., 'NVDA')",
                        },
                    },
                    "required": ["ticker_symbol"],
                },
            },
            {
                "name": "plot_stock_price",
                "description": "Plot the stock price trend for a given ticker symbol and date range.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker_symbol": {
                            "type": "string",
                            "description": "Ticker symbol of the stock (e.g., 'NVDA')",
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date of the historical data in 'YYYY-MM-DD' format",
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date of the historical data in 'YYYY-MM-DD' format",
                        },
                        "save_path": {
                            "type": "string",
                            "description": "File path where the plot should be saved",
                        },
                    },
                    "required": ["ticker_symbol", "start_date", "end_date", "save_path"],
                },
            },
            {
                "name": "get_stock_price",
                "description": "Get the historical stock price data for a given ticker symbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker_symbol": {
                            "type": "string",
                            "description": "Ticker symbol of the stock (e.g., 'NVDA')",
                        },
                    },
                    "required": ["ticker_symbol"],
                },
            },
            {
                "name": "save_markdown_report",
                "description": "Save the analysis to a markdown file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report": {
                            "type": "string",
                            "description": "The report content.",
                        },
                        "file_path": {
                            "type": "string",
                            "description": "The file path where the report should be saved.",
                        },
                    },
                    "required": ["report", "file_path"],

            }
            }
        ],
         "config_list": config_list,
        "timeout": 120,

        
    }

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="For coding tasks, only use the functions you have been provided with. Don't create code on your own. Reply TERMINATE when the task is done.",

    llm_config=llm_config,)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") is not None and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="coding"),

    },
)

user_proxy.register_function(
    function_map={
        "get_company_news": get_news_alpha_vintage,
        "get_stock_price": get_price,
        "plot_stock_price": plot_stock_price_chart,
        "save_markdown_report": save_markdown_report,
    }
)
task = (
    "Use the function call (please run the code)to create a stock research report about MSFT stock in the past month and save it to 'report.md'. "
    "Use the 'get_stock_price' function to retrieve price data."
    "Use the 'get_company_news' function to fetch recent news."
    "Use the 'plot_stock_price' function to plot the stock price trend (start_date='2024-02-01',end_date='2024-06-01'), save the figure to 'stock_price.png'."
    "Finally,Include the stock price, news, and your analysis for stock price in the report and store the writing in report.md by using the 'save_markdown_report'function."
)

with Cache.disk(cache_seed=31) as cache:

    chat_res = user_proxy.initiate_chat(
        assistant,
        message=task,
        summary_method="reflection_with_llm",
    )