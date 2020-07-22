import requests as RQ
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
import pickle
base_url = ["https://en.wikipedia.org/wiki/Category:All_articles_with_unsourced_statements"]
base_netloc = urlparse(base_url[0]).netloc
list_of_links = []
file_name = "Links.LIST"
while base_url:
    url = base_url.pop(0)
    r = RQ.get(url)
    soup = BeautifulSoup(r.content , features = "html.parser" )
    portion = soup.find("div", {"class": "mw-category"})
    for tag in portion.find_all("a", href=True):
        tag = urljoin(url,tag["href"])
        if(urlparse(tag).netloc == base_netloc):
            list_of_links.append(tag)
    portion = soup.find("div", {"class": "mw-content-ltr"})
    for tag in portion.find_all("a", href=True):
        if(tag.text == "next page"):
            base_url.append(urljoin(url,tag["href"]))
            break
    list_of_links = list(set(list_of_links))
    with open(file_name , "wb") as file:
        pickle.dump(list_of_links,file)
    print(len(list_of_links))
