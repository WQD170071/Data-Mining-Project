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

# Check the type of the dataframe 
PDF.info()

# - Debt Ratio shows a company’s ability to pay off its liabilities with its assets. 
# 
# This ratio measures the financial leverage of a company. Companies with higher levels of liabilities compared with assets are considered highly leveraged and more risky for lenders.
# This helps investors and creditors analysis the overall debt burden on the company as well as the firm’s ability to pay off the debt in future, uncertain economic times.
# - Debt Ratio = Total Liabilities / Total Assets

# Calculate the Debt Ratio and merge with sector
PDF['debt_ratio'] = PDF['total liabilities'] / PDF['total assets']
PDF1 = PDF[['code','debt_ratio']]
PDF_sector = pd.merge(PDF1,sector,how='left',on='code')
#PDF_sector

# Subset of the dataset which with the Debt Ratio lower then 50%
PDF_sector_good = PDF_sector[PDF_sector.debt_ratio < 0.5]
PDF_sector_good = PDF_sector_good.sort_values(by=['debt_ratio'],ascending=(True))
PDF_sector_good
