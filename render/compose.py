from PIL import ImageDraw, ImageFont
from render.template import base

def compose(bg, data):
    img = base(bg)
    d = ImageDraw.Draw(img)
    f = ImageFont.load_default()
    d.text((30,30), data.get("title",""), fill="white", font=f)
    d.text((30,60), " ".join(data.get("genres",[])), fill="white", font=f)
    d.text((900,200), data.get("desc","")[:300], fill="white", font=f)
    return img
