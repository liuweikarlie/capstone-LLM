
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

text = '''Today Apple is reporting revenue of $90.8 billion for the March quarter in 2024, including an all-time revenue record in Services. During the quarter, we were thrilled to launch Apple Vision Pro and to show the world the potential that spatial computing unlocks. We’re also looking forward to an exciting product announcement next week and an incredible Worldwide Developers Conference next month. As always, we are focused on providing the very best products and services for our customers, and doing so while living up to the core values that drive us.'''

# Specify the file path

def convert_file(text,name):
    file_path = name+'.txt'

    # Write the text to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"The text has been stored in the file: {file_path}")
    
text1='''CUPERTINO, CALIFORNIA Apple today announced financial results for its fiscal 2024 first quarter ended December 30, 2023. The Company posted quarterly revenue of $119.6 billion, up 2 percent year over year, and quarterly earnings per diluted share of $2.18, up 16 percent year over year.
“Today Apple is reporting revenue growth for the December quarter fueled by iPhone sales, and an all-time revenue record in Services,” said Tim Cook, Apple’s CEO. “We are pleased to announce that our installed base of active devices has now surpassed 2.2 billion, reaching an all-time high across all products and geographic segments. And as customers begin to experience the incredible Apple Vision Pro tomorrow, we are committed as ever to the pursuit of groundbreaking innovation — in line with our values and on behalf of our customers.”
“Our December quarter top-line performance combined with margin expansion drove an all-time record EPS of $2.18, up 16 percent from last year,” said Luca Maestri, Apple’s CFO. “During the quarter, we generated nearly $40 billion of operating cash flow, and returned almost $27 billion to our shareholders. We are confident in our future, and continue to make significant investments across our business to support our long-term growth plans.”
Apple’s board of directors has declared a cash dividend of $0.24 per share of the Company’s common stock. The dividend is payable on February 15, 2024 to shareholders of record as of the close of business on February 12, 2024.
Based on the Company’s fiscal calendar, the Company’s fiscal 2024 first quarter had 13 weeks, while the Company’s fiscal 2023 first quarter had 14 weeks.
Apple will provide live streaming of its Q1 2024 financial results conference call beginning at 2:00 p.m. PT on February 1, 2024 at apple.com/investor/earnings-call. The webcast will be available for replay for approximately two weeks thereafter.'''

text2='''Earnings Release FY24 Q2
Microsoft Cloud Strength Drives Second Quarter Results

REDMOND, Wash. — January 30, 2024 — Microsoft Corp. today announced the following results for the quarter ended December 31, 2023, as compared to the corresponding period of last fiscal year:

·        Revenue was $62.0 billion and increased 18% (up 16% in constant currency)

·        Operating income was $27.0 billion and increased 33%, and increased 25% non-GAAP (up 23% in constant currency)

·        Net income was $21.9 billion and increased 33%, and increased 26% non-GAAP (up 23% in constant currency)

·        Diluted earnings per share was $2.93 and increased 33%, and increased 26% non-GAAP (up 23% in constant currency)

Microsoft completed the acquisition of Activision Blizzard, Inc. (“Activision”) on October 13, 2023. Financial results from the acquired business are reported in the More Personal Computing segment.

"We’ve moved from talking about AI to applying AI at scale," said Satya Nadella, chairman and chief executive officer of Microsoft. "By infusing AI across every layer of our tech stack, we’re winning new customers and helping drive new benefits and productivity gains across every sector.”

“Strong execution by our sales teams and partners drove Microsoft Cloud revenue to $33.7 billion, up 24% (up 22% in constant currency) year-over-year,” said Amy Hood, executive vice president and chief financial officer of Microsoft.

The following table reconciles our financial results reported in accordance with generally accepted accounting principles (GAAP) to non-GAAP financial results. Additional information regarding our non-GAAP definition is provided below. All growth comparisons relate to the corresponding period in the last fiscal year.'''
text3='''SEATTLE--(BUSINESS WIRE)-- Starbucks Corporation (Nasdaq: SBUX) today reported financial results for its 13-week fiscal second quarter ended March 31, 2024. GAAP results in fiscal 2024 and fiscal 2023 include items that are excluded from non-GAAP results. Please refer to the reconciliation of GAAP measures to non-GAAP measures at the end of this release for more information.

Q2 Fiscal 2024 Highlights

Global comparable store sales declined 4%, driven by a 6% decline in comparable transactions, partially offset by a 2% increase in average ticket
North America and U.S. comparable store sales declined 3%, driven by a 7% decline in comparable transactions, partially offset by a 4% increase in average ticket
International comparable store sales declined 6%, driven by a 3% decline in both comparable transactions and average ticket; China comparable store sales declined 11%, driven by an 8% decline in average ticket and a 4% decline in comparable transactions
The company opened 364 net new stores in Q2, ending the period with 38,951 stores: 52% company-operated and 48% licensed
At the end of Q2, stores in the U.S. and China comprised 61% of the company’s global portfolio, with 16,600 and 7,093 stores in the U.S. and China, respectively
Consolidated net revenues declined 2%, to $8.6 billion, or a 1% decline on a constant currency basis
GAAP operating margin contracted 240 basis points year-over-year to 12.8%, primarily driven by deleverage, incremental investments in store partner wages and benefits, increased promotional activities, lapping the gain on the sale of Seattle's Best Coffee brand, as well as higher general and administrative costs primarily in support of Reinvention. This decline was partially offset by pricing and in-store operational efficiencies.
Non-GAAP operating margin contracted 150 basis points year-over-year to 12.8%, or contracted 140 basis points on a constant currency basis
GAAP earnings per share of $0.68 declined 14% over prior year Non-GAAP earnings per share of $0.68 declined 8% over prior year, or declined 7% on a constant currency basis
Starbucks Rewards loyalty program 90-day active members in the U.S. totaled 32.8 million, up 6% year-over-year
“In a highly challenged environment, this quarter's results do not reflect the power of our brand, our capabilities or the opportunities ahead,” commented Laxman Narasimhan, chief executive officer. “It did not meet our expectations, but we understand the specific challenges and opportunities immediately in front of us. We have a clear plan to execute and the entire organization is mobilized around it. We are very confident in our long-term and know that our Triple Shot Reinvention with Two Pumps strategy will deliver on the limitless potential of this brand,” Narasimhan added.

“While it was a difficult quarter, we learned from our own underperformance and sharpened our focus with a comprehensive roadmap of well thought out actions making the path forward clear,” commented Rachel Ruggeri, chief financial officer. “On this path, we remain committed to our disciplined approach to capital allocation as we navigate this complex and dynamic environment,” Ruggeri added.'''
convert_file(text,"2nd_Apple")
convert_file(text1,"1nd_Apple")
convert_file(text2,"1nd_Microsoft")
convert_file(text3,"2nd_Starbucks")




import glob


# Specify the folder path where the .txt files are located
folder_path = "/kaggle/working/"

# Use glob to get the list of .txt files in the folder
txt_files = glob.glob(folder_path + "/*.txt")

for i in txt_files:
    loader = TextLoader(i,
                        encoding="utf8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    all_splits = text_splitter.split_documents(documents)
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cuda"}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
    vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory="chroma_db")