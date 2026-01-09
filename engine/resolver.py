from apis.anilist import search_anilist
from apis.mangadex import search_mangadex
from apis.tmdb import search_tmdb
from apis.omdb import search_omdb

def resolve(title):
    ani = search_anilist(title)
    if ani:
        return {
            "title": ani["title"]["english"] or ani["title"]["romaji"],
            "genres": ani["genres"][:3],
            "status": ani["status"],
            "hero": ani["characters"]["nodes"][0]["name"]["full"],
            "desc": ani["description"][:300]
        }

    md = search_mangadex(title)
    if md:
        return md

    tm = search_tmdb(title)
    if tm:
        return {"title": tm.get("title") or tm.get("name"), "desc": tm.get("overview","")}

    om = search_omdb(title)
    if om:
        return {"title": om["Title"], "desc": om["Plot"]}

    return None
