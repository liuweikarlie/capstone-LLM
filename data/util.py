import requests
import pandas as pd
import time

# rebuild from AKShare

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


def turn_page(start_time,data):
  print("hello")
  print(data.iloc[0]['发布时间'])
  print(start_time)
  if data.iloc[0]['发布时间']>start_time:
    print("Yes")
    return True
  else:
    return False

  


def get_news(symbol,start_date):
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