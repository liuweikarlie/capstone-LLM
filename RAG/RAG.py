
from langchain.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain
from CustomLLM import CustomLLM
from langchain.embeddings import HuggingFaceEmbeddings
import re



class Rag:

    def __init__(self,path):
        self.llm=CustomLLM()
        self.path=path


    def generate(self,question):
        self.q=question
        if self.q:
            model_name = "sentence-transformers/all-mpnet-base-v2"
            model_kwargs = {"device": "cuda"}
            embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
            db = Chroma(persist_directory=self.path, embedding_function=embeddings) 
            doc = db.similarity_search(self.q)
            context = doc[0].page_content


            instruction="Utilize your financial knowledge, give your answer or opinion to the input question or subject . Answer format is not limited. Here is the reference resource:"+context


            prompt_template = """
            {instruction}
            Question: {question}
            """
            prompt = PromptTemplate(template=prompt_template, input_variables=["instruction", "question"])

            query_llm = LLMChain(llm=self.llm, prompt=prompt)
            response = query_llm.run({"instruction": instruction, "question": self.q})
            print(type(response))
            response=re.findall(r"Answer:\s*(.*)", response)

            return response