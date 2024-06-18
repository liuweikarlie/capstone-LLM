import pandas as pd
import json

with open("/kaggle/input/forecast/stock_prompt2.json", "r", encoding="utf-8") as f:
        data = json.load(f)
for i,value in data.items():
    file_name="/kaggle/input/fork-of-forecast-code-nvida/backup_"+i+'.csv'
    print(file_name)
    df=pd.read_csv(file_name)
    df['prompt']=data[i]
    df = df.rename(columns={'result': 'answer'})
    print(df)
    df[["prompt",'answer']].to_csv("gpt_"+i+'.csv')