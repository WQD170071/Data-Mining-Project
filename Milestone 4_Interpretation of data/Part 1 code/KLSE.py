#!/usr/bin/env python
# coding: utf-8

# Import packages
import pandas as pd
import numpy as np
import os

# ## -- Part 1 --

# ### KLSE Indicator

# Read in KLSE csv file 
KLSE = pd.read_csv('klse_clean.csv')
KLSE

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

KLSE1.info()

# - ***Market Cap:*** It means how much all of the outstanding shares of a company is worth at the current market price.
# 
# - ***PE ratio (price-to-earnings ratio):*** It’s a financial measurement that investors can use to evaluate the future cash flows from an investment in relation to the value of the investment.
# 
# - ***PEG:*** Often called Price Earnings to Growth, is an investment calculation that measures the value of a stock based on the current earnings and the potential future growth of the company.
# 
#         PEG = PE / EPS
# 
# - ***DY:*** It shows what percentage of the stock’s market price is being paid back in the form of a dividend that year.

# Change the variable name and calculate PEG
KLSE2 = KLSE1[['full name','code','Sector_main','sector','P/E','EPS','DY','Market_Cap']]
KLSE2 = KLSE2.rename(columns={'full name':'name','P/E':'PE','Market_Cap':'MC'})
KLSE2['PEG'] = KLSE2.PE / KLSE2.EPS
KLSE2 = KLSE2.drop(columns=['EPS'])
KLSE2.head()

# Sort value in order to get the top stock simply base on their value
KLSE_good = KLSE2.sort_values(by=['MC','PE','PEG','DY'],ascending=(False,True,True,False))
KLSE_good.head(50)

