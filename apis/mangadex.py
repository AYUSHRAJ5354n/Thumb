import requests
from config import MANGADEX_URL

def search_mangadex(title):
    try:
        r = requests.get(f"{MANGADEX_URL}/manga", params={"title":title,"limit":1}, timeout=10)
        data = r.json()["data"]
        if not data:
            return None
        manga = data[0]
        return {
            "title": manga["attributes"]["title"].get("en"),
            "genres": [t["attributes"]["name"]["en"] for t in manga["attributes"]["tags"]][:3],
            "status": manga["attributes"]["status"],
            "desc": manga["attributes"]["description"].get("en","")
        }
    except:
        return None
