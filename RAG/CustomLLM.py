from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer,AutoModelForCausalLM
import transformers
from torch import cuda, bfloat16
from peft import PeftModel
import re

#https://github.com/davidhandsome86/LLM_RAG/blob/main/Rag.py
#https://blog.csdn.net/qq_39749966/article/details/136108973

class CustomLLM(LLM):
    tokenizer : AutoTokenizer = None
    model: AutoModelForCausalLM = None
   

    
    
    def __init__(self):
        super().__init__()
        hf_auth="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"
        model_id='meta-llama/Llama-2-7b-hf'
        perft_model='Andy1124233/capstone_fingpt'

        bnb_config = transformers.BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=bfloat16
            )
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            device_map='auto',
            token=hf_auth,
            quantization_config=bnb_config,
            offload_folder="/kaggle/working/"
        )

   
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True,token=hf_auth)

        self.tokenizer.padding_side = "left"
        if not self.tokenizer.pad_token or self.tokenizer.pad_token_id == self.tokenizer.eos_token_id:
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        self.model = PeftModel.from_pretrained(self.model,perft_model,offload_folder="/kaggle/working/")

        self.model = self.model.eval()
        print("Model loaded successfully!")
  

    def _llm_type(self) -> str:
        return "custom" 

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        callbacks: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
        ) -> str:
        prompt1 = 'Instruction: {instruction}\nInput: {input}\nAnswer: '.format(
            input=prompt, 
            instruction="Utilize your financial knowledge, give your answer or opinion to the input question or subject . Answer format is not limited."
        )
        inputs = self.tokenizer(
            prompt1, return_tensors='pt',
            padding=True, max_length=4096,
            return_token_type_ids=False
        )
        inputs = {key: value.to(self.model.device) for key, value in inputs.items()}
        res = self.model.generate(
            **inputs, max_length=4096, do_sample=False,
            eos_token_id=self.tokenizer.eos_token_id
        )
        output = self.tokenizer.decode(res[0], skip_special_tokens=True)
        # output=re.findall(r"Answer:\s*(.*)", output)

       
        return output