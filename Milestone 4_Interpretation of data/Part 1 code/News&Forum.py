# Import packages
import pandas as pd
import numpy as np
import os

# ## -- Part 1 --

# ### News & Forum of Stock

# News data
# Read in News csv file 
news = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/processed_news.csv')
# news

# Count the total news base on stock code and sort in descending order, to see which stock is more popular
news1 = news.groupby(["extract_code"], as_index=False)['news'].count()
news1 = news1.sort_values(by=['news'],ascending=(False))
news1 = news1.rename(columns={'extract_code':'code'})
news_count = pd.merge(news1,sector,how='left',on='code')
news_count.head(50)


# Forum data
Forum = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Comment.csv')
# Forum

Forum1 = Forum.groupby(['Stock Code'], as_index=False)['Hot'].sum()
Forum1 = Forum1.sort_values(by=['Hot'],ascending=(False))
Forum1 = Forum1.rename(columns={'Stock Code':'code'})
Forum_count = pd.merge(Forum1,sector,how='left',on='code')
Forum_count.head(50)

