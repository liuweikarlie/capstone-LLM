import json
from openai import OpenAI
import time
import pandas as pd

# https://oai.azure.com/portal
# Read the JSON file


#llama3-70b-instruct
# Access the data
SYSTEM_PROMPT = "You are an experienced stock market analyst. Your task is to analyze the company's recent news and quarterly financial condition over the past few weeks, and list the positive developments and potential concerns for the company. Then, based on your overall judgment of the financial and economic market, you need to provide a forecast and analysis of the company's stock price change for the upcoming week.\n\nYour answer should be in English,and [Forecast and Analysis] part should be more than 200 words, and the format should be as follows:\n\n[Positive Developments]:\n1. ...\n\n[Potential Concerns]:\n1. ...\n\n[Forecast and Analysis]:\n ...\n"

def question_generate_from_llm(symbol,df):
    error = None
    client = OpenAI(
      base_url = "https://integrate.api.nvidia.com/v1",
      api_key = "api"
    )
    result = []
    token_count = 0
    try:
        for index in range(len(df)):

            message = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": df[index]}
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
                    
                    print(string_res)
                    result.append(string_res)
                    #print("current index:", index)
                    break
                except Exception as e:
                    error = e
                    print(error)

    except KeyboardInterrupt:
            print("Execution interrupted.")
    df=pd.DataFrame({"result":result})
    df.to_csv("backup_"+symbol+".csv")
    return result


if __name__ == "__main__":
    with open("/kaggle/input/forecast-tech/stock_prompt5.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for i,value in data.items():
        result=question_generate_from_llm(i,data[i])
        
    
        print(result)
 

