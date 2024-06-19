import os
import json
from autogen import ConversableAgent

# put the fine-tune model to the LM studio, get the api key and base url , rewrite the config_list
gpt_config_list={"config_list":[{
    'model': 'test', #model here is your model name in the LM studio
    'api_key': 'api',
    'base_url': "https://gpgpt.openai.azure.com/",
    'api_version': '2024-02-15-preview',
    'api_type': 'azure',
}],
"cache_seed":None,
}


class ReportWriteReview():
    def __init__(self,report_keypoint):
        self.write_agent = ConversableAgent(
            "Jack (Analyst)",
            llm_config=gpt_config_list,
            system_message='''
            Your name is Jack, You are an equity research writer. Your task is to write a report on the company's financial performance and future prospects based on the provided company analysis brainstoming point information provided from your director. Your report should include a brief introduction of company, analysis of company's recent financial performance, how the recent event and news influence stock price and an analysis of the company's future prospects and risk. Your report should be written in English and be at least 300 words long. Also if receiving feedback from your director, you should be able to revise the report based on the feedback. The output should always follow the format: [Introduction of company]/n.../n/n[Analysis based on news and industry perspect]/n/n.../n/n[Analysis on Financial Report]/n/n.../n/n[Risk]/n/n.../n/n[Forecast]/n/n.../n/n[Recommendation]/n/n.../n
            '''
            )
        self.review_agent= ConversableAgent(

            "Emma(Director)",
            llm_config=gpt_config_list,
            system_message='''
            Your name is Emma, You are an professional equity research director. Your task is to review the report written by your analyst and provide feedback on the report. Your feedback should include detail suggestions for improvement, additional information that should be included, and any corrections that need to be made. Your feedback should be written in English and be at least 100 words long.
            '''
        )
        self.report_keypoint=report_keypoint

    def start_task(self):
        chat_result=self.review_agent.initiate_chat(self.write_agent,message="Jack, please write an equity research report for this company based on below information: "+self.report_keypoint,max_turn=3)
        return chat_result




if __name__=="__main__":
    report_keypoint='''[公司介绍]:\n\n腾讯控股是一家在软件服务行业的领先实体，自2004年06月16日成立并公开交易。截止今天，腾讯控股的总市值为3572736890364.0人民币，总股本数为9406890180.0，流通市值为3572736890364.0人民币，流通股数为9406890180.0。\n\n腾讯控股主要在中国运营，以股票代码00700在交易所进行交易。\n\n自2024-01-07至2024-01-14，腾讯控股的股票价格由288.80下跌至285.00，涨跌幅为：下跌1-2%。在此期间的公司新闻如下:\n\n[新闻标题]：腾讯控股00700.HK)连续33日回购 累计回购5978.00万股\n[新闻内容]：证券时报·数据宝统计，腾讯控股在港交所公告显示，1月8日以每股285.600港元至294.400港元的价格回购174.00\n\n如下所列为腾讯控股近期的一些金融基本面信息，记录时间为2023-12-31 00:00:00:\n\n[金融基本面]:\n\n报告期: 2023-12-31 00:00:00\n收入增长QOQ: 1.710497968345\n利润增长QOQ: 5.675512948548\n债务比例: 44.6071823926\n流水比例: 1.472201319298\n\n基于在2024-01-14之前的所有信息，让我们首先分析腾讯控股的积极发展和潜在担忧。请简洁地陈述，分别提出2-4个最重要的因素。大部分所提及的因素应该从公司的相关新闻中推断出来。那么让我们假设你对于下一周(2024-01-14至2024-01-21)的预测是下跌超过5%。提供一个总结分析来支持你的预测。预测结果需要从你最后的分析中推断出来，因此不作为你分析的基础因素。'''
    report_writer=ReportWriteReview(report_keypoint)
    chat_result=report_writer.start_task()
    print(chat_result)