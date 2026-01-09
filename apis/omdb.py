import requests
from config import OMDB_KEYS

def search_omdb(title):
    for key in OMDB_KEYS:
        try:
            r = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={key}", timeout=10)
            data = r.json()
            if data.get("Response")=="True":
                return data
        except:
            pass
    return None
