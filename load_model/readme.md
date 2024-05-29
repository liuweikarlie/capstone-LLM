# Load Model

After the fine-tunning model, we actually got the model with two parts:
- llama2-7b-hf
- lora adapter (file)-- peft

## Step 1
We fisrt need to merge this two model together. So in the `lora-gpt.py ` we load the model and then merge them together. Save the merge model and tokenizer.

> If you use the Autodl platform to load the model, remember to swith to save the hugging face cache in the autodl-tmp file and also open the "学术加速“
```bash

export HF_HOME=/root/autodl-tmp/cache/
source /etc/network_turbo

```

After getting the model, you will have two folders (merge,token), inside the folder it includes the safetensors, move the token related file to the merge folder. 

> If you use the Autodl, please copy your merge file to autodl-fs



## Step 2 Turn the file to gguf

Since the model size is really large and everytime i need to use the huggingface pre-train model to load it, which is take long time. 

So, we need to save the model in one file to easy implement. `llama.cpp` is a solution to turn the model to one file. 

```bash 

#step 1
git clone https://github.com/ggerganov/llama.cpp.git

# step 2
cd llama.cpp

#step 3
pip install -r requirements.txt

# Step 4 -if you use CUDA
make LLAMA_CUBLAS=1

# Step 4 - if you use cpu
make

#if you run in window, please see this : https://blog.csdn.net/road_of_god/article/details/133901390 or https://zhuanlan.zhihu.com/p/652963043

# step 5 - convert model to gguf format
python ./convert.py <your_model_path> — outfile <output_name>.gguf



```
> autodl User, if you have constrain on your memeory, remember to move your previous `merge` model to the `autodl-fs` or `autodl-tmp`. For my case, the output of the gguf file size is 24 GB, it's really large. 



## Step 3 Quantize to 4b 

Since the file is too large, we need to quantize it to 4b. 

```bash
./quantize <model_output_in_step2>.gguf <output_file_name>.gguf Q4_K

```
The file would decrease from 24 GB to 3GB. 


## Launch 
```bash
./main -m <model_name>.gguf --interactive

#or
./main -m <model_name>.gguf --color -f prompts/alpaca.txt -ins -c 2048 --temp 0.2 -n 256 --repeat_penalty 1.3
```

## Server

```bash
./server -m <your_model>.gguf -ngl 100
```
You can check in the localhost port 8080
### Reference

- https://blog.csdn.net/god_zzZ/article/details/130328307
- https://medium.com/@kevin.lopez.91/simple-tutorial-to-quantize-models-using-llama-cpp-from-safetesnsors-to-gguf-c42acf2c537d
- 


## Problem
- sometime the model would not have result
- generate speed is slow 
    - https://cloud.tencent.com/developer/news/1262045
    - https://www.qbitai.com/2023/09/84399.html
