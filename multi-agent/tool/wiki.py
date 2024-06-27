import os
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from typing import Annotated, List, Tuple
from pandas import DateOffset
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

class wiki:
    def company_profile(ticker_symbol: Annotated[str, "Ticker symbol of the stock (e.g., 'AAPL' for Apple)"]):
        HSI_dict = {
            "01024.HK":"Tencent",
   
        }
        if ticker_symbol in HSI_dict:
            name=HSI_dict[ticker_symbol]
            wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))
            result=wikipedia.run(name)
            return result

        else:
            print("The company is not in the HSI list")
            return 
        





