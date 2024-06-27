import requests
import json
import pandas as pd
api_key="LS5RN88HLIZU7NOH"
def get_news_google(ticker_symbol: str):
    url = "https://google.serper.dev/news"

    payload = json.dumps({
    "q": ticker_symbol,
    "num": 30
    })
    headers = {
    'X-API-KEY': 'f6cb1d0f809bb567e76fcdb677415bbb903bdcac',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    result=response.text['news']
    text=""
    if result is not None:
        for i in result:
            if i['title'] is not None:
                text=text+"[News Title]:"+i['title']
            else:
                text=text+"[News Title]:None"
            if i['snippet'] is not None:
                text=text+"[News Content]:"+i['snippet']
            elif i['section'] is not None:
                text=text+"[News Content]:"+i['section']
            else:
                text=text+"[News Content]:None"
    return text

def get_news_alpha_vintage(ticker_symbol: str):
    url=f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker_symbol}&apikey={api_key}"
    print(url)
    response = requests.request("GET", url)
    result=response.json()
    print(result)
    result=result['feed']
    if len(result)>0:
        text=""
        titles = [item['title'] for item in result]
        summaries = [item['summary'] for item in result]

        # Create DataFrame
        for i in range(len(result)):
            text=text+"[News Title]:"+titles[i]+"[News Content]:"+summaries[i]
        return text
        
    else:
        return 

