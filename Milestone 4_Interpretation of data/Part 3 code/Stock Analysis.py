#!/usr/bin/env python
# coding: utf-8

# Import packages
import pandas as pd
import numpy as np
import os

# ## -- Part 1 --

# ### Financial Report (PDF)

# Read in PDF csv file
PDF = pd.read_csv('PDF_summary.csv')
#PDF

# Read in sector csv file
sector = pd.read_csv('Stock_Sector.csv')

# There are some value in the 'code' variable that need to be reformat
PDF['code'] = PDF['code'].str.replace('.0','').astype(str)
PDF['debt_ratio'] = PDF['total liabilities'] / PDF['total assets']
PDF1 = PDF[['code','debt_ratio']]
PDF_sector = pd.merge(PDF1,sector,how='left',on='code')
PDF_sector_good = PDF_sector[PDF_sector.debt_ratio < 0.5]
PDF_sector_good = PDF_sector_good.sort_values(by=['debt_ratio'],ascending=(True))

# ### KLSE Indicator

# Read in KLSE csv file
KLSE = pd.read_csv('klse_clean.csv')

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

# Change the variable name and calculate PEG
KLSE2 = KLSE1[['full name','code','Sector_main','sector','P/E','EPS','DY','Market_Cap']]
KLSE2 = KLSE2.rename(columns={'full name':'name','P/E':'PE','Market_Cap':'MC'})
KLSE2['PEG'] = KLSE2.PE / KLSE2.EPS
KLSE2 = KLSE2.drop(columns=['EPS'])
KLSE2.head()

# Sort value in order to get the top stock simply base on their value
KLSE_good = KLSE2.sort_values(by=['MC','PE','PEG','DY'],ascending=(False,True,True,False))


# ### News of Stock

# Read in News csv file
news = pd.read_csv('processed_news.csv')

# Count the total news base on stock code and sort in descending order, to see which stock is more popular
news1 = news.groupby(["extract_code"], as_index=False)['news'].count()
news1 = news1.sort_values(by=['news'],ascending=(False))
news1 = news1.rename(columns={'extract_code':'code'})
news_count = pd.merge(news1,sector,how='left',on='code')


# ## -- Part 2 --

# Choose the top 50 stocks from three difference sources, and then combine all together
PDF_code = PDF_sector_good.dropna().head(50)[['code','Sector_main','sector']]
KLSE_code = KLSE_good.dropna().head(50)[['code','Sector_main','sector']]
news_code = news_count.dropna().head(50)[['code','Sector_main','sector']]

# Choose a stock that is included in multiple sources
top_code1 = top_code[top_code.duplicated('code')]
top_code_most = top_code1.drop_duplicates('code',keep='last')

# ## -- Part 3 --

# - News Data Sentiment Analysis

# Separate Chinese and English
import re
import langid

inx = []
for i in range(len(news)):
    if langid.classify(news.iloc[i, 3])[0]!='zh':
        inx.append(i)
        
l = list(range(len(news)))
zh = [i for i in l if i not in inx]

len(inx)+len(zh)==len(news)

en_df = news.loc[inx]
zh_df = news.loc[zh]

# Sentiment of Chinese
from snownlp import SnowNLP

szh_df = zh_df[['news','extracted_date','extract_code']]

def stm(x):
    return SnowNLP(x).sentiments

sentiment = szh_df['news'].apply(stm)

szh_df['sentiment'] = sentiment
szh_df

szh_df['sentiment'].describe()

szh_dfstm = szh_df.drop(columns = ['news'])
szh_dfstm = szh_dfstm.rename(columns = {'extracted_date':'date','extract_code':'code'})

# Sentiment of English
from textblob import TextBlob

sen_df = en_df[['news','extracted_date','extract_code']]

def plt(x):
    return TextBlob(x).sentiment[0]

polarity = sen_df['news'].apply(plt)

sen_df['polarity'] = polarity
sen_df

sen_df['polarity'].describe()

sen_dfstm = sen_df.drop(columns = ['news'])
sen_dfstm = sen_dfstm.rename(columns = {'extracted_date':'date','extract_code':'code','polarity':'sentiment'})

# - Stock price is a typical time series data, which will be affected by various complicated factors such as economic environment, government policies, and human operation.
# - First let's load the dataset and define the target variable.

# Read in csv
import pandas as pd
import numpy as np

df = pd.read_csv('pct_chg_all.csv')
df.head()


# - There are multiple variables in the data set - name, code, date, time, opening price, high price, low price, price, volume(total transaction amount), buy/volume, sell/volume, Sector_main, sector, change.
# 
# - The opening price and closing price represent the starting and closing prices of the stock on a certain day.
# 
# - The highest price and the lowest price represent the highest and lowest prices of the day's stock.
# 
# - The total amount of transactions refers to the number of shares traded on the day, and the turnover (Lacs) refers to the turnover of a particular company on a specific date.

# - Firstly, the data is cleaned. In order to ensure the integrity of the data, the ‘-’ of the three variables of open, low and high is changed to NaN value.
# Then remove the unused variables such as time, buy/volume, sell/volume

# Change '-' to NAN
df1 = df.copy(deep=True)
ind_df = df1[df1['open']=='-'].index.tolist()
print(len(ind_df))
print(len(ind_df)/len(df1)) #pct of '-'
df1.loc[ind_df,['open','low','high']]= np.nan
df1 = df1.drop(columns = ['time','buy/volume','sell/volume'])
df1


# - Because the variables of open, low, volume, etc. are character data, change them all back to float to prepare for drawing.

# Change variable type
def vtoFloat(x):
    return float(x.replace(',','')) * 100

volume = df1['volume'].apply(vtoFloat)
df1['volume'] = volume

def alltoFloat(x):
    return float(x)

o = df1['open'].apply(alltoFloat)
l = df1['low'].apply(alltoFloat)
h = df1['high'].apply(alltoFloat)

df1['open'] = o
df1['low'] = l
df1['high'] = h

df1.head()

df1.info()

# - Subset the dataset based on the stocks that consider as the good stock.

df_top = df1[df1.code.isin(top_code_most.code)]
df_top


# To see which company stock we have
company = list(df_top['name'].unique())
company

# To see what Main sector of these stocks
m_sector = list(df_top['Sector_main'].unique())
m_sector

# To see what sector we have
c_sector = list(df_top['sector'].unique())
c_sector


# - After getting the subset of those good stock, group them base on sector, and then analysis them separately.

# Group by sector of all the stock
groups = df_top.groupby('sector')
sectorList = []
for name, group in groups:
    sectorList.append(group)
    
all_sector = sectorList[0]
for k in sectorList[1:]:
    all_sector = all_sector.append(k)

all_sector

# create new folder
if os.path.exists('Market Sector')==False:
    os.mkdir('Market Sector')
#separate dataset into diff_sector
for s in c_sector:
    df_sector = all_sector.loc[all_sector['sector'] == s]
    df_sector.to_csv('Market Sector/'+s.replace(' & ','_').replace(' ','_')+'.csv', index = False)


# - Financial Services

# Use the first sector as an example
Financial = pd.read_csv('Market Sector/Financial_Services.csv')
list(Financial['code'].unique())

# Use the first stock from that sector to analysis the stock trend
F_stock1 = Financial[Financial['code']==5185]
st_name1 = F_stock1.iloc[0,0]
print(st_name1)
F_stock1 = F_stock1.drop(columns=['name','code','Sector_main','sector'])
#setting index as date
F_stock1['date'] = pd.to_datetime(F_stock1.date,format='%Y-%m-%d')
F_stock1.index = F_stock1['date']
F_stock1.describe()


# - As can be seen from the above results, this stock have a total of 41 samples. For the price varibale, we can see it have an average of 2.24, a standard deviation of 2.23 (the fluctuation is relatively small), and a maximum value of 2.34.

# - The calculation of profit and loss is usually determined by the closing price of the stock on the day, so we use the closing price as the plotting variable. Let's draw the target variable to understand its distribution in our dataset.
# - Use the stock closing price column data to draw a line chart to see the stock trend:

# Plot time series data using price variable
import matplotlib.pyplot as plt
import matplotlib

from pylab import *
plt.rcParams['axes.unicode_minus'] = False

F_stock1.plot(y='price')
plt.title(st_name1+' stock price trend')
plt.xlabel('Date')
plt.ylabel('Stock Price(RM)')
plt.grid(True)

F_stock1.plot(y='volume')
plt.title(st_name1+' stock volume trend')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.grid(True)

# It can be seen that there are few trading peaks in the figure
# which can be further analyzed by combining other data

# Daily return visualization
F_stock1['change'].plot(grid = True)

# Plot price and 5 day moving average
s_p_m1 = F_stock1.copy(deep=True)
s_p_m1['roll_mean'] = s_p_m1['price'].rolling(window=5).mean()
s_p_m1[['price', 'roll_mean']].plot(subplots=False, figsize=(9, 5), grid=True)

# - Line segment chart is feasible, but the data for each day has at least four variables (opening, stock price, stock price and closing), We hope to find a visualization that does not require us to draw four different lines to see the trend of these four variables. In general, we use the candlestick chart (also known as the Japanese candlestick chart) to visualize financial data. The candlestick chart was first used by Japanese rice merchants in the 18th century.

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime
import pylab

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime
import pylab
 
MA1 = 5# The date interval of the moving average
MA2 = 10
startdate = datetime.date(2019,2,25)
enddate = datetime.date(2019,4,23)
data=pd.DataFrame(F_stock1)
stdata=pd.DataFrame({'DateTime':data.index,'Open':data.open,'High':data.high,'Close':data.price,'Low':data.low})
stdata['DateTime'] = mdates.date2num(stdata['DateTime'].astype(datetime.date))
 
def main():
    daysreshape = stdata.reset_index()
    daysreshape = daysreshape.reindex(columns=['DateTime', 'Open', 'High', 'Low', 'Close'])
 
    Av1 = daysreshape['Close'].rolling(window=MA1).mean()
    Av2 = daysreshape['Close'].rolling(window=MA2).mean()
    SP = len(daysreshape.DateTime.values[MA2 - 1:])
    fig = plt.figure(facecolor='#07000d', figsize=(15, 10))
 
    ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, facecolor='#07000d')
    candlestick_ohlc(ax1, daysreshape.values[-SP:], width=.6, colorup='#53c156', colordown='#ff1717')
    Label1 = str(MA1) + ' SMA'
    Label2 = str(MA2) + ' SMA'
 
    ax1.plot(daysreshape.DateTime.values[-SP:], Av1[-SP:], '#e1edf9', label=Label1, linewidth=1.5)
    ax1.plot(daysreshape.DateTime.values[-SP:], Av2[-SP:], '#4ee6fd', label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.show()

if __name__ == "__main__":
    main()


# - Here, green means stock price is increasing, red means stock price is decreasing.

# - The green line in the candlestick chart represents the closing price of the trading day is higher than the opening price (profit), and the red line represents the opening price of the trading day is higher than the closing price (loss). The tick marks represent the highest and lowest prices of the day's trade. Candlestick charts are widely used in financial and technical analysis in trading decisions, using the shape, color and position of the body.

# - Analysis of the rise and fall of stock:
# - Which defines a function change() function, the calculation formula is:
# - Calculate stock price change = (last price - buy price) / buy price

# Analysis stock price change within these 40 days
def change(column):
    buyPrice = column[0]
    curPrice = column[len(F_stock1)-1]
    priceChange = (curPrice-buyPrice)/buyPrice
    if(priceChange > 0):
        print('Stock Accumulated Rise=',priceChange)
    elif(priceChange == 0):
        print('Stock Accumulated not change=',priceChange)
    else:
        print('Stock Accumulated Decrease=',priceChange)
    return priceChange

closeCol = F_stock1['price']
F_stock1_change = change(closeCol)


# - Show the correlation coefficient matrix of the stock:


F_stock1.corr()


# According to the results, the stock volatility is slightly larger, but the overall form of the stock is decreasing. Combining the scatter plot and the correlation coefficient matrix, the correlation coefficient between volume and stock price is 0.08, which is slightly positively linear. Stock trading was active, and combined with the results of the previous calculations, this stocks decrease by 6.08% in those weeks, so this stock is temporarily not suitable for investing.

# - Use a scatter plot to show the relationship between volume and stock price:

F_stock1.plot(x='volume',y='price',kind='scatter')
plt.xlabel('Volume')
plt.ylabel('Stock Price(RM)')
plt.title('Volume VS. Price')
plt.grid(True)

F_stock1[['price','volume']].plot(secondary_y='volume', grid=True)


# - To compare with the Stock Index 

ftse = pd.read_csv('FTSE.csv')
#setting index as date
ftse['Date'] = pd.to_datetime(ftse.Date,format='%Y-%m-%d')
ftse = ftse.sort_values(by = 'Date')
ftse.index = ftse['Date']
st_ft = F_stock1[['price']]
def ptoFloat(x):
    return float(x)

Price = ftse['Price'].apply(ptoFloat)
st_ft['SI_Price'] = Price
price = st_ft['price'].apply(ptoFloat)
st_ft['price'] = price

st_ft[['price','SI_Price']].plot(secondary_y='SI_Price', grid=True)

# - To compare with news

F_news1_zh = szh_dfstm[szh_dfstm['code']=='5185']
F_news1_en = sen_dfstm[sen_dfstm['code']=='5185']

zh_stm = []
en_stm = []

# Reasign the value to sentiment, where 1 means positive, 0 means neutral, -1 means negative
if len(F_news1_zh) != 0:
    F_news1_zh = F_news1_zh.groupby(by=['date']).mean()
    for i in F_news1_zh['sentiment']:
        if i < 0.501:
            zh_stm.append(-1)
        elif i > 0.59:
            zh_stm.append(1)
        else:
            zh_stm.append(0)
    F_news1_zh['sentiment'] = zh_stm
    
if len(F_news1_en) != 0:
    F_news1_en = F_news1_en.groupby(by=['date']).mean()
    for i in F_news1_en['sentiment']:
        if i < 0:
            en_stm.append(-1)
        elif i > 0:
            en_stm.append(1)
        else:
            en_stm.append(0)
    F_news1_en['sentiment'] = en_stm

# Combine sentiment of both Chinese and English all together 
F_news1 = F_news1_zh.append(F_news1_en)
F_news1 = F_news1.drop(columns = ['code','date'])

F_news1['date'] = list(F_news1.index)

#setting index as date
F_news1['date'] = pd.to_datetime(F_news1.date,format='%Y-%m-%d')
F_news1.index = F_news1['date']

# Merge stock price data and news sentiment data together for plotting 
stock_news1 = pd.merge(F_stock1,F_news1,how='left',on='date')
# Fill NAs with value 0 in other to get a better visual
stock_news1['sentiment'] = stock_news1['sentiment'].fillna(0)
#setting index as date
stock_news1['date'] = pd.to_datetime(stock_news1.date,format='%Y-%m-%d')
stock_news1.index = stock_news1['date']
stock_news1

# Compare price and sentiment
stock_news1[['price','sentiment']].plot(secondary_y='sentiment', grid=True)

# Compare volume and sentiment
stock_news1[['volume','sentiment']].plot(secondary_y='sentiment', grid=True)


# - To compare with other stocks

# The second stock from the same sector
F_stock2 = Financial[Financial['code']==2488]
st_name2 = F_stock2.iloc[0,0]
print(st_name2)
F_stock2 = F_stock2.drop(columns=['name','code','Sector_main','sector'])
#setting index as date
F_stock2['date'] = pd.to_datetime(F_stock2.date,format='%Y-%m-%d')
F_stock2.index = F_stock2['date']
F_stock2.describe()


F_stock3 = Financial[Financial['code']==1023]
st_name3 = F_stock3.iloc[0,0]
print(st_name3)
F_stock3 = F_stock3.drop(columns=['name','code','Sector_main','sector'])
#setting index as date
F_stock3['date'] = pd.to_datetime(F_stock3.date,format='%Y-%m-%d')
F_stock3.index = F_stock3['date']
F_stock3.describe()


F_stock4 = Financial[Financial['code']==1155]
st_name4 = F_stock4.iloc[0,0]
print(st_name4)
F_stock4 = F_stock4.drop(columns=['name','code','Sector_main','sector'])
#setting index as date
F_stock4['date'] = pd.to_datetime(F_stock4.date,format='%Y-%m-%d')
F_stock4.index = F_stock4['date']
F_stock4.describe()


F_stock5 = Financial[Financial['code']==1066]
st_name5 = F_stock5.iloc[0,0]
print(st_name5)
F_stock5 = F_stock5.drop(columns=['name','code','Sector_main','sector'])
#setting index as date
F_stock5['date'] = pd.to_datetime(F_stock5.date,format='%Y-%m-%d')
F_stock5.index = F_stock5['date']
F_stock5.describe()

# Create a dataframe that put all the stock price inside
closePrice = pd.DataFrame({"stock1": F_stock1["price"],
                      "stock2": F_stock2["price"],
                      "stock3": F_stock3["price"],
                      "stock4": F_stock4["price"],
                      "stock5": F_stock5["price"],    })
# Plot all the stock price from the same sector 
# Draw different stock prices on a graph.
# So that we can compare different stocks and compare the relationship between stocks and the market.
closePrice.plot(grid=True)
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Stock price trend comparison chart')


# - The problem of this graph: Although the absolute value of the price is important (expensive stocks are difficult to buy, this will not only affect their volatility but also affect the ease with which you trade them). But in the transaction, we pay more attention to the change in the price of each stock rather than its price.

# - A "better" solution is to visualize the information we actually care about: the return of stocks, which requires us to make the necessary data transformations. There are many ways to convert data. One of the conversion methods is to compare the stock price of each trading day with the stock price starting from the time period we care about. That is: 
#        Return = Price(t) / Price(0)

# To plot the return of each stock
stock_return = closePrice.apply(lambda x: x / x[0])
stock_return.plot(grid = True).axhline(y = 1, color = "black", lw = 2)
plt.xlabel('Date')
plt.ylabel('Benchmark rate of return')
plt.title('Stock price return')


# - Now we can see how high the return of each stock is from the date we care about. And we can see that the correlation between these stocks is positive. They basically move in the same direction, which is difficult to observe in other types of charts.

# - We can use logarithmic differences to represent stock price changes:
#         Change(t) = log(price(t)) - log(price(t-1))
# - The log here is the natural logarithm. The advantage of using a logarithmic difference is that the difference value can be interpreted as a percentage difference in the stock and is not affected by the denominator.

# Plot all stock 
stock_return = closePrice.apply(lambda x: np.log(x) - np.log(x.shift(1)))
stock_return.plot(grid = True).axhline(y = 0, color = "black", lw = 2)
plt.xlabel('Date')
plt.ylabel('Rate of change')
plt.title('Stock price change')


# - From the income gap of the relative time period, the overall trend of different securities can be clearly seen.


# - Correlation to other stocks

import seaborn as sns 
# Correlation between the first two stock
sns.jointplot(F_stock1.price, F_stock2.price, kind="reg")

# We can also look at the correlation value:
np.corrcoef(F_stock1.price, F_stock2.price)


# - We noticed that the r-value is 0.7435; it is good for predictions, but we need to remember an important fact: if we know the closing price of stock1, we can also check the closing price of stock2.
# - So let's look at the correlation of the closing price seven days ago to get a more viable indicator: This time we get the r-value of 0.69; still very good!

#seven day lead 
np.corrcoef(F_stock1.price[:-7],F_stock2.price[7:])


# Make a stock correlation comparison for all companies
sns.pairplot(closePrice.dropna())


# - Comparing the data between any two companies of the five companies, it can be seen from the scatter plot that the correlation between some stocks is better, the data trend is more in line with x=y, and the width is not exaggerated. The correlation in other figures is weaker.
# 
#            
# - In short, the rise and fall of stocks is affected by many factors, which may be due to policy reasons, environmental reasons, internal reasons, and the correlation between different companies.


# - Consumer Products & Services

Consumer = pd.read_csv('Market Sector/Consumer_Products_Services.csv')
list(Consumer['code'].unique())


# - Telecommunications & Media

Telecom = pd.read_csv('Market Sector/Telecommunications_Media.csv')
list(Telecom['code'].unique())


# - Construction

Construction = pd.read_csv('Market Sector/Construction.csv')
list(Construction['code'].unique())


# - Health Care

Health = pd.read_csv('Market Sector/Health_Care.csv')
list(Health['code'].unique())


# - Transportation & Logistics

Transpor = pd.read_csv('Market Sector/Transportation_Logistics.csv')
list(Transpor['code'].unique())


# - Energy

Energy = pd.read_csv('Market Sector/Energy.csv')
list(Energy['code'].unique())


# - Industrial Products & Services

Industrial = pd.read_csv('Market Sector/Industrial_Products_Services.csv')
list(Industrial['code'].unique())


# # Conclusion

# - By analyzing such a stock in this way, it can be extended to multiple stocks for analysis and comparison. First, the user can understand the real situation of the market, select a stock of a sector to invest, and compare the same sector to select a stock that is more worthy of investment.

