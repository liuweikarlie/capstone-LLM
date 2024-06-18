import pandas as pd
import re
import datasets
from datasets import Dataset

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
def gpt4_to_llama(symbol, with_basics=True):
    
    csv_file = '/kaggle/input/translate-nividia/translate_'+symbol+'.csv'
    
    df = pd.read_csv(csv_file)
    SYSTEM_PROMPT = "You are an experienced stock market analyst. Your task is to analyze the company's recent news and quarterly financial condition over the past few weeks, and list the positive developments and potential concerns for the company. Then, based on your overall judgment of the financial and economic market, you need to provide a forecast and analysis of the company's stock price change for the upcoming week.\n\nYour answer should be in English,and [Forecast and Analysis] part should be more than 200 words, and the format should be as follows:\n\n[Positive Developments]:\n1. ...\n\n[Potential Concerns]:\n1. ...\n\n[Forecast and Analysis]:\n ...\n"

    
    prompts, answers, periods, labels = [], [], [], []
    count=0
    
    for i, row in df.iterrows():
        
        prompt, answer = row['translate'], row['answer']
        check=True
        res = re.search(r"let's assume your prediction for next week \((.*)\) is ((:?up|down) by .*%).", prompt)

        if res==None:
            check=False
            res = re.search(r"let's assume your prediction for next week ([\d-]+ to [\d-]+) is ((:?up|down) by .*%).", prompt)
       
        try:
            period, label = res.group(1), res.group(2)
        except:
            count=count+1
            print(count)
            continue
        
      
            
            
            
        
        if check==False:
            prompt = re.sub(
            r"Then let's assume your prediction for next week ([\d-]+ to [\d-]+) is (up|down) by ((:?.*)%). Provide a summary analysis to support your prediction. The prediction result need to be inferred from your analysis at the end, and thus not appearing as a foundational factor of your analysis.", 
            f"Then make your prediction of the {symbol} stock price movement for next week ({period}). Provide a summary analysis to support your prediction.",
            prompt
        )
            check=True
            
        
        else:
            prompt = re.sub(
            r"Then let's assume your prediction for next week \((.*)\) is (up|down) by ((:?.*)%). Provide a summary analysis to support your prediction. The prediction result need to be inferred from your analysis at the end, and thus not appearing as a foundational factor of your analysis.", 
            f"Then make your prediction of the {symbol} stock price movement for next week ({period}). Provide a summary analysis to support your prediction.",
            prompt
        )
        try:
            answer = re.sub(
                r"\[Forecast and Analysis\]:\s*",
                f"[Forecast and Analysis]:\nForecast: {label.capitalize()}\nAnalysis: ",
                answer
            )
        except Exception:
            print(symbol, i)
            print(label)
            print(answer)
            continue
            
        new_system_prompt = SYSTEM_PROMPT.replace(':\n...', '\nForecast: ...\nAnalysis: ...')
#         new_system_prompt = SYSTEM_PROMPT.replace(':\n...', '\nPrediction: {Up|Down} by {1-2|2-3|3-4|4-5|5+}%\nAnalysis: ...')
        
        prompt = B_INST + B_SYS + new_system_prompt + E_SYS + prompt + E_INST
        
        prompts.append(prompt)
        answers.append(answer)
        periods.append(period)
        labels.append(label)
        
    return {
        "prompt": prompts,
        "answer": answers,
        "period": periods,
        "label": labels,
    }


def create_dataset(symbol_list, train_ratio=0.8, with_basics=True):

    train_dataset_list = []
    test_dataset_list = []

    for symbol in symbol_list:

        data_dict = gpt4_to_llama(symbol, with_basics)
#         print(data_dict['prompt'][-1])
#         print(data_dict['answer'][-1])
        symbols = [symbol] * len(data_dict['label'])
        data_dict.update({"symbol": symbols})
        #print(data_dict)

        dataset = Dataset.from_dict(data_dict)
        train_size = round(train_ratio * len(dataset))

        train_dataset_list.append(dataset.select(range(train_size)))
        test_dataset_list.append(dataset.select(range(train_size, len(dataset))))
    
    print(test_dataset_list)
    print(train_dataset_list)

    train_dataset = datasets.concatenate_datasets(train_dataset_list)
    test_dataset = datasets.concatenate_datasets(test_dataset_list)

    dataset = datasets.DatasetDict({
        'train': train_dataset,
        'test': test_dataset
    })
    
    return dataset
   




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
symbol_list = list(HSI_dict.keys())

dataset = create_dataset(symbol_list)
dataset.save_to_disk("data/stock_forecast")
