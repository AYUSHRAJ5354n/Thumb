import requests
from bs4 import BeautifulSoup

def get_image(title):
    try:
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ','_')}"
        soup = BeautifulSoup(requests.get(url).text,"lxml")
        img = soup.select_one("table.infobox img")
        if img:
            return "https:"+img["src"]
    except:
        pass
    return None
