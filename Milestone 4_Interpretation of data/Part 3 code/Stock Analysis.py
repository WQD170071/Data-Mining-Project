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

###########################################################################

# ## -- Part 2 --

# Choose the top 50 stocks from three difference sources, and then combine all together
PDF_code = PDF_sector_good.dropna().head(50)[['code','Sector_main','sector']]
KLSE_code = KLSE_good.dropna().head(50)[['code','Sector_main','sector']]
news_code = news_count.dropna().head(50)[['code','Sector_main','sector']]
Forum_code = Forum_count.dropna().head(50)[['code','Sector_main','sector']]

top_code = PDF_code.append(KLSE_code).append(news_code).append(Forum_code)

# Choose a stock that is included in multiple sources
top_code1 = top_code[top_code.duplicated('code')]
top_code_most = top_code1.drop_duplicates('code',keep='last')

###########################################################################

###########################################################################

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

# len(inx)+len(zh)==len(news)

en_df = news.loc[inx]
zh_df = news.loc[zh]

# Sentiment of Chinese
from snownlp import SnowNLP

szh_df = zh_df[['news','extracted_date','extract_code']]

def stm(x):
    return SnowNLP(x).sentiments

sentiment = szh_df['news'].apply(stm)

szh_df['sentiment'] = sentiment
# szh_df

# szh_df['sentiment'].describe()

szh_dfstm = szh_df.drop(columns = ['news'])
szh_dfstm = szh_dfstm.rename(columns = {'extracted_date':'date','extract_code':'code'})

# Sentiment of English
from textblob import TextBlob

sen_df = en_df[['news','extracted_date','extract_code']]

def plt(x):
    return TextBlob(x).sentiment[0]

polarity = sen_df['news'].apply(plt)

sen_df['polarity'] = polarity
# sen_df

# sen_df['polarity'].describe()

sen_dfstm = sen_df.drop(columns = ['news'])
sen_dfstm = sen_dfstm.rename(columns = {'extracted_date':'date','extract_code':'code','polarity':'sentiment'})

# - Stock price is a typical time series data, which will be affected by various complicated factors such as economic environment, government policies, and human operation.
# - First let's load the dataset and define the target variable.

# Read in csv
import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/pct_chg_all.csv')
# df


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
df1.loc[ind_df,['open','low','high']]= 0
df1 = df1.drop(columns = ['time','buy/volume','sell/volume'])
df1['change'].fillna(0,inplace=True)
# df1


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

# df1.head()

# df1.info()

# - Subset the dataset based on the stocks that consider as the good stock.

df_top = df1[df1.code.isin(top_code_most.code)]
# df_top


# To see which company stock we have
company = list(df_top['name'].unique())
# company

# To see what Main sector of these stocks
m_sector = list(df_top['Sector_main'].unique())
# m_sector

# To see what sector we have
c_sector = list(df_top['sector'].unique())
# c_sector


# - After getting the subset of those good stock, group them base on sector, and then analysis them separately.

# Group by sector of all the stock
groups = df_top.groupby('sector')
sectorList = []
for name, group in groups:
    sectorList.append(group)

all_sector = sectorList[0]
for k in sectorList[1:]:
    all_sector = all_sector.append(k)

all_sector1 = all_sector.drop_duplicates(('code','date'),keep='last')
# all_sector1

# create new folder
if os.path.exists('Market Sector')==False:
    os.mkdir('Market Sector')
#separate dataset into diff_sector
for s in c_sector:
    df_sector = all_sector1.loc[all_sector1['sector'] == s]
    df_sector.to_csv('Market Sector/'+s.replace(' & ','_').replace(' ','_')+'.csv', index = False)

# - Technology
Technology = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Technology.csv')
#list(Technology['code'].unique())

# - Telecommunications & Media
Telecom = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Telecommunications_Media.csv')
# list(Telecom['code'].unique())

# - Construction
Construction = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Construction.csv')
# list(Construction['code'].unique())

# - Health Care
Health = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Health_Care.csv')
# list(Health['code'].unique())

# - Transportation & Logistics
Transpor = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Transportation_Logistics.csv')
# list(Transpor['code'].unique())

# - Energy
Energy = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Energy.csv')
# list(Energy['code'].unique())

# - Industrial Products & Services
Industrial = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Industrial_Products_Services.csv')
# list(Industrial['code'].unique())

# - Financial Services
Financial = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Financial_Services.csv')
#list(Financial['code'].unique())

# - Consumer Products & Services
import pandas as pd
Consumer = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Consumer_Products_Services.csv')
# list(Consumer['code'].unique())
# Use the Consumer Products & Services sector as the stock analysis dataset

def stockAna (code):
    stock = Sector[Sector['code']==code]
    st_name = stock.iloc[0,0]
    print(st_name)
    stock = stock.drop(columns=['Sector_main','sector'])
    stock['date'] = pd.to_datetime(stock.date,format='%m/%d/%Y')
    stock.index = stock['date']
    return stock

Sector = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Consumer_Products_Services.csv')
C_stock1 = stockAna(5099)
C_stock2 = stockAna(1562)
C_stock3 = stockAna(5248)
C_stock4 = stockAna(3689)
C_stock5 = stockAna(3182)
C_stock6 = stockAna(7668)
C_stock7 = stockAna(7087)
C_stock8 = stockAna(4707)
C_stock9 = stockAna(7052)
C_stock10 = stockAna(4197)
C_stock11 = stockAna(5131)

#To compare with news

def newsentiment(code):
    news_zh = szh_dfstm[szh_dfstm['code']==code]
    news_en = sen_dfstm[sen_dfstm['code']==code]
    #print(news_zh)
    zh_stm = []
    en_stm = []
    
    # Reasign the value to sentiment, where 1 means positive, 0 means neutral, -1 means negative
    if len(news_zh) != 0:
        news_zh = news_zh.groupby(by=['date']).mean()
        for i in news_zh['sentiment']:
            if i < 0.501:
                zh_stm.append(-1)
            elif i > 0.59:
                zh_stm.append(1)
            else:
                zh_stm.append(0)
        news_zh['sentiment'] = zh_stm
    
    if len(news_en) != 0:
        news_en = news_en.groupby(by=['date']).mean()
        for i in news_en['sentiment']:
            if i < 0:
                en_stm.append(-1)
            elif i > 0:
                en_stm.append(1)
            else:
                en_stm.append(0)
        news_en['sentiment'] = en_stm
    
    n = news_zh.append(news_en)
    n['date'] = list(n.index)
    #setting index as date
    n['date'] = pd.to_datetime(n.date,format='%Y-%m-%d')
    
    return n

# Combine sentiment of both Chinese and English all together
C_news1 = newsentiment('5099')
C_news2 = newsentiment('1562')
C_news3 = newsentiment('5248')
C_news4 = newsentiment('3689')
C_news5 = newsentiment('3182')
C_news6 = newsentiment('7668')
C_news7 = newsentiment('7087')
C_news8 = newsentiment('4707')
C_news9 = newsentiment('7052')
C_news10 = newsentiment('4197')
C_news11 = newsentiment('5131')

# C_stock1.describe()

# - As can be seen from the above results, this stock have a total of 41 samples. For the price varibale, we can see it have an average of 2.71, a standard deviation of 0.16 (the fluctuation is relatively large), and a maximum value of 3.10.

# - The calculation of profit and loss is usually determined by the closing price of the stock on the day, so we use the closing price as the plotting variable. Let's draw the target variable to understand its distribution in our dataset.
# - Use the stock closing price column data to draw a line chart to see the stock trend:

# Plot time series data using price variable
import matplotlib.pyplot as plt
import matplotlib

from pylab import *
plt.rcParams['axes.unicode_minus'] = False

C_stock1.plot(y='price')
plt.title('AIRASIA GROUP BERHAD stock price trend')
plt.xlabel('Date')
plt.ylabel('Stock Price(RM)')
plt.grid(True)

C_stock1.plot(y='volume')
plt.title('AIRASIA GROUP BERHAD stock volume trend')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.grid(True)

# It can be seen that there are few trading peaks in the figure
# which can be further analyzed by combining other data

# Daily return visualization
C_stock1['change'].plot(grid = True)
plt.title('AIRASIA GROUP BERHAD stock change trend')
plt.xlabel('Date')
plt.ylabel('Change')

# Plot price and 5 day moving average
s_p_m1 = C_stock1.copy(deep=True)
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
data=pd.DataFrame(C_stock1)
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

# Analysis stock price change for the past 40 days
def change(column):
    buyPrice = column[0]
    curPrice = column[len(C_stock1)-1]
    priceChange = (curPrice-buyPrice)/buyPrice
    if(priceChange > 0):
        print('Stock Accumulated Rise=',priceChange)
    elif(priceChange == 0):
        print('Stock Accumulated not change=',priceChange)
    else:
        print('Stock Accumulated Decrease=',priceChange)
    return priceChange

closeCol = C_stock1['price']
C_stock1_change = change(closeCol)

# - Show the correlation coefficient matrix of the stock:
C_stock1.corr()

# According to the results, the stock volatility is slightly larger, but the overall form of the stock is decreasing. Combining the scatter plot and the correlation coefficient matrix, the correlation coefficient between volume and stock price is 0.07, which is slightly positively linear. Stock trading was active, and combined with the results of the previous calculations, this stocks decrease by 18.89% in those weeks.

# - Use a scatter plot to show the relationship between volume and stock price:

C_stock1.plot(x='volume',y='price',kind='scatter')
plt.xlabel('Volume')
plt.ylabel('Stock Price(RM)')
plt.title('Volume VS. Price')
plt.grid(True)

C_stock1[['price','volume']].plot(secondary_y='volume', grid=True)

# - To compare with the Stock Index

ftse = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/FTSE%20Malaysia%20KLCI%20Historical%20Data.csv')
#setting index as date
ftse['Date'] = pd.to_datetime(ftse.Date,format='%Y-%m-%d')
ftse = ftse.sort_values(by = 'Date')
ftse.index = ftse['Date']
st_ft = C_stock1[['price']]
def ptoFloat(x):
    return float(x)

Price = ftse['Price'].apply(ptoFloat)
st_ft['SI_Price'] = Price
price = st_ft['price'].apply(ptoFloat)
st_ft['price'] = price

st_ft[['price','SI_Price']].plot(secondary_y='SI_Price', grid=True)

# - To compare with news

# Merge stock price data and news sentiment data together for plotting
stock_news1 = pd.merge(C_stock1,C_news1,how='left',on='date')
# Fill NAs with value 0 in other to get a better visual
stock_news1['sentiment'] = stock_news1['sentiment'].fillna(0)
#setting index as date
stock_news1['date'] = pd.to_datetime(stock_news1.date,format='%Y-%m-%d')
stock_news1.index = stock_news1['date']
# stock_news1

# Compare price and sentiment
stock_news1[['price','sentiment']].plot(secondary_y='sentiment', grid=True)

# Compare volume and sentiment
stock_news1[['volume','sentiment']].plot(secondary_y='sentiment', grid=True)

# - To compare with other stocks

# Create a dataframe that put all the stock price inside
closePrice = pd.DataFrame({"stock1": C_stock1["price"],
                          "stock2": C_stock2["price"],
                          "stock3": C_stock3["price"],
                          "stock4": C_stock4["price"],
                          "stock5": C_stock5["price"],
                          "stock6": C_stock6["price"],
                          "stock7": C_stock7["price"],
                          "stock8": C_stock8["price"],
                          "stock9": C_stock9["price"],
                          "stock10": C_stock10["price"],
                          "stock11": C_stock11["price"]})
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
sns.jointplot(C_stock3.price, C_stock2.price, kind="reg")

# We can also look at the correlation value:
np.corrcoef(C_stock3.price, C_stock2.price)

# - We noticed that the r-value is 0.5839198; it is good for predictions, but we need to remember an important fact: if we know the closing price of stock3, we can also relate the closing price of stock2.

# Make a stock correlation comparison for all companies
sns.pairplot(closePrice.dropna())

# - We can see that stock 1,5,6,8 have a positve correlation, while stock 11 has no correlation among these stocks.

# - Comparing the data between any two companies of the five companies, it can be seen from the scatter plot that the correlation between some stocks is better, the data trend is more in line with x=y, and the width is not exaggerated. The correlation in other figures is weaker.
#
#
# - In short, the rise and fall of stocks is affected by many factors, which may be due to policy reasons, environmental reasons, internal reasons, and the correlation between different companies.

import numpy as np
import math

class SAX_trans:
    
    def __init__(self, ts, w, alpha):
        self.ts = ts
        self.w = w
        self.alpha = alpha
        self.aOffset = ord('a')
        self.breakpoints = {'3' : [-0.43, 0.43],
            '4' : [-0.67, 0, 0.67],
            '5' : [-0.84, -0.25, 0.25, 0.84],
            '6' : [-0.97, -0.43, 0, 0.43, 0.97],
            '7' : [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
            '8' : [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
        
        }
        self.beta = self.breakpoints[str(self.alpha)]
    
    def normalize(self):
        X = np.asanyarray(self.ts)
        return (X - np.nanmean(X)) / np.nanstd(X)

    def paa_trans(self):
        tsn = self.normalize()
        paa_ts = []
        n = len(tsn)
        xk = math.ceil( n / self.w )
        for i in range(0,n,xk):
            temp_ts = tsn[i:i+xk]
            paa_ts.append(np.mean(temp_ts))
        return paa_ts
    
    def to_sax(self):
        tsn = self.paa_trans()
        len_tsn = len(tsn)
        len_beta = len(self.beta)
        strx = ''
        for i in range(len_tsn):
            letter_found = False
            for j in range(len_beta):
                if np.isnan(tsn[i]):
                    strx += '-'
                    letter_found = True
                    break
                if tsn[i] < self.beta[j]:
                    strx += chr(self.aOffset +j)
                    letter_found = True
                    break
            if not letter_found:
                strx += chr(self.aOffset + len_beta)
    return strx

    
    def compare_Dict(self):
        num_rep = range(self.alpha)
        letters = [chr(x + self.aOffset) for x in num_rep]
        compareDict = {}
        len_letters = len(letters)
        for i in range(len_letters):
            for j in range(len_letters):
                if np.abs(num_rep[i] - num_rep[j])<=1:
                    compareDict[letters[i]+letters[j]]=0
                else:
                    high_num = np.max([num_rep[i], num_rep[j]])-1
                    low_num = np.min([num_rep[i], num_rep[j]])
                    compareDict[letters[i]+letters[j]] = self.beta[high_num] - self.beta[low_num]
        return compareDict

def dist(self, strx1,strx2):
    len_strx1 = len(strx1)
    len_strx2 = len(strx2)
    com_dict = self.compare_Dict()
    
    if len_strx1 != len_strx2:
        print("The length of the two strings does not match")
        else:
            list_letter_strx1 = [x for x in strx1]
            list_letter_strx2 = [x for x in strx2]
            mindist = 0.0
            for i in range(len_strx1):
                if list_letter_strx1[i] is not '-' and list_letter_strx2[i] is not '-':
                    mindist += (com_dict[list_letter_strx1[i] + list_letter_strx2[i]])**2
            mindist = np.sqrt((len(self.ts)*1.0)/ (self.w*1.0)) * np.sqrt(mindist)
            return mindist

ts1 = C_stock1['price'].values.tolist()
ts2 = C_stock2['price'].values.tolist()
ts3 = C_stock3['price'].values.tolist()
ts4 = C_stock4['price'].values.tolist()
ts5 = C_stock5['price'].values.tolist()
ts6 = C_stock6['price'].values.tolist()
ts7 = C_stock7['price'].values.tolist()
ts8 = C_stock8['price'].values.tolist()
ts9 = C_stock9['price'].values.tolist()
ts10 = C_stock10['price'].values.tolist()
ts11 = C_stock11['price'].values.tolist()
x1 = SAX_trans(ts=ts1,w=10,alpha=4)
x2 = SAX_trans(ts=ts2,w=10,alpha=4)
x3 = SAX_trans(ts=ts3,w=10,alpha=4)
x4 = SAX_trans(ts=ts4,w=10,alpha=4)
x5 = SAX_trans(ts=ts5,w=10,alpha=4)
x6 = SAX_trans(ts=ts6,w=10,alpha=4)
x7 = SAX_trans(ts=ts7,w=10,alpha=4)
x8 = SAX_trans(ts=ts8,w=10,alpha=4)
x9 = SAX_trans(ts=ts9,w=10,alpha=4)
x10 = SAX_trans(ts=ts10,w=10,alpha=4)
x11 = SAX_trans(ts=ts11,w=10,alpha=4)
st1 = x1.to_sax()
st2 = x2.to_sax()
st3 = x3.to_sax()
st4 = x4.to_sax()
st5 = x5.to_sax()
st6 = x6.to_sax()
st7 = x7.to_sax()
st8 = x8.to_sax()
st9 = x9.to_sax()
st10 = x10.to_sax()
st11 = x11.to_sax()
dist12 = x1.dist(st1,st2)
dist13 = x1.dist(st1,st3)
dist14 = x1.dist(st1,st4)
dist15 = x1.dist(st1,st5)
dist16 = x1.dist(st1,st6)
dist17 = x1.dist(st1,st7)
dist18 = x1.dist(st1,st8)
dist19 = x1.dist(st1,st9)
dist110 = x1.dist(st1,st10)
dist111 = x1.dist(st1,st11)
dist23 = x2.dist(st2,st3)
dist24 = x2.dist(st2,st4)
dist25 = x2.dist(st2,st5)
dist26 = x2.dist(st2,st6)
dist27 = x2.dist(st2,st7)
dist28 = x2.dist(st2,st8)
dist29 = x2.dist(st2,st9)
dist210 = x2.dist(st2,st10)
dist211 = x2.dist(st2,st11)
dist34 = x3.dist(st3,st4)
dist35 = x3.dist(st3,st5)
dist36 = x3.dist(st3,st6)
dist37 = x3.dist(st3,st7)
dist38 = x3.dist(st3,st8)
dist39 = x3.dist(st3,st9)
dist310 = x3.dist(st3,st10)
dist311 = x3.dist(st3,st11)
dist45 = x4.dist(st4,st5)
dist46 = x4.dist(st4,st6)
dist47 = x4.dist(st4,st7)
dist48 = x4.dist(st4,st8)
dist49 = x4.dist(st4,st9)
dist410 = x4.dist(st4,st10)
dist411 = x4.dist(st4,st11)
dist56 = x5.dist(st5,st6)
dist57 = x5.dist(st5,st7)
dist58 = x5.dist(st5,st8)
dist59 = x5.dist(st5,st9)
dist510 = x5.dist(st5,st10)
dist511 = x5.dist(st5,st11)
dist67 = x6.dist(st6,st7)
dist68 = x6.dist(st6,st8)
dist69 = x6.dist(st6,st9)
dist610 = x6.dist(st6,st10)
dist611 = x6.dist(st6,st11)
dist78 = x7.dist(st7,st8)
dist79 = x7.dist(st7,st9)
dist710 = x7.dist(st7,st10)
dist711 = x7.dist(st7,st11)
dist89 = x8.dist(st8,st9)
dist810 = x8.dist(st8,st10)
dist811 = x8.dist(st8,st11)
dist910 = x9.dist(st9,st10)
dist911 = x9.dist(st9,st11)
dist1011 = x10.dist(st10,st11)
print('st1',st1)
print('st2',st2)
print('st3',st3)
print('st4',st4)
print('st5',st5)
print('st6',st6)
print('st7',st7)
print('st8',st8)
print('st9',st9)
print('st10',st10)
print('st11',st11)
print('dist12',dist12)
print('dist13',dist13)
print('dist14',dist14)
print('dist15',dist15)
print('dist16',dist16)
print('dist17',dist17)
print('dist18',dist18)
print('dist19',dist19)
print('dist110',dist110)
print('dist111',dist111)
print('dist23',dist23)
print('dist24',dist24)
print('dist25',dist25)
print('dist26',dist26)
print('dist27',dist27)
print('dist28',dist28)
print('dist29',dist29)
print('dist210',dist210)
print('dist211',dist211)
print('dist34',dist34)
print('dist35',dist35)
print('dist36',dist36)
print('dist37',dist37)
print('dist38',dist38)
print('dist39',dist39)
print('dist310',dist310)
print('dist311',dist311)
print('dist45',dist45)
print('dist46',dist46)
print('dist47',dist47)
print('dist48',dist48)
print('dist49',dist49)
print('dist410',dist410)
print('dist411',dist411)
print('dist56',dist56)
print('dist57',dist57)
print('dist58',dist58)
print('dist59',dist59)
print('dist510',dist510)
print('dist511',dist511)
print('dist67',dist67)
print('dist68',dist68)
print('dist69',dist69)
print('dist610',dist610)
print('dist611',dist611)
print('dist78',dist78)
print('dist79',dist79)
print('dist710',dist710)
print('dist711',dist711)
print('dist89',dist89)
print('dist810',dist810)
print('dist811',dist811)
print('dist910',dist910)
print('dist911',dist911)
print('dist1011',dist1011)

# Use the Financial Services sector as the stock analysis dataset
Consumer = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/Market%20Sector/Consumer_Products_Services.csv')
# list(Consumer['code'].unique())

# Merge stock price data and news sentiment data together
def mergePS(s,n):
    stock_news = pd.merge(s.reset_index(drop=True),n.reset_index(drop=True),how='left',on='date')
    stock_news['sentiment'].fillna(0,inplace=True)
    #setting index as date
    stock_news['date'] = pd.to_datetime(stock_news.date,format='%Y-%m-%d')
    stock_news.index = stock_news['date']
    return stock_news

stock_news1 = mergePS(C_stock1,C_news1)
stock_news2 = mergePS(C_stock5,C_news5)
stock_news3 = mergePS(C_stock6,C_news6)
stock_news4 = mergePS(C_stock8,C_news8)

Consumer_news = stock_news1.append(stock_news2).append(stock_news3).append(stock_news4)
# Consumer_news
# Consumer_news.describe()
Consumer_news.loc[(Consumer_news['change']< -0.005)|(Consumer_news['sentiment']==-1),'target'] = 'sell'
Consumer_news.loc[(Consumer_news['change']>0.0025)|(Consumer_news['sentiment']==1),'target'] = 'buy'
Consumer_news.loc[Consumer_news['target'].isnull(),'target'] = 'hold'
# Consumer_news

print("buy: "+str(sum(Consumer_news['target']=='buy')),"hold: "+str(sum(Consumer_news['target']=='hold')),"sell: "+str(sum(Consumer_news['target']=='sell')))

Consumer_news.to_csv('CModel.csv',index=False,sep=',')

# # Conclusion

# - By analyzing such a stock in this way, it can be extended to multiple stocks for analysis and comparison. First, the user can understand the real situation of the market, select a stock of a sector to invest, and compare the same sector to select a stock that is more worthy of investment.

