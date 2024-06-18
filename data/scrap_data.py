import yfinance as yf
import math
import akshare as ak
import requests
import json
import pandas as pd
import random
import time
import index 
import bing_news
import datetime

start_date = "20240101"
end_date = "20240601"

def stock_news_em(symbol: str = "300059",page_number:int = 1) -> pd.DataFrame:
    """
    东方财富-个股新闻-最近 100 条新闻
    https://so.eastmoney.com/news/s?keyword=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%AF%BF&pageindex=1&searchrange=8192&sortfiled=4
    :param symbol: 股票代码
    :type symbol: str
    :return: 个股新闻
    :rtype: pandas.DataFrame
    """
    url = "http://search-api-web.eastmoney.com/search/jsonp"
    params = {
        "cb": "jQuery3510875346244069884_1668256937995",
        "param": '{"uid":"",'
        + f'"keyword":"{symbol}"'
        + ',"type":["cmsArticleWebOld"],"client":"web","clientType":"web","clientVersion":"curr",'
        '"param":{"cmsArticleWebOld":{"searchScope":"default","sort":"default","pageIndex":'+str(page_number)+','
        '"pageSize":100,"preTag":"<em>","postTag":"</em>"}}}',
        "_": "1668256937996",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(
        data_text.strip("jQuery3510875346244069884_1668256937995(")[:-1]
    )
    temp_df = pd.DataFrame(data_json["result"]["cmsArticleWebOld"])
    temp_df.rename(
        columns={
            "date": "发布时间",
            "mediaName": "文章来源",
            "code": "-",
            "title": "新闻标题",
            "content": "新闻内容",
            "url": "新闻链接",
            "image": "-",
        },
        inplace=True,
    )
    temp_df["关键词"] = symbol
    temp_df = temp_df[
        [
            "关键词",
            "新闻标题",
            "新闻内容",
            "发布时间",
            "文章来源",
            "新闻链接",
        ]
    ]
    temp_df["新闻标题"] = (
        temp_df["新闻标题"]
        .str.replace(r"\(<em>", "", regex=True)
        .str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["新闻标题"] = (
        temp_df["新闻标题"]
        .str.replace(r"<em>", "", regex=True)
        .str.replace(r"</em>", "", regex=True)
    )
    temp_df["新闻内容"] = (
        temp_df["新闻内容"]
        .str.replace(r"\(<em>", "", regex=True)
        .str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["新闻内容"] = (
        temp_df["新闻内容"]
        .str.replace(r"<em>", "", regex=True)
        .str.replace(r"</em>", "", regex=True)
    )
    temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\u3000", "", regex=True)
    temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\r\n", " ", regex=True)

    temp_df["发布时间"] = pd.to_datetime(temp_df["发布时间"], exact=False, format="%Y-%m-%d")
    temp_df.sort_values(by=["发布时间"], inplace=True)

    return temp_df



def turn_page(start_time,data):
#   print("hello")
#   print(data.iloc[0]['发布时间'])
#   print(start_time)
  if data.iloc[0]['发布时间']>start_time:
    print("Yes")
    return True
  else:
    return False

  


def get_news(symbol):
    start_time=pd.Timestamp(start_date)
    page_number=1
    data_copy = stock_news_em(symbol=symbol,page_number=page_number)
    data=data_copy
    count=0
    while turn_page(start_time,data_copy):
      if count>6:
          break
    
      page_number=page_number+1
      time.sleep(3)
      data=stock_news_em(symbol=symbol,page_number=page_number)
      data_copy = pd.concat([data_copy, data], ignore_index=True)
      data_copy.sort_values(by=["发布时间"], inplace=True)
      print("pass")
      count=count+1
      
    return data_copy


def stock_individual_info_em(symbol: str = "603777", timeout: float = None) -> pd.DataFrame:
    """
    东方财富-个股-股票信息
    https://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param timeout: choice of None or a positive float number
    :type timeout: float
    :return: 股票信息
    :rtype: pandas.DataFrame
    """

    url = "http://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fltt": "2",
        "invt": "2",
        "fields": "f120,f121,f122,f174,f175,f59,f163,f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f255,f256,f257,f258,f127,f199,f128,f198,f259,f260,f261,f171,f277,f278,f279,f288,f152,f250,f251,f252,f253,f254,f269,f270,f271,f272,f273,f274,f275,f276,f265,f266,f289,f290,f286,f285,f292,f293,f294,f295",
        "secid": f"116.{symbol}",
        "_": "1640157544804",
    }
    r = requests.get(url, params=params, timeout=timeout)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df.reset_index(inplace=True)
    del temp_df["rc"]
    del temp_df["rt"]
    del temp_df["svr"]
    del temp_df["lt"]
    del temp_df["full"]
    code_name_map = {
        "f57": "股票代码",
        "f58": "股票简称",
        "f84": "总股本",
        "f85": "流通股",
        "f127": "行业",
        "f116": "总市值",
        "f117": "流通市值",
        "f189": "上市时间",
    }
    temp_df["index"] = temp_df["index"].map(code_name_map)
    temp_df = temp_df[pd.notna(temp_df["index"])]
    if "dlmkts" in temp_df.columns:
        del temp_df["dlmkts"]
    temp_df.columns = [
        "item",
        "value",
    ]
    temp_df.reset_index(inplace=True, drop=True)
    return temp_df



def get_return(symbol, start_date,end_date,adjust="qfq"):
    """
    Get stock return data.

    Args:
        symbol: str
            A-share market stock symbol
        adjust: str ("qfq", "hfq")
            price ajustment
            default = "qfq" 前复权

    Return:
        weekly forward filled return data
    """

    # load data
    return_data = ak.stock_hk_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust=adjust)

    # process timestamp
    return_data["日期"] = pd.to_datetime(return_data["日期"])
    return_data.set_index("日期", inplace=True)

    # resample and filled with forward data
    weekly_data = return_data["收盘"].resample("W").ffill()
    weekly_returns = weekly_data.pct_change()[1:]
    weekly_start_prices = weekly_data[:-1]
    weekly_end_prices = weekly_data[1:]
    weekly_data = pd.DataFrame({
        '起始日期': weekly_start_prices.index,
        '起始价': weekly_start_prices.values,
        '结算日期': weekly_end_prices.index,
        '结算价': weekly_end_prices.values,
        '周收益': weekly_returns.values
    })
    weekly_data["简化周收益"] = weekly_data["周收益"].map(return_transform)

    return weekly_data


def return_transform(ret):

    up_down = '涨' if ret >= 0 else '跌'
    integer = math.ceil(abs(100 * ret))
    if integer == 0:
        return "平"

    return up_down + (str(integer) if integer <= 5 else '5+')


def get_news(symbol):
    start_time=pd.Timestamp(start_date)
    page_number=1
    data_copy = stock_news_em(symbol=symbol,page_number=page_number)
    data=data_copy
    while turn_page(start_time,data_copy):
      page_number=page_number+1
      time.sleep(3)
      data=stock_news_em(symbol=symbol,page_number=page_number)
      data_copy = pd.concat([data_copy, data], ignore_index=True)
      data_copy.sort_values(by=["发布时间"], inplace=True)
      print("pass")
    return data_copy


def get_basic(symbol, data):
    """
    Get and match basic data to news dataframe.

    Args:
        symbol: str
            A-share market stock symbol
        data: DataFrame
            dated news data

    Return:
        financial news dataframe with matched basic_financial info
    """
    key_financials = ['REPORT_DATE', 'GROSS_PROFIT_QOQ', 'OPERATE_INCOME_QOQ', 'CURRENT_RATIO', 'DEBT_ASSET_RATIO']

    # load quarterly basic data
    basic_quarter_financials = ak.stock_financial_hk_analysis_indicator_em(symbol = symbol, indicator="报告期")
    basic_fin_dict = basic_quarter_financials.to_dict("index")
    basic_fin_list = [dict([(key, val) for key, val in basic_fin_dict[i].items() if (key in key_financials) and val]) for i in range(len(basic_fin_dict))]

    # match basic financial data to news dataframe
    matched_basic_fin = []
    for i, row in data.iterrows():

        newsweek_enddate = row['结算日期'].strftime("%Y-%m-%d")

        matched_basic = {}
        for basic in basic_fin_list:
            # match the most current financial report
            if basic["REPORT_DATE"] < newsweek_enddate:
                matched_basic = basic
                break
        matched_basic_fin.append(json.dumps(matched_basic, ensure_ascii=False))

    data['基本面'] = matched_basic_fin

    return data

def convert_date(date_str):
    date_str = date_str[:26] + date_str[27:-1]
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj

def raw_financial_data(symbol, with_basics = True):

    # get return data from API
    data = get_return(symbol=symbol,start_date=start_date,end_date=end_date,adjust="qfq")

    # get news data from local
    news_df = get_news(symbol)
    news_df["发布时间"] = pd.to_datetime(news_df["发布时间"], exact=False, format="%Y-%m-%d")
    news_df.sort_values(by=["发布时间"], inplace=True)

    # match weekly news for return data
    news_list = []
    for a, row in data.iterrows():
        week_start_date = row['起始日期'].strftime('%Y-%m-%d')
        week_end_date = row['结算日期'].strftime('%Y-%m-%d')
        print(symbol, ': ', week_start_date, ' - ', week_end_date)

        weekly_news = news_df.loc[(news_df["发布时间"]>week_start_date) & (news_df["发布时间"]<week_end_date)]
        if len(weekly_news)==0:
          print("bingsearch begin")
          stock_name=index.HSI_dict[symbol]
          symbol_input=symbol[1:]

          bing=bing_news.BingSearch(stock_name+" "+symbol)
          weekly_news=bing.formulate(week_start_date)
          weekly_news.rename(columns={'name': '新闻标题','description':'新闻内容',
                                      'datePublished':'发布时间'}, inplace=True)
          
          weekly_news['发布时间'] = weekly_news['发布时间'].map(convert_date)


          




        weekly_news = [
            {
                "发布时间": n["发布时间"].strftime('%Y%m%d'),
                "新闻标题": n['新闻标题'],
                "新闻内容": n['新闻内容'],
            } for a, n in weekly_news.iterrows()
        ]
        news_list.append(json.dumps(weekly_news,ensure_ascii=False))

    data["新闻"] = news_list

    if with_basics:
        data = get_basic(symbol=symbol, data=data)
        # data.to_csv(symbol+start_date+"_"+end_date+".csv")
    else:
        data['新闻'] = [json.dumps({})] * len(data)
        # data.to_csv(symbol+start_date+"_"+end_date+"_nobasics.csv")

    return data


def get_company_prompt_new(symbol):
    try:
        company_profile = dict(stock_individual_info_em(symbol).values)
    except:
        print("Company Info Request Time Out! Please wait and retry.")
    company_profile["上市时间"] =  pd.to_datetime(str(company_profile["上市时间"])).strftime("%Y年%m月%d日")

    template = "[公司介绍]:\n\n{股票简称}是一家在{行业}行业的领先实体，自{上市时间}成立并公开交易。截止今天，{股票简称}的总市值为{总市值}人民币，总股本数为{总股本}，流通市值为{流通市值}人民币，流通股数为{流通股}。" \
        "\n\n{股票简称}主要在中国运营，以股票代码{股票代码}在交易所进行交易。"

    formatted_profile = template.format(**company_profile)
    stockname = company_profile['股票简称']
    return formatted_profile, stockname

def map_return_label(return_lb):
    """
    Map abbrev in the raw data
    Example:
        涨1 -- 上涨1%
        跌2 -- 下跌2%
        平 -- 股价持平
    """

    lb = return_lb.replace('涨', '上涨')
    lb = lb.replace('跌', '下跌')
    lb = lb.replace('平', '股价持平')
    lb = lb.replace('1', '0-1%')
    lb = lb.replace('2', '1-2%')
    lb = lb.replace('3', '2-3%')
    lb = lb.replace('4', '3-4%')
    if lb.endswith('+'):
        lb = lb.replace('5+', '超过5%')
    else:
        lb = lb.replace('5', '4-5%')

    return lb

def check_news_quality(n, last_n, week_end_date, repeat_rate = 0.6):
    try:
        # check content avalability
        if not (not(str(n['新闻内容'])[0].isdigit()) and not(str(n['新闻内容'])=='nan') and n['发布时间'][:8] <= week_end_date.replace('-', '')):
            return False
        # check highly duplicated news
        # (assume the duplicated contents happened adjacent)

        elif str(last_n['新闻内容'])=='nan':
            return True
        elif len(set(n['新闻内容'][:20]) & set(last_n['新闻内容'][:20])) >= 20*repeat_rate or len(set(n['新闻标题']) & set(last_n['新闻标题']))/len(last_n['新闻标题']) > repeat_rate:
            return False

        else:
            return True
    except TypeError:
        print(n)
        print(last_n)
        raise Exception("Check Error")


def sample_news(news, k=10):
    """
    Ramdomly select past news.

    Args:
        news:
            newslist in the timerange
        k: int
            the number of selected news
    """
    return [news[i] for i in sorted(random.sample(range(len(news)), k))]


# ------------------------------------------------------------------------------
# Prompt Generation
# ------------------------------------------------------------------------------

SYSTEM_PROMPT = "你是一名经验丰富的股票市场分析师。你的任务是根据公司在过去几周内的相关新闻和季度财务状况，列出公司的积极发展和潜在担忧，然后结合你对整体金融经济市场的判断，对公司未来一周的股价变化提供预测和分析。" \
    "你的回答语言应为中文。你的回答格式应该如下：\n\n[积极发展]：\n1. ...\n\n[潜在担忧]：\n1. ...\n\n[预测和分析]：\n...\n"



def get_prompt_by_row_new(stock, row):
    """
    Generate prompt for each row in the raw data
    Args:
        stock: str
            stock name
        row: pandas.Series
    Return:
        head: heading prompt
        news: news info
        basics: basic financial info
    """

    week_start_date = row['起始日期'] if isinstance(row['起始日期'], str) else row['起始日期'].strftime('%Y-%m-%d')
    week_end_date = row['结算日期'] if isinstance(row['结算日期'], str) else row['结算日期'].strftime('%Y-%m-%d')
    term = '上涨' if row['结算价'] > row['起始价'] else '下跌'
    chg = map_return_label(row['简化周收益'])
    head = "自{}至{}，{}的股票价格由{:.2f}{}至{:.2f}，涨跌幅为：{}。在此期间的公司新闻如下:\n\n".format(
        week_start_date, week_end_date, stock, row['起始价'], term, row['结算价'], chg)

    news = json.loads(row["新闻"])

    left, right = 0, 0
    filtered_news = []
    while left < len(news):
        n = news[left]

        if left == 0:
            # check first news quality
            if (not(str(n['新闻内容'])[0].isdigit()) and not(str(n['新闻内容'])=='nan') and n['发布时间'][:8] <= week_end_date.replace('-', '')):
                filtered_news.append("[新闻标题]：{}\n[新闻内容]：{}\n".format(n['新闻标题'], n['新闻内容']))
            left += 1

        else:
            news_check = check_news_quality(n, last_n = news[right], week_end_date= week_end_date, repeat_rate=0.5)
            if news_check:
                filtered_news.append("[新闻标题]：{}\n[新闻内容]：{}\n".format(n['新闻标题'], n['新闻内容']))
            left += 1
            right += 1


    basics = json.loads(row['基本面'])
    change_basics={'报告期':basics['REPORT_DATE'],'收入增长QOQ':basics.get('OPERATE_INCOME_QOQ',0),"利润增长QOQ":basics.get('GROSS_PROFIT_QOQ', 0),"债务比例":basics.get('DEBT_ASSET_RATIO',0),"流水比例":basics.get('CURRENT_RATIO',0)}
    bascis=change_basics

    if len(change_basics)>0:
        basics = "如下所列为{}近期的一些金融基本面信息，记录时间为{}:\n\n[金融基本面]:\n\n".format(
            stock, change_basics['报告期']) + "\n".join(f"{k}: {v}" for k, v in change_basics.items() if k != 'period')
    else:
        basics = "[金融基本面]:\n\n 无金融基本面记录"

    return head, filtered_news, basics


def get_all_prompts_new(symbol, min_past_week=1, max_past_weeks=2, with_basics=True):
    """
    Generate prompt. The prompt consists of news from past weeks, basics financial information, and weekly return.
    History news in the prompt is chosen from past weeks range from min_past_week to max_past_week,
    and there is a number constraint on ramdomly selected data (default: up to 5).

    Args:
        symbol: str
            stock ticker
        min_past_week: int
        max_past_week: int
        with_basics: bool
            If true, add basic infomation to the prompt

    Return:
        Prompts for the daterange
    """

    # Load Data
    df = raw_financial_data(symbol, with_basics=with_basics)
    time.sleep(5)
    company_prompt, stock = get_company_prompt_new(symbol)

    prev_rows = []
    all_prompts = []

    for row_idx, row in df.iterrows():

        prompt = ""

        # judge for available history news
        if len(prev_rows) >= min_past_week:

            # randomly set retrieve data of past weeks
            # idx = min(random.choice(range(min_past_week, max_past_weeks+1)), len(prev_rows))
            idx = min(max_past_weeks, len(prev_rows))
            for i in range(-idx, 0):
                # Add Head
                prompt += "\n" + prev_rows[i][0]
                # Add History News (with numbers constraint)
                sampled_news = sample_news(
                    prev_rows[i][1],
                    min(3, len(prev_rows[i][1]))
                )
                if sampled_news:
                    prompt += "\n".join(sampled_news)
                else:
                    prompt += "无有关新闻报告"

        head, news, basics = get_prompt_by_row_new(stock, row)

        prev_rows.append((head, news, basics))

        if len(prev_rows) > max_past_weeks:
            prev_rows.pop(0)

        # set this to make sure there is history news for each considered date
        if not prompt:
            continue

        prediction = map_return_label(row['简化周收益'])

        prompt = company_prompt + '\n' + prompt + '\n' + basics

        prompt += f"\n\n基于在{row['起始日期'].strftime('%Y-%m-%d')}之前的所有信息，让我们首先分析{stock}的积极发展和潜在担忧。请简洁地陈述，分别提出2-4个最重要的因素。大部分所提及的因素应该从公司的相关新闻中推断出来。" \
            f"那么让我们假设你对于下一周({row['起始日期'].strftime('%Y-%m-%d')}至{row['结算日期'].strftime('%Y-%m-%d')})的预测是{prediction}。提供一个总结分析来支持你的预测。预测结果需要从你最后的分析中推断出来，因此不作为你分析的基础因素。"

        all_prompts.append(prompt.strip())

    return all_prompts


if __name__ == "__main__":
    list_dict = {}
    for id, name in index.HSI_dict.items():
        if id=="00700":
            pass
        result = get_all_prompts_new(id)
        list_dict[id] = result

        # Save the data to the file after each iteration
        with open("stock_prompt5.json", "w", encoding="utf-8") as f:
            json.dump(list_dict, f,ensure_ascii=False)

        time.sleep(50) 
    

