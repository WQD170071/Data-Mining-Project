# import package
from selenium import webdriver
from lxml import html
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

name_list = []
code_list = []
sector_1_list = []
sector_2_list = []

sector_list = []
sector_name_list = []
sector_elements = []
sector_links = []
company_names = []
company_links = []

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Referer':'https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2305666475781689&output=html&h=90&slotname=9390552809&adk=3116781417&adf=1662620477&w=970&lmt=1552753083&guci=2.2.0.0.2.2.0.0&format=970x90&url=http%3A%2F%2Fwww.investalks.com%2Fforum%2Fforum.php%3Fmod%3Dforumdisplay%26fid%3D7%26filter%3Dtypeid%26typeid%3D17&flash=0&wgl=1&dt=1552753083912&bpp=42&bdt=108&fdt=46&idt=22&shv=r20190313&cbv=r20190131&saldr=aa&abxe=1&correlator=6683659723222&frm=20&pv=2&ga_vid=691979923.1552569252&ga_sid=1552752744&ga_hid=1232295072&ga_fc=1&iag=0&icsg=12206&dssz=10&mdo=0&mso=0&u_tz=480&u_his=3&u_java=0&u_h=864&u_w=1536&u_ah=824&u_aw=1536&u_cd=24&u_nplug=3&u_nmime=4&adx=34&ady=100&biw=1026&bih=350&scr_x=0&scr_y=0&eid=21060853&oid=3&rx=0&eae=0&fc=656&brdim=426%2C33%2C426%2C33%2C1536%2C0%2C1057%2C735%2C1042%2C350&vis=1&rsz=%7C%7CeE%7C&abl=CS&ppjl=f&pfx=0&fu=16&bc=7&ifi=1&uci=1.afatrway4czq&fsb=1&xpc=kkAgITwzNl&p=http%3A//www.investalks.com&dtd=90'}

def get_sectors():
    # set up browser
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome() # open web page
    browser.implicitly_wait(10)  # wait for web page to load

    url = 'https://www.thestar.com.my/business/marketwatch/'
    browser.get(url)
    r = browser.page_source
    html = BeautifulSoup(r, 'html.parser')
    # print(html)
    browser.close()

    # sector elements
    htmlPart = html.find(class_=re.compile("stocks"))
    linkPart = [x.get_attribute_list('id') for x in htmlPart.find_all('a', {"id": True})]
    for i in range(len(linkPart)):
        sector_elements.extend(linkPart[i])
    # print(linkPart)
    # print(sector_elements)
    # print(len(sector_elements))

    # sector_list
    sector = html.find_all('strong')
    for i in sector:
        sector_list.append(i.text.strip(':'))
        # print(i.text)
    # print(sector_list)

    # sector_name_list
    sector_n = html.select('div.text a')
    for i in sector_n:
        sector_name_list.append(i.text)
    # print(sector_name_list)

    return


def get_company_names():
    for l in sector_list:
        for e, n in zip(sector_elements, sector_name_list):
            if l.lower()[0] == e[0]:
                # set up browser
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.managed_default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                browser = webdriver.Chrome(options=chrome_options)
                # browser = webdriver.Chrome() # open web page
                browser.implicitly_wait(10)  # wait for web page to load

                url_s = 'https://www.thestar.com.my/business/marketwatch/stock-list/?sector=' + e
                # sector_links.append(url_s)
                browser.get(url_s)
                name_list = browser.find_elements_by_xpath(
                    '//table[@class="market-trans"]//tr[@class="linedlist"]/td/a')
                for name in name_list:
                    if name.text != '':
                        name_text = name.text.replace("&", "%26")
                        company_names.append(name_text)
                        sector_1_list.append(l)
                        sector_2_list.append(n)
                browser.close()

    # save as links for crawling all the information
    for n in company_names:
        link = 'https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=' + n
        company_links.append(link)

    return

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
        code = tree.xpath('//li[@class="f14"]/text()')[1]

        name_list.append(name)
        print(name)
        code_list.append(code[3:])
        print(code[3:])

        return


class App:

    def __init__(self, name, code, links):
        self.name = name
        self.code = code
        self.links = links

    def __str__(self):
        return ("Name: " + self.name.encode('UTF-8') +
                "\r\nCode: " + self.developer.encode('UTF-8') + "\r\n")


get_sectors()
get_company_names()

for link_c in company_links:
    crawler = AppCrawler(link_c, 0)
    crawler.crawl()

na = name_list
co = code_list
s1 = sector_1_list
s2 = sector_2_list

dataframe = pd.DataFrame({'name': na, 'code': co, 'Sector_main': s1, 'sector': s2})

# save data
#dataframe.to_csv("sector.csv", index=False, sep=',')
print(dataframe)
