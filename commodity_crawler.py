
# coding: utf-8

# In[36]:


import requests
from bs4 import BeautifulSoup
import json
class Crawler:
    """prepare to connect and retrieve data"""
    def html_parser(self,url):
        r = requests.get(url)
        if r.status_code == 200:
            print("...")
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            if soup != None:
                return soup
            else:
                print("Your request returns nothing.")
        else:
            print("Cannot connect.")
    """get list of URL
    def get_contentURL(self,lst):
        for url in lst:
            soup = self.html_parser(url)
        return soup
    """
"""go to next page if any exists"""         
def find_next_Page(soup):
    next_pageURL_lst = []
    for div in soup.find_all("div", class_= "gonum"):
        for links in div.find_all('a', href = True):
            if links not in next_pageURL_lst:
                links["href"] = "https://mart.ibon.com.tw" + links["href"]
                next_pageURL_lst.append(links["href"])
                
    return next_pageURL_lst 
            
"""find category URL"""
categoryURL_lst = []
url = 'https://mart.ibon.com.tw/mart/rui002.faces?catid=12107'
categoryURL = Crawler()
category_soup = categoryURL.html_parser(url)
for div in category_soup.find_all("div", class_="submenu"):
    for ul in div.find_all("ul", class_="l2"):
        for li in ul.find_all("li"):
            for link in li.find_all('a', class_= "open"):
                if link["href"] != "javascript:;" and link["href"] not in categoryURL_lst:
                    categoryURL_lst.append(link["href"])

"""find commodity URL"""
commodityURL_lst = []
commodityURL = Crawler()
for url in categoryURL_lst:
    commodity_soup = commodityURL.html_parser(url)
    for p in commodity_soup.find_all("p", class_=" marginB5px"):
        for link in p.find_all('a', href = True):
            if link["href"] not in commodityURL_lst:
                commodityURL_lst.append(link["href"])
print(len(commodityURL_lst))

"""get URL on next pages """
nextURL = Crawler()
next_pageURL_lst = find_next_Page(commodity_soup)
for url in next_pageURL_lst:
    next_page_soup = nextURL.html_parser(url)
    for p in next_page_soup.find_all("p", class_=" marginB5px"):
        for link in p.find_all('a', href = True):
            if link["href"] not in commodityURL_lst:
                commodityURL_lst.append(link["href"])
print(len(commodityURL_lst))

"""get content in webpages"""
contentURL = Crawler()
for url in commodityURL_lst:
    content_soup = contentURL.html_parser(url)
    for letters in content_soup.find_all('div', class_= "TabbedPanelsContentGroup"):
        for fonts in letters.find_all('font'):
            print(fonts.text)
