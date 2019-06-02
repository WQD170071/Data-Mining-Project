import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver

def get_PDFurl():
    pdf_links = []
    links = soup.find_all(href=re.compile(".pdf"))
    for each in links:
        pdf_links.append(each.attrs['href'])
    return pdf_links


def get_pageurl():
    page_links = []
    links = soup.find_all(href=re.compile("javascript:__doPostBack"))
    for each in links:
        page_links.append(each.attrs['href'])
    return page_links


def download_pdf(pdf_links, current_page):
    print("Downloading Page " + current_page + " : ")
    j = 1
    # download automatically pdf files from website
    for i in pdf_links:
        file_name = i.split('&name=')[-1]
        r = requests.get(i)
        # create new folder (change it to your directory)
        if not os.path.exists('PDF/Page ' + current_page):
            os.mkdir('PDF/Page ' + current_page)
        with open('PDF/Page ' + current_page + '/' + file_name, 'wb') as pdf:
            pdf.write(r.content)
            print(str(j) + '--' + file_name + '...Successful!')
            j += 1
        pdf.close()
    print('Done With Page ' + current_page + '!\n\n')
    return


url = 'https://www.malaysiastock.biz/Annual-Report.aspx'

# Set browser environment
chrome_options = webdriver.ChromeOptions()
# Using headless mode to avroid connection error
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)
browser.set_page_load_timeout(30)
browser.implicitly_wait(30)

# Download first page
browser.get(url)
time.sleep(3)
r = browser.page_source
soup = BeautifulSoup(r, 'html.parser')
pdf_links = get_PDFurl()
page_links = get_pageurl()
current_page = soup.find(class_='pgr').find('span').text
download_pdf(pdf_links, current_page)
time.sleep(2)

# Download all other pages
for i in page_links:
    browser.execute_script(i)  # turning page
    time.sleep(3)
    r = browser.page_source
    soup = BeautifulSoup(r, 'html.parser')
    pdf_links = get_PDFurl()
    current_page = soup.find(class_='pgr').find('span').text
    download_pdf(pdf_links, current_page)
    time.sleep(2)

browser.quit()
print("\n=====================ALL Done!!!=======================\n")

