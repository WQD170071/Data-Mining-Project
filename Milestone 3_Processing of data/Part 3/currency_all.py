import pandas as pd
import os

def currency_csv():
    df_list = []
    url = 'https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/Currency_csv/Day_'
    SaveFile_Name = r'all_currency.csv'
    
    #Loop through the names of the individual CSV files in the list and append them to the merged file
    for i in range(1,27):
        df = pd.read_csv(url+str(i)+'.csv')
        df_list.append(df)
    
    df = pd.concat(df_list)
    df.to_csv(SaveFile_Name,index=False,sep=',')

currency_csv()


#read combined csv file
all = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/all_currency.csv', sep = ',')

#separate date_day into two columns, namely date and day
all[['date', 'day']] = all.date_day.str.split("(", expand = True)
all['day'] = all['day'].map(lambda x: x.lstrip('+-').rstrip(')'))

#remove column date_day from dataset
all = all.drop("date_day", axis = 1)
all = all.drop(columns = 'Unnamed: 0')

#shift column
columnsName = ['currency_unit', 'date', 'day', 'buy_rate', 'middle_rate', 'sell_rate']
all = all.reindex(columns = columnsName)

#write the processed dataset into a new dataset
all.to_csv('currency_preprocessed.csv', index = False)
all
