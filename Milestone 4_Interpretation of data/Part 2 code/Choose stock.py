#!/usr/bin/env python
# coding: utf-8

# Import packages
import pandas as pd
import numpy as np
import os


# ## -- Part 2 --

# - From Part one we can get the information that lead us to selecting some sector out of the entir dataset, and then, from each sector, choose top 8-10 stock to analysis their stock price and performance. 

# Choose the top 50 stocks from three difference sources, and then combine all together
PDF_code = PDF_sector_good.dropna().head(50)[['code','Sector_main','sector']]
KLSE_code = KLSE_good.dropna().head(50)[['code','Sector_main','sector']]
news_code = news_count.dropna().head(50)[['code','Sector_main','sector']]

# Choose a stock that is included in multiple sources
top_code1 = top_code[top_code.duplicated('code')]
top_code_most = top_code1.drop_duplicates('code',keep='last')
top_code_most

