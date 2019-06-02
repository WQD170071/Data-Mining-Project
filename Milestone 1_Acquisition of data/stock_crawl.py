# import packages
from selenium import webdriver
from lxml import html
import requests
import pandas as pd

##-----------------------------------------------------------------------------------------------------------
## Crawl for company names
# disable picture
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(options=chrome_options)
# browser = webdriver.Chrome() # open web page
browser.implicitly_wait(10)  # wait for web page to load

company_names = []  # save company names in a list
# crawl all company names from A-Z
for i in range(65, 91):
    url = 'https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet=' + chr(i)
    browser.get(url)

    name_list = browser.find_elements_by_xpath('//table[@class="market-trans"]//tr[@class="linedlist"]/td/a')
    for name in name_list:
        if name.text != '':
            name_text = name.text.replace("&", "%26")
            company_names.append(name_text)

# crawl all company names in 0-9
url1 = 'https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet=0-9'
browser.get(url1)
name1_list = browser.find_elements_by_xpath('//table[@class="market-trans"]//tr[@class="linedlist"]/td/a')
for name1 in name1_list:
    if name1.text != '':
        name1_text = name1.text.replace("&", "%26")
        company_names.append(name1_text)

# print(company_names)
browser.close()

# save as links for crawling all the information
company_links = []
for n in company_names:
    link = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=' + n
    company_links.append(link)

##-----------------------------------------------------------------------------------------------------------
## Crawl for stock price

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Referer':'https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2305666475781689&output=html&h=90&slotname=9390552809&adk=3116781417&adf=1662620477&w=970&lmt=1552753083&guci=2.2.0.0.2.2.0.0&format=970x90&url=http%3A%2F%2Fwww.investalks.com%2Fforum%2Fforum.php%3Fmod%3Dforumdisplay%26fid%3D7%26filter%3Dtypeid%26typeid%3D17&flash=0&wgl=1&dt=1552753083912&bpp=42&bdt=108&fdt=46&idt=22&shv=r20190313&cbv=r20190131&saldr=aa&abxe=1&correlator=6683659723222&frm=20&pv=2&ga_vid=691979923.1552569252&ga_sid=1552752744&ga_hid=1232295072&ga_fc=1&iag=0&icsg=12206&dssz=10&mdo=0&mso=0&u_tz=480&u_his=3&u_java=0&u_h=864&u_w=1536&u_ah=824&u_aw=1536&u_cd=24&u_nplug=3&u_nmime=4&adx=34&ady=100&biw=1026&bih=350&scr_x=0&scr_y=0&eid=21060853&oid=3&rx=0&eae=0&fc=656&brdim=426%2C33%2C426%2C33%2C1536%2C0%2C1057%2C735%2C1042%2C350&vis=1&rsz=%7C%7CeE%7C&abl=CS&ppjl=f&pfx=0&fu=16&bc=7&ifi=1&uci=1.afatrway4czq&fsb=1&xpc=kkAgITwzNl&p=http%3A//www.investalks.com&dtd=90'}


class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link,headers = header)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        code = tree.xpath('//li[@class="f14"]/text()')[1]
        date = tree.xpath('//span[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        time = tree.xpath('//span[@id="slcontent_0_ileft_0_timetxt"]/text()')[0]
        open_price = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        low = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        high = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        vol = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        buy_vol = tree.xpath('//td[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        sell_vol = tree.xpath('//td[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]

        name_list.append(name)
        print(name)
        code_list.append(code[3:])
        # print(code[3:])
        price_list.append(price)
        # print(price)
        date_list.append(date[10:21])
        # print(date[10:21])
        time_list.append(time)
        # print(time)
        open_price_list.append(open_price)
        # print(open_price)
        low_list.append(low)
        # print(low)
        high_list.append(high)
        # print(high)
        vol_list.append(vol)
        # print(vol)
        buy_vol_list.append(buy_vol)
        # print(buy_vol)
        sell_vol_list.append(sell_vol)
        # print(sell_vol)

        return


class App:

    def __init__(self, name, code, price, links):
        self.name = name
        self.code = code
        self.price = price
        self.links = links

    def __str__(self):
        return ("Name: " + self.name.encode('UTF-8') +
                "\r\nCode: " + self.developer.encode('UTF-8') +
                "\r\nPrice: " + self.price.encode('UTF-8') + "\r\n")


# create list for all the variables
name_list = []
code_list = []
price_list = []
date_list = []
time_list = []
open_price_list = []
low_list = []
high_list = []
vol_list = []
buy_vol_list = []
sell_vol_list = []

for l in company_links:
    crawler = AppCrawler(l, 0)
    crawler.crawl()

##-----------------------------------------------------------------------------------------------------------
## Save data as .csv file
na = name_list
co = code_list
da = date_list
ti = time_list
op = open_price_list
lo = low_list
hi = high_list
pr = price_list
vo = vol_list
bv = buy_vol_list
sv = sell_vol_list

dataframe = pd.DataFrame({'name':na,'code':co,'date':da,'time':ti,'open':op,'low':lo,'high':hi,'price':pr,'volume':vo,'buy/volum':bv,'sell/volum':sv})

# save data
print(dataframe)
# dataframe.to_csv("Day_9.csv",index=False,sep=',')
