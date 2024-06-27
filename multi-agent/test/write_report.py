import os
import json
from autogen import ConversableAgent

# put the fine-tune model to the LM studio, get the api key and base url , rewrite the config_list
gpt_config_list={"config_list":[
     {
    'model': 'llama3-8b-8192', #model here is your model name in the LM studio
    'api_key': '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',
    'base_url': "https://api.groq.com/openai/v1",}
],
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
        chat_result=self.review_agent.initiate_chat(self.write_agent,message="Jack, please write an equity research report for this company: "+self.report_keypoint,max_turn=2)
        return chat_result




if __name__=="__main__":
    report_keypoint='''Tencent'''
    report_writer=ReportWriteReview(report_keypoint)
    chat_result=report_writer.start_task()
    print(chat_result)