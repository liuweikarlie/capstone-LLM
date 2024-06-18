# Readme

## File Explain (logic ordering)
- `index.py` store the ticker of the stock
- `scrap_data.py`
   - get stock return
   - get company news
   - get company fundemental info
   - get company profile
   - convert it to prompt for feed in gpt
- `gpt.py / nvida.py` (in here our result use the nvida llama3 70b api for get the forecast result）
- `nvida_result_merge.py`
- `translate_nivida.py` (translate the prompt to english)
- `formulate_data.py` (convert the data format to our fine-tune format)
- tool
  - `bing_news.py` bing api to get news
  - `util.py` (rewrite the akshare library function)

## News
- langchain 爬虫： https://www.tizi365.com/article/107.html
