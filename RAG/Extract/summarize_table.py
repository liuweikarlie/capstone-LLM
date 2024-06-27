from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from clean_data import *
from Extract_pdf import *
import os
import json

def summarize_main(folderpath):
    prompt_text = """
        "Instruction":You are an assistant tasked with summarizing tables and texts. \
        These summaries will be embedded and used to retrieve the raw text or table elements. \
        Give a concise summary of the table or text that is well optimized for retrieval. DOn't start with like "Sure.Here's the summary of something". Directly give me the output.\
        Table or text: {element} """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Summary chain
    model = ChatOllama(model="llama3")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    # Specify the path to your PDF file
    #folderpath= "/home/bsl/pdf"
    result = {
        "PDF": [],
        "context": [],
        "table":[]
    }
    pdf_id = 1

    # text_summaries_results = []
    table_summaries_results=[]
    for filename in os.listdir(folderpath):
        if filename.endswith(".pdf"):

            result["PDF"].append({
                "pdf_id": pdf_id,
                "path": filename
            })
            # Get elements
            raw_pdf_elements = extract_pdf_elements(folderpath, filename)
            # Get text, tables
            texts, tables = categorize_elements(raw_pdf_elements)
            texts = clean_text(texts)
            # # Optional: Enforce a specific token size for texts
            for text in texts:
                result["context"].append({
                    "id": len(result["context"]) + 1,
                    "pdf_id": pdf_id,
                    "content": text
                })

            for table in tables:
                result["table"].append({
                    "id": len(result["table"]) + 1,
                    "html": table.to_dict()['metadata']['text_as_html'],
                    "summary": ""  # Provide a summary or remove this field
                })
            str_tables = [str(table) for table in tables]
            # Apply to tables
            table_summaries = summarize_chain.batch(str_tables, {"max_concurrency": 5})
            table_summaries_results.append(table_summaries)
            # text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})
            # text_summaries_results.append(text_summaries)
            pdf_id += 1

    return result,table_summaries_results

def summarize_table_final(table_summaries_results, result):
    temptable = sum(table_summaries_results,[])
    for summary,table in zip(temptable,result["table"]):
        table['summary'] = summary
    with open("pdf_extraction_result_text_and_table.json", "w") as f:
        json.dump(result, f, indent=4) 


if __name__=="__main__":
    folderpath = "/home/bsl/pdf"
    result,table_summaries_results = summarize_main(folderpath)
    summarize_table_final(table_summaries_results,result)
    print("Done!")