#!/usr/bin/env python
# coding: utf-8

# Import packages
import pandas as pd
import numpy as np
import os

# ## -- Part 1 --

# ### News of Stock

# Read in News csv file 
news = pd.read_csv('processed_news.csv')
news

# Count the total news base on stock code and sort in descending order, to see which stock is more popular
news1 = news.groupby(["extract_code"], as_index=False)['news'].count()
news1 = news1.sort_values(by=['news'],ascending=(False))
news1 = news1.rename(columns={'extract_code':'code'})
news_count = pd.merge(news1,sector,how='left',on='code')
news_count.head(50)


