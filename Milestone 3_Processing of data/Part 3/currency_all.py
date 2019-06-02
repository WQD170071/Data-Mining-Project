import pandas as pd
import os

SaveFile_Name = r'all_currency.csv'
file_list = os.listdir('Currency_csv')

#Sort file by days
file_list.sort(key=lambda x:int(x[4:-4]))

#Read the first CSV file and include the header
df = pd.read_csv('Currency_csv/' + file_list[0])

#Write the first CSV file read to the merged file to save
df.to_csv(SaveFile_Name, encoding="utf_8_sig", index=False)

#Loop through the names of the individual CSV files in the list and append them to the merged file
for i in range(1, len(file_list)):
    df = pd.read_csv('Currency_csv/' + file_list[i])
    df.to_csv(SaveFile_Name, encoding="utf_8_sig", index=False, header=False, mode='a+')


#read combined csv file
all = pd.read_csv('all_currency.csv', sep = ',')

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



















