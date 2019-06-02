import pandas as pd
import os

##### part 1 : preprocessed data
# Merge all the dataset together

def price_csv():
    df_list = []
    url = 'https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/Price_csv/Day_'
    SaveFile_Name = r'Stock_Price.csv'
    
    #Loop through the names of the individual CSV files in the list and append them to the merged file
    for i in range(1,42):
        df = pd.read_csv(url+str(i)+'.csv')
        df_list.append(df)
    
    df = pd.concat(df_list)
    df.to_csv(SaveFile_Name,index=False,sep=',')
    return(df)

def sector_csv():
    df_list = []
    url = 'https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/Sector_csv/sector'
    SaveFile_Name = r'Stock_Sector.csv'
    #Loop through the names of the individual CSV files in the list and append them to the merged file
    for i in range(1,17):
        df = pd.read_csv(url+str(i)+'.csv')
        df_list.append(df)
    
    df = pd.concat(df_list)
    df = df.drop_duplicates()
    df.to_csv(SaveFile_Name,index=False,sep=',')
    return(df)

price_csv()
sector_csv()

# read csv files
price = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/Stock_Price.csv')
sector = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/Stock_Sector.csv')

# merge price and sector
stock = pd.merge(price, sector.drop(['code'],axis=1), on = 'name', how = 'left')
stock.to_csv('All_Stocks.csv',index=False,sep=',')
print(stock)

# just check how many missing value each variable, using 'x' indicate missing
df1 = stock
df1 = df1.replace('-','x')
df1 = df1.fillna('x')
(df1 == 'x').astype(int).sum(axis=0)

##### part 2 : calculating percentage of change in price
# read the merged stock file
data = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/All_Stocks.csv')

#format and sort 'date' variable
data['date'] = pd.to_datetime(data.date)
data = data.sort_values(by = 'date')

#group the data by its 'name'
data_byname = data.groupby('name')

nameList = []
for name, group in data_byname:
    nameList.append(group)

#create a column 'change'
#calculate the percentage of change of stock : change = (todayprice-yesterdayprice)/yesterdayprice
for j in nameList:
    #print(j)
    j['change'] = (j['price']-j['price'].shift(1))/j['price'].shift(1)

#save data into csv file
nameList[0].to_csv('pct_chg_all.csv', index=False)
for k in nameList[1:]:
    k.to_csv('pct_chg_all.csv', index=False, header=False, mode='a+')

##### part 3 : filtering data by market and sector
df = pd.read_csv('https://raw.githubusercontent.com/WQD170071/Data-Mining-Project/master/Dataset/Milestone%203/pct_chg_all.csv')
# create new folder
if os.path.exists('market')==False:
    os.mkdir('market')
#separate dataset into diff_main_sector
#main market
df_main = df.loc[df['Sector_main'] == 'Main Market']
df_main.to_csv('market/all_Main_Market.csv', index = False)

#ace market
df_ace = df.loc[df['Sector_main'] == 'Ace Market']
df_ace.to_csv('market/all_Ace_Market.csv', index = False)

#bond&loan
df_bond_loan = df.loc[df['Sector_main'] == 'Bond & Loan']
df_bond_loan.to_csv('market/all_Bond&Loan.csv', index = False)

#etf
df_etf = df.loc[df['Sector_main'] == 'ETF']
df_etf.to_csv('market/all_ETF.csv', index = False)

#warrants
df_warrants = df.loc[df['Sector_main'] == 'Warrants']
df_warrants.to_csv('market/all_Warrants.csv', index = False)

##### part 4 : creating pivot table to see the relationship of each stocks within the same sector and the same market
market = os.listdir('market')
# create new folder
if os.path.exists('market/pivot_table')==False:
    os.mkdir('market/pivot_table')
for m in market:
    data1 = pd.read_csv('market/' + m)
    #get the first element in column sector_main
    filename1 = data1['Sector_main'].iloc[0]
    #group stock together by sector
    sector = data1.groupby('sector')
    sectorList = []
    #create a list containing dataframe for each sector
    for name, group in sector:
        sectorList.append(group)
        
        for n in sectorList:
            dataframe = pd.DataFrame(n)
            #get the first element in column sector
            filename2 = dataframe['sector'].iloc[0]
            #give name to a new csv filr
            filename = 'pivot_' + filename1 + '_' + filename2 + '.csv'
            #build a pivot table for each sector
            df_new = pd.pivot_table(dataframe, index = 'date', columns = 'name', values = 'change')
            #export to csv file
            df_new.to_csv('market/pivot_table/' + filename)

##### part 5 : correlation analysis
data2 = os.listdir('market/pivot_table')

corrList = []
nameList1= []

for df in data2:
    #read csv
    data3 = pd.read_csv('market/pivot_table/' + df)
    #shorten the file name for naming excel tabs
    df = df.replace('Warrants', 'W')
    df = df.replace('Ace Market', 'AM')
    df = df.replace('Main Market', 'MM')
    df = df.replace('Bond & Loan', 'BL')
    df = df.replace('Industrial Products & Services', 'IPS')
    df = df.replace('Consumer Products & Services', 'CPS')
    df = df.replace('Telecommunications & Media', 'TM')
    df = df.replace('Transportation & Logistics', 'TL')
    df = df.replace('Exchange Traded Fund', 'ETF')
    df = df.replace('Real Estate Investment Trusts', 'REIT')
    df = df.replace('Special Purpose Acquisition Company', 'SPAC')
    df = df.replace('Financial Services', 'FS')
    df = df.replace('Bond Islamic', 'BI')
    df = df.replace('Closed End Fund', 'CEF')
    a = os.path.splitext(df)[0]
    name = a[6:]
    nameList1.append(name)
    #correlation
    col_name = list(data3.columns.values)
    col_name.remove('date')
    correlation = data3[col_name].corr()
    correlation = round(correlation, 5)
    #print(correlation)
    corrList.append(correlation)

#function to produce excel file containing all correlation results
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name, engine = 'xlsxwriter')
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0)
    writer.save()

#run function
dfs_tabs(corrList, nameList1, 'correlation_results.xlsx')
   
df = pd.read_excel('correlation_results.xlsx')
df
