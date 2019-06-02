# Import packages
import pandas as pd
import numpy as np
import os

# ## -- Part 1 --

###########################################################################

# ### Financial Report (PDF)

# Read in PDF csv file
PDF = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/PDF_summary.csv')
# PDF

# Read in sector csv file
sector = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Stock_Sector.csv')

# There are some value in the 'code' variable that need to be reformat
PDF['code'] = PDF['code'].str.replace('.0','').astype(str)

# Calculate the Debt Ratio and merge with sector
PDF['debt_ratio'] = PDF['total liabilities'] / PDF['total assets']
PDF1 = PDF[['code','debt_ratio']]
PDF_sector = pd.merge(PDF1,sector,how='left',on='code')

PDF_sector_good = PDF_sector.drop_duplicates(keep='last')
PDF_sector_good = PDF_sector_good.sort_values(by=['debt_ratio'],ascending=(True))

###########################################################################

###########################################################################
# ### KLSE Indicator

# Read in KLSE csv file
KLSE = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/klse_clean.csv')

# Change variable type
KLSE1 = KLSE.copy(deep=True)

def toFloat(x):
    return float(x.replace('M','').replace('%','').replace(',',''))

MC = KLSE1['Market_Cap'].apply(toFloat)
DY = KLSE1['DY'].apply(toFloat)
KLSE1['Market_Cap'] = MC
KLSE1['DY'] = DY

def toString(x):
    return str(x).replace('.0','')

co = KLSE1['code'].apply(toString)
KLSE1['code'] = co

def splitVal(x):
    val = x.split(' ')[0]
    if val == 'Oversold':
        val = 1
    if val == 'Neutral':
        val = 0
    if val == 'Overbought':
        val = -1
    return val
rsi = KLSE1['RSI'].apply(splitVal)
sto = KLSE1['Stochastic'].apply(splitVal)
KLSE1['RSI'] = rsi
KLSE1['Stochastic'] = sto

# Change the variable name and calculate PEG
KLSE2 = KLSE1[['full name','code','Sector_main','sector','ROE','P/E','EPS','DPS','DY','RSI','Stochastic']]
KLSE2 = KLSE2.rename(columns={'full name':'name','P/E':'PE'})

KLSE3 = KLSE2[KLSE2['RSI']+KLSE2['Stochastic']>=0]

# Sort value in order to get the top stock simply base on their value
KLSE_good = KLSE3.sort_values(by=['ROE','PE','EPS','DPS','DY'],ascending=(False,True,False,False,False))

###########################################################################

###########################################################################

# ### News & Forum of Stock

# News data
# Read in News csv file
news = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/processed_news.csv')

# Count the total news base on stock code and sort in descending order, to see which stock is more popular
news1 = news.groupby(["extract_code"], as_index=False)['news'].count()
news1 = news1.sort_values(by=['news'],ascending=(False))
news1 = news1.rename(columns={'extract_code':'code'})
news_count = pd.merge(news1,sector,how='left',on='code')

# Forum data
Forum = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Comment.csv')

Forum1 = Forum.groupby(['Stock Code'], as_index=False)['Hot'].sum()
Forum1 = Forum1.sort_values(by=['Hot'],ascending=(False))
Forum1 = Forum1.rename(columns={'Stock Code':'code'})
Forum_count = pd.merge(Forum1,sector,how='left',on='code')

###########################################################################


# ## -- Part 2 --

# - From Part one we can get the information that lead us to selecting some sector out of the entir dataset, and then, from each sector, choose top 8-10 stock to analysis their stock price and performance. 

# Choose the top 50 stocks from three difference sources, and then combine all together
PDF_code = PDF_sector_good.dropna().head(50)[['code','Sector_main','sector']]
KLSE_code = KLSE_good.dropna().head(50)[['code','Sector_main','sector']]
news_code = news_count.dropna().head(50)[['code','Sector_main','sector']]
Forum_code = Forum_count.dropna().head(50)[['code','Sector_main','sector']]

top_code = PDF_code.append(KLSE_code).append(news_code).append(Forum_code)

# Choose a stock that is included in multiple sources
top_code1 = top_code[top_code.duplicated('code')]
top_code_most = top_code1.drop_duplicates('code',keep='last')
top_code_most

top_code_most.to_csv('top_stock_code.csv',index=False,sep=',')
