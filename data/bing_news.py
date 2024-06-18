import os
import requests
import json
import pandas as pd
import html
import datetime

# reference https://learn.microsoft.com/en-us/bing/search-apis/bing-news-search/reference/query-parameters
def decode_html_entities(text):
    return html.unescape(text)

class BingSearch:
    def __init__(self,symbol):
        self.symbol=symbol
        self.subscription_key = "fe3a991cdbc74336b621548a39c03d33"
        self.search_url = "https://api.bing.microsoft.com/v7.0/news/search"
        self.headers = {"Ocp-Apim-Subscription-Key" : self.subscription_key}
    def bing_api(self,start_time):
        """
        get the most recent 100 data for the symbol news within month

            Args:
                symbol: str
                    A-share market stock symbol

            Return:
                search_results: dict
                    raw data from bing api
        """
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        unix_timestamp = int(start_time.timestamp())
        params  = {"q": self.symbol, "textDecorations": True, "textFormat": "HTML","count":100,"sortBy":"Date","since":unix_timestamp,"category":"Business"}
        response = requests.get(self.search_url, headers=self.headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        # descriptions = [article["description"] for article in search_results["value"]]
        # print(descriptions)
        return search_results




    def final_output(self,raw_data):
        """
        manage the raw data to desired format

            Args:
                raw_data: dict
                    raw data from bing api

            Return:
                df: DataFrame
                    including (name (/title), description, datePublished, url)
        
        """
        raw_data=raw_data['value']
        df = pd.DataFrame(raw_data)
        df=df[['name','description','datePublished','url']]
        df['name'] = df['name'].apply(decode_html_entities)
        df['description'] = df['description'].apply(decode_html_entities)
        df['name'] = df['name'].str.replace('<b>', '').str.replace('</b>', '')
        df['description'] = df['description'].str.replace('<b>', '').str.replace('</b>', '')

        return df
    
    def formulate(self,start_time):
        raw_data=self.bing_api(start_time)
        df=self.final_output(raw_data)
        return df


if __name__ == "__main__":
    symbol = "阿里巴巴 Alibaba"
    start_time = "2023-06-01"
    bing_search = BingSearch(symbol)
    df=bing_search.formulate(start_time)
    print(df)
    df.to_csv("bing_news.csv",index=False)




