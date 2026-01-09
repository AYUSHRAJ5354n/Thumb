import requests
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from apis.anilist import search_anilist
from apis.mangadex import search_mangadex
from apis.tmdb import search_tmdb
from apis.omdb import search_omdb
from apis.wikipedia import get_image


async def generate_thumbnail(title, bg_url):
    # Download background
    bg = Image.open(BytesIO(requests.get(bg_url).content)).convert("RGB")
    bg = bg.resize((1280, 720))

    # Resolve metadata
    data = None
    ani = search_anilist(title)
    if ani:
        data = {
            "title": ani["title"]["english"] or ani["title"]["romaji"],
            "desc": ani["description"][:300],
            "hero": ani["characters"]["nodes"][0]["name"]["full"],
        }
    else:
        md = search_mangadex(title)
        if md:
            data = md
        else:
            tm = search_tmdb(title)
            if tm:
                data = {"title": tm.get("title") or tm.get("name"), "desc": tm.get("overview","")}
            else:
                om = search_omdb(title)
                if om:
                    data = {"title": om["Title"], "desc": om["Plot"]}
                else:
                    data = {"title": title, "desc": ""}

    # Draw layout
    draw = ImageDraw.Draw(bg)
    font = ImageFont.load_default()

    draw.rectangle((0, 500, 1280, 720), fill=(0, 0, 0, 180))
    draw.text((40, 520), data["title"], fill="white", font=font)
    draw.text((40, 560), data.get("desc","")[:200], fill="white", font=font)

    # Save output
    out_path = "/tmp/poster.png"
    bg.save(out_path)
    return out_path
