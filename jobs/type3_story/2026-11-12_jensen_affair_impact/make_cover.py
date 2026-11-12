"""Cover (9:16, 1080x1920) for the Jensen Huang clip: real photo + one big question, brand colours/fonts from brand/brand.json.
usage: python make_cover.py  -> out/cover_v1.png"""
import json, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
here = pathlib.Path(__file__).parent; root = here.parents[2]
B = json.loads((root / "brand/brand.json").read_text(encoding="utf-8")); C = {k: v["hex"] for k, v in B["colors"].items() if isinstance(v, dict) and "hex" in v}
F = lambda name, size: ImageFont.truetype(str(root / "brand/fonts" / name), size)
W, H = 1080, 1920
im = Image.new("RGB", (W, H), C.get("ice", "#F3F7FF")); d = ImageDraw.Draw(im)
# faint brand grid
for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill="#E6EDFF")
for y in range(0, H, 60): d.line([(0, y), (W, y)], fill="#E6EDFF")
# photo print (face kept clear, upper half)
ph = Image.open(here / "assets/photos/jensen_portrait.jpg").convert("RGB")
ph = ImageOps.fit(ph, (820, 860), centering=(0.5, 0.32))
frame = Image.new("RGB", (860, 960), "white"); frame.paste(ph, (20, 20))
fd = ImageDraw.Draw(frame); fd.text((840, 925), "ภาพ: Anderseidesvik / Wikimedia Commons (CC BY-SA 4.0)", font=F("IBMPlexSansThai-Regular.ttf", 20), fill="#7A84A6", anchor="rs")
sh = Image.new("RGBA", (900, 1040), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([20, 30, 880, 990], fill=(14, 26, 77, 90))
sh = sh.filter(ImageFilter.GaussianBlur(18))
rot = frame.rotate(2.2, expand=True, fillcolor=None, resample=Image.BICUBIC)
im.paste(sh.rotate(2.2, expand=True), (90, 270), sh.rotate(2.2, expand=True))
mask = Image.new("L", frame.size, 255).rotate(2.2, expand=True)
im.paste(rot, (110, 260), mask)
# title block
d = ImageDraw.Draw(im)
def center(txt, y, font, fill, stroke=0, sc=None):
    d.text((W // 2, y), txt, font=font, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sc)
d.rounded_rectangle([60, 1250, W - 60, 1700], radius=40, fill=C.get("blue", "#214AFF"))
center("เรื่องนอกใจ", 1350, F("Kanit-Black.ttf", 120), "white")
center("ทำหุ้นหาย 15 ล้านล้านบาท?", 1500, F("Kanit-Black.ttf", 74), C.get("sky", "#9EE8FF"))
center("Jensen Huang · NVIDIA", 1625, F("Kanit-Bold.ttf", 52), "white")
d.rounded_rectangle([W // 2 - 230, 1750, W // 2 + 230, 1840], radius=45, fill=C.get("orange", "#FE4C1C"))
center("เล่า Business", 1795, F("Kanit-Bold.ttf", 50), "white")
logo = Image.open(root / "brand" / B["logo"]["color"]).convert("RGBA"); lw = 190
logo = logo.resize((lw, int(lw * logo.height / logo.width))); im.paste(logo, (W - lw - 60, 40), logo)
(here / "out").mkdir(exist_ok=True); im.save(here / "out/cover_v1.png"); print("out/cover_v1.png")
