# Import packages
import pandas as pd
import numpy as np
import os

# ## -- Part 1 --

# ### KLSE Indicator

# Read in KLSE csv file
KLSE = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%204/klse_clean.csv')
# KLSE

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

KLSE1.info()

# - ***PE ratio (price-to-earnings ratio):*** It’s a financial measurement that investors can use to evaluate the future cash flows from an investment in relation to the value of the investment.

# - ***DY:*** It shows what percentage of the stock’s market price is being paid back in the form of a dividend that year.

# Change the variable name and calculate PEG
KLSE2 = KLSE1[['full name','code','Sector_main','sector','ROE','P/E','EPS','DPS','DY','RSI','Stochastic']]
KLSE2 = KLSE2.rename(columns={'full name':'name','P/E':'PE'})
# KLSE2.head()

KLSE3 = KLSE2[KLSE2['RSI']+KLSE2['Stochastic']>=0]
KLSE3

# Sort value in order to get the top stock simply base on their value
KLSE_good = KLSE3.sort_values(by=['ROE','PE','EPS','DPS','DY'],ascending=(False,True,False,False,False))
KLSE_good.head(50)
