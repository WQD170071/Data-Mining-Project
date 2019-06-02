import numpy
import matplotlib.pyplot as plt
import pandas as pd

from tslearn.generators import random_walks
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.piecewise import PiecewiseAggregateApproximation
from tslearn.piecewise import SymbolicAggregateApproximation, OneD_SymbolicAggregateApproximation
from tslearn.utils import to_time_series


price = pd.read_csv('Stock_Price.csv')
sector = pd.read_csv('Stock_Sector.csv')

df = pd.merge(price, sector.drop(['code'],axis=1), on = 'name', how = 'left')
#format and sort 'date' variable
df['date'] = pd.to_datetime(df.date)
data = df.sort_values(by = 'date')

#group the data by its 'name'
data_byname = data.groupby('name')

nameList = []
for name, group in data_byname:
    nameList.append(group)

df_list = []

for i in range(len(nameList)):
    try:
        df = nameList[i]
        
        dataset = [list(nameList[i].price)]
        scaler = TimeSeriesScalerMeanVariance(mu=0., std=1.)  # Rescale time series
        dataset = scaler.fit_transform(dataset)
        df['raw'] = dataset[0]
        
        # PAA transform (and inverse transform) of the data
        n_paa_segments = 10
        paa = PiecewiseAggregateApproximation(n_segments=n_paa_segments)
        paa_dataset_inv = paa.inverse_transform(paa.fit_transform(dataset))
        df['paa'] = paa_dataset_inv[0]
        
        # SAX transform
        n_sax_symbols = 4
        sax = SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols)
        sax_dataset_inv = sax.inverse_transform(sax.fit_transform(dataset))
        df['sax'] = sax_dataset_inv[0]
        
        # 1d-SAX transform
        n_sax_symbols_avg = 8
        n_sax_symbols_slope = 8
        one_d_sax = OneD_SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols_avg,
                                                        alphabet_size_slope=n_sax_symbols_slope)
                                                        one_d_sax_dataset_inv = one_d_sax.inverse_transform(one_d_sax.fit_transform(dataset))
                                                        df['one_dsax'] = one_d_sax_dataset_inv[0]
                                                        
        df_list.append(df[['name','code','date','price','raw','paa','sax','one_dsax','Sector_main','sector']])

    except ZeroDivisionError:
        pass

#df_list
df = pd.concat(df_list)
df.to_csv('Stock_paa_sax.csv',index=False,sep=',')
df
