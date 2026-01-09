import requests
from config import ANILIST_URL

QUERY = """
query ($search: String) {
  Media(search: $search, type: ANIME) {
    title { romaji english }
    status
    genres
    description(asHtml:false)
    characters(sort:ROLE) {
      nodes {
        name { full }
        image { large }
      }
    }
  }
}
"""

def search_anilist(title):
    try:
        r = requests.post(ANILIST_URL, json={"query":QUERY,"variables":{"search":title}}, timeout=10)
        return r.json()["data"]["Media"]
    except:
        return None
