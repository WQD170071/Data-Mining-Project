import requests
from lxml import etree
from lxml import html
import re
import time

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Referer':'https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2305666475781689&output=html&h=90&slotname=9390552809&adk=3116781417&adf=1662620477&w=970&lmt=1552753083&guci=2.2.0.0.2.2.0.0&format=970x90&url=http%3A%2F%2Fwww.investalks.com%2Fforum%2Fforum.php%3Fmod%3Dforumdisplay%26fid%3D7%26filter%3Dtypeid%26typeid%3D17&flash=0&wgl=1&dt=1552753083912&bpp=42&bdt=108&fdt=46&idt=22&shv=r20190313&cbv=r20190131&saldr=aa&abxe=1&correlator=6683659723222&frm=20&pv=2&ga_vid=691979923.1552569252&ga_sid=1552752744&ga_hid=1232295072&ga_fc=1&iag=0&icsg=12206&dssz=10&mdo=0&mso=0&u_tz=480&u_his=3&u_java=0&u_h=864&u_w=1536&u_ah=824&u_aw=1536&u_cd=24&u_nplug=3&u_nmime=4&adx=34&ady=100&biw=1026&bih=350&scr_x=0&scr_y=0&eid=21060853&oid=3&rx=0&eae=0&fc=656&brdim=426%2C33%2C426%2C33%2C1536%2C0%2C1057%2C735%2C1042%2C350&vis=1&rsz=%7C%7CeE%7C&abl=CS&ppjl=f&pfx=0&fu=16&bc=7&ifi=1&uci=1.afatrway4czq&fsb=1&xpc=kkAgITwzNl&p=http%3A//www.investalks.com&dtd=90'}

num_list = []
hot_list = []
title_list = []
time1_list = []
time2_list = []
link_list = []
stock_list = []
date1_list = []
date2_list = []

def get_page():
    url = 'http://www.investalks.com/forum/forum.php?mod=forumdisplay&fid=7&typeid=17&filter=typeid&typeid=17&page=1'
    r = requests.get(url, headers = header)
    time.sleep(2)
    html = etree.HTML(r.text)
    page = html.xpath('//div[@class="pg"]/a[@class="last"]/text()')[0].split(' ')[-1]
    return int(page)

def get_info(pages):
    for i in range(1,pages+1):
        html = 'http://www.investalks.com/forum/forum.php?mod=forumdisplay&fid=7&typeid=17&filter=typeid&typeid=17&page=' + str(i)
        html_i = requests.get(html, headers = header)
        time.sleep(2)
        selector =etree.HTML(html_i.text)
        content=selector.xpath('//table[@id="threadlisttableid"]/tbody')[2:]
        for tr in content:
            num_list.append(tr.xpath('.//td//a[@class="xi2"]//text()')[0])
            hot_list.append(tr.xpath('.//td[@class="num"]//em//text()')[0])
            title_list.append(tr.xpath('.//th//a[@class="s xst"]//text()')[0])
            stock = re.findall(r'\d+',tr.xpath('.//th//a[@class="s xst"]//text()')[0])
            stock = " ".join(stock)
            stock_list.append(stock[0:4])
            time1_list.append(tr.xpath('.//td//em//span//text()')[0][-5:])
            date1_list.append(tr.xpath('.//td//em//span//text()')[0][:-6])
            time2_list.append(tr.xpath('.//td//em//a//text()')[0][-5:])
            date2_list.append(tr.xpath('.//td//em//a//text()')[0][:-6])
            #date_latest_list.append(tr.xpath('.//td//em//'))
            link_list.append('http://www.investalks.com/forum/'+tr.xpath('.//th//a[@class="s xst"]/@href')[0])
    return

total_page = get_page()
get_info(total_page)

import pandas as pd
dataframe = pd.DataFrame({'Stock Code':stock_list,'Titles':title_list,'Hot':hot_list,'Replies':num_list,'Start_Date':date1_list,'Start_Time':time1_list,'Latest_Date':date2_list,'Latest_Time':time2_list,'Link':link_list})
sector = pd.read_csv('20_days_sector.csv')
sector = sector.rename(columns={'code':'Stock Code'})
df = pd.merge(sector.drop(['Sector_main','sector'],axis=1), dataframe, on = 'Stock Code', how = 'right')
df.to_csv("Comments_processed.csv",index=False,sep=',')
df
