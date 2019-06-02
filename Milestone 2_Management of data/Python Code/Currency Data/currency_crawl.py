from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()
driver.get("http://www.bnm.gov.my/?tpl=exchangerates")

currency = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/section/div/div/div/div/div[2]/table[4]/tbody/tr[20]/td[2]")
date = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/section/div/div/div/div/div[2]/table[4]/tbody/tr[1]/th[2]/b")
buy = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/section/div/div/div/div/div[2]/table[4]/tbody/tr[20]/td[3]")
sell = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/section/div/div/div/div/div[2]/table[4]/tbody/tr[20]/td[5]")
middle = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/section/div/div/div/div/div[2]/table[4]/tbody/tr[20]/td[7]")


currency_unit = currency.text
date_day = date.text
buy_rate = buy.text
sell_rate = sell.text
middle_rate = middle.text

dataframe = pd.DataFrame({"currency_unit":currency_unit, "date_day":date_day, "buy_rate":buy_rate, "sell_rate":sell_rate, "middle_rate":middle_rate}, index = [0])
# dataframe.to_csv("currency.csv",index=False,sep=',')
print(dataframe)
