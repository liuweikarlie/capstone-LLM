import json
from openai import AzureOpenAI
import time
import pandas as pd

# https://oai.azure.com/portal
# Read the JSON file



# Access the data
SYSTEM_PROMPT = "你是一名经验丰富的股票市场分析师。你的任务是根据公司在过去几周内的相关新闻和季度财务状况，列出公司的积极发展和潜在担忧，然后结合你对整体金融经济市场的判断，对公司未来一周的股价变化提供预测和分析。" \
    "你的回答语言应为中文。你的回答格式应该如下：\n\n[积极发展]：\n1. ...\n\n[潜在担忧]：\n1. ...\n\n[预测和分析]：\n...\n"


def question_generate_from_llm(symbol,df):
    error = None
    api_key = "api"
    client = AzureOpenAI(
        api_key=api_key,
        api_version="2023-12-01-preview",
        azure_endpoint="https://gpgpt.openai.azure.com/"
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
                        model="test2",
                        messages=message
                    )
                    result.append(completion.choices[0].message.content)
                    print("current index:", index)
                    break
                except Exception as e:
                    error = e
                    # Handle rate limit exceeded error
                    if "code" in e.error or e.error["code"] == 429:
                        # Sleep for 60 seconds and retry after rate limit reset
                        time.sleep(60)
                        print("Error:", e)
                        print("Current index:", index)
                        break
                    else:
                        # Handle other exceptions
                        print("Error:", e)
                        break

            if error is not None:
                print("Current index of the DataFrame is:", index)
    except KeyboardInterrupt:
            print("Execution interrupted.")
    df=pd.DataFrame({"result":result})
    df.to_csv("backup.csv")
    return result


if __name__ == "__main__":
    with open("stock_prompt.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data['00700'][3])

 

