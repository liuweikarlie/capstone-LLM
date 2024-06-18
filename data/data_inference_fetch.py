from datetime import date, datetime, timedelta
import akshare as ak
import pandas as pd
import requests
import bing_news
import index
import scrap_data


def convert_date(date_str):
    date_str = date_str[:26] + date_str[27:-1]
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj

def get_curday():
    
    return date.today().strftime("%Y-%m-%d")

def n_weeks_before(date_string, n, format = "%Y-%m-%d"):
    
    date = datetime.strptime(date_string, "%Y-%m-%d") - timedelta(days=7*n)
    
    return date.strftime(format=format)

def get_news(symbol):
    input_search=index.HSI_dict[symbol]

    bing=bing_news.BingSearch(input_search)
    response=bing.formulate(n_weeks_before(get_curday(),1))
    response.rename(columns={'name': 'Headline','description':'Content',
                                      'datePublished':'date'}, inplace=True)
          
    response['date'] = response['date'].map(convert_date)

    return response


def get_cur_return(symbol,start_date,end_date,adjust="qfq"):
    data=scrap_data.get_return(symbol,start_date,end_date,adjust)
    new_column_names = {
    '起始日期': 'Start Date',
    '起始价': 'Start Price',
    '结算日期': 'End Date',
    '结算价': 'End Price',
    '周收益': 'Weekly Returns',
    '简化周收益':'Simple Weekly Returns',
    }
    df = df.rename(columns=new_column_names)

    return data


def cur_financial_data(symbol, start_date, end_date):
    text='{company_name} is a leading entity in the {industry} sector. Incorporated and publicly traded since {ipo_time}, the company has established its reputation as one of the key players in the market. As of today, Tencent has a market capitalization of {market_cap} in RMB, which {share_num} shares outstanding.\n\n{company_name} operates primarily in the China, trading under the ticker {symbol}'
    df=scrap_data.stock_individual_info_em(symbol)
    return data

