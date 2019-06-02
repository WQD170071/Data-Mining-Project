import pandas as pd
import re


#load data
a = pd.read_csv(r"https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/news_20190318.csv")
b = pd.read_csv(r"https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/news_20190327.csv")

#merge data by columns
merge_news = a.append(b)

#remove duplicates of news
merge_news['extract_code'] = merge_news['code'].str[-4:]
news = merge_news.sort_values('extract_code',ascending=True).drop_duplicates(['news'],keep='first')

#extract date
news['extracted_date']=news.date.str.extract(r'(\d{2}\s[A-Z][a-z]{2},\s\d{4})')

#remove news that before 25 Feb 2019
news['extracted_date']=pd.to_datetime(news['extracted_date'])
res = news[~(news['extracted_date']<'25 Feb, 2019')]

res.to_csv(r"News_processed.csv")
res
