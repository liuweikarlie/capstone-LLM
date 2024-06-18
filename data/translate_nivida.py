import pandas as pd
from openai import OpenAI

def question_generate_from_llm(symbol,df):
    error = None
#     api_key = "ebc76beedf89486382e773d3b4cf0b10"
    client = OpenAI(
      base_url = "https://integrate.api.nvidia.com/v1",
      api_key = "api"
    )
    result = []
    token_count = 0
    try:
        for index in range(len(df)):
            raw_text1='''Raw text1: "[公司介绍]:\n\n腾讯控股是一家在软件服务行业的领先实体，自2004年06月16日成立并公开交易。截止今天，腾讯控股的总市值为3572736890364.0人民币，总股本数为9406890180.0，流通市值为3572736890364.0人民币，流通股数为9406890180.0。\n\n腾讯控股主要在中国运营，以股票代码00700在交易所进行交易。\n\n自2024-01-07至2024-01-14，腾讯控股的股票价格由288.80下跌至285.00，涨跌幅为：下跌1-2%。在此期间的公司新闻如下:\n\n[新闻标题]：腾讯控股00700.HK)连续33日回购 累计回购5978.00万股\n[新闻内容]：证券时报·数据宝统计，腾讯控股在港交所公告显示，1月8日以每股285.600港元至294.400港元的价格回购174.00\n\n如下所列为腾讯控股近期的一些金融基本面信息，记录时间为2023-12-31 00:00:00:\n\n[金融基本面]:\n\n报告期: 2023-12-31 00:00:00\n收入增长QOQ: 1.710497968345\n利润增长QOQ: 5.675512948548\n债务比例: 44.6071823926\n流水比例: 1.472201319298\n\n基于在2024-01-14之前的所有信息，让我们首先分析腾讯控股的积极发展和潜在担忧。请简洁地陈述，分别提出2-4个最重要的因素。大部分所提及的因素应该从公司的相关新闻中推断出来。那么让我们假设你对于下一周(2024-01-14至2024-01-21)的预测是下跌超过5%。提供一个总结分析来支持你的预测。预测结果需要从你最后的分析中推断出来，因此不作为你分析的基础因素。"，'''
            translate_text1='''Translate text1: "[Company Introduction]:\n\nTencent is a leading entity in the software services sector. Incorporated and publicly traded since June 16, 2004, the company has established its reputation as one of the key players in the market. As of today, Tencent has a market capitalization of 3,572,736,890,364.00 in RMB, with 9,406,890,180.00 shares outstanding." "\n\nnTencent operates primarily in the China, trading under the ticker 00700.\n\nFrom 2024-01-07 to 2024-01-14, Tencent's stock price is down from 288.80 to 285.00. Company news during this period are listed below:\n\n[Headline]:Tencent Holdings (00700.HK) buybacked for 33 consecutive days，accumulated 59.78 million shares repurchased\n[Content]:Securities Times - Data Treasure statistics, Tencent Holdings in the Hong Kong Stock Exchange announcement shows that on January 8 at a price of HK$ 285.600 to HK$ 294.400 per share to buy back 174.00 \n\n The following are listed as some of Tencent Holdings recent financial fundamentals information, the record time is 2023-12-31 00:00:00\n\nSome recent basic financials of Tencent, reported at 2023-12-31 00:00:00, are presented below:\n\n[Basic Financials]:\n\nReporting Period: 2023-12-31 00:00:00\nRevenue Growth QOQ: 1.710497968345\nProfit Growth QOQ: 5.675512948548\nDebt Ratio: 44.6071823926\nCurrent Ratio: 1.472201319298\n\nBased on all the information before 2024-01-14, let's first analyze the positive developments and potential concerns for Tencent. Come up with 2-4 most important factors respectively and keep them concise. Most factors should be inferred from company related news.Then let's assume your prediction for next week 2024-01-14 to 2024-01-21 is down by 5%. Provide a summary analysis to support your prediction. The prediction result need to be inferred from your analysis at the end, and thus not appearing as a foundational factor of your analysis.",'''
            template='''Template: "[Company Introduction]:\n\n{company_name} is a leading entity in the {Industry} sector. Incorporated and publicly traded since {ipodate}, the company has established its reputation as one of the key players in the market. As of today, {company_name} has a market capitalization of {marketCapitalization:.2f} in HKD, with {shareOutstanding:.2f} shares outstanding." "\n\n{company_name} operates primarily in the China, trading under the ticker {ticker_id}.\n\nFrom {start_time} to {end_time}, {company_name}'s stock price is {up/down} from {:.2f} to {:.2f}. Company news during this period are listed below:\n\n[Headline]:{translate headline}\n[Content]:{translate content}\n\nSome recent basic financials of {company_name}, reported at {report_date}, are presented below:\n\n[Basic Financials]:\n\nReporting Period: {report_time}\nRevenue Growth QOQ: {revenue_growth_qoq_data}\nProfit Growth QOQ: {profit_growth_qoq}\nDebt Ratio: {debt_ratio_data}\nCurrent Ratio: {current_ratio_data}\n\nBased on all the information before {end_date}, let's first analyze the positive developments and potential concerns for {company}. Come up with 2-4 most important factors respectively and keep them concise. Most factors should be inferred from company related news.Then let's assume your prediction for next week {start_date} to {end_date} is {up/down} by {percentage change}. Provide a summary analysis to support your prediction. The prediction result need to be inferred from your analysis at the end, and thus not appearing as a foundational factor of your analysis."'''
            raw_text2='''Raw text2:'''+df[index]
            all_prompt=raw_text1+translate_text1+template+raw_text2+"Translate text2: "
            message = [
                {"role": "system", "content": "please follow the rule"},
                {"role": "user", "content": all_prompt}
            ]
            # token_count = len(prompt.split(" ")) + token_count

            # if token_count > 3000:
            #     time.sleep(5)
            #     token_count = 0
            while True:
                try:
                    completion = client.chat.completions.create(
                          model="meta/llama3-70b-instruct",
                          messages=message,
                          temperature=0.5,
                          top_p=1,
                          max_tokens=1024,
                          stream=True
                        )
                    string_res=''
                    for chunk in completion:
                          if chunk.choices[0].delta.content is not None:
                                string_res=string_res+chunk.choices[0].delta.content
                                
                    
                    start_index = string_res.find("[Company Introduction]")
                    extracted_text = string_res[start_index:]
                    print(extracted_text)
                    result.append(extracted_text)
                    #print("current index:", index)
                    break
                except Exception as e:
                    error = e
                    print(error)

    except KeyboardInterrupt:
            print("Execution interrupted.")
    df=pd.DataFrame({"translate":result})
    df.to_csv("backup_"+symbol+".csv")
    return result


if __name__ == "__main__":
    HSI_dict = {
        "00700": "Tencent",
        "00941": "China Mobile",
        "09988": "Alibaba",
        "00939": "CCBC",
        "00005": "HSBC",
        "00883": "CNOOC",
        "03690": "Meituan",
        "01299": "AIA",
        "09999": "NetEase",
        "01398": "ICBC"
    }

    for index,value in HSI_dict.items():
        file=pd.read_csv("/kaggle/input/nvidia-forecast1-result/gpt_"+index+".csv")
        translate_raw=file['prompt']
        result=question_generate_from_llm(index,translate_raw)
        file['translate']=result
        file.to_csv("translate_"+index+'.csv')
    
    
    
    