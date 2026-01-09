import requests
from config import TMDB_API_KEY

def search_tmdb(title):
    try:
        url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title}"
        r = requests.get(url, timeout=10)
        res = r.json()["results"]
        return res[0] if res else None
    except:
        return None
