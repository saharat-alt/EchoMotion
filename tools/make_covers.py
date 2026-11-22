"""Covers (ปก) for the three 2026-11-23 clips, Western YouTube/Shorts thumbnail style (user 2026-11-23: "ตัมเนลสวยๆสไตล์ฝรั่ง"):
full-bleed image, one cut-out subject with a white outline, 2-4 huge words with a thick ink stroke, one highlighted word,
one arrow/circle on the point. Key content kept inside the middle 1080x1350 (IG grid crops 9:16 to 4:5).
usage: .venv/bin/python tools/make_covers.py  -> work/covers/out/*.png (inputs: work/covers/safe_cut.png, cut from the raw take; never committed)"""
import pathlib
from playwright.sync_api import sync_playwright

R = pathlib.Path(__file__).resolve().parents[1]
C = R / "work/covers"; (C / "out").mkdir(exist_ok=True)
u = lambda p: (R / p).resolve().as_uri()
FONTS = f"""
@font-face{{font-family:KB;src:url({u('brand/fonts/Kanit-Black.ttf')})}}
@font-face{{font-family:KBo;src:url({u('brand/fonts/Kanit-Bold.ttf')})}}
@font-face{{font-family:RH;src:url({u('brand/fonts/RedHatDisplay-Var.ttf')});font-weight:300 900}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:KB}}
.big{{position:absolute;left:0;right:0;text-align:center;color:#fff;line-height:1.02;paint-order:stroke fill;-webkit-text-stroke:22px #111;
     text-shadow:0 14px 0 #111,0 22px 40px rgba(0,0,0,.55)}}
.hl{{color:#FFD43B}} .or{{color:#FE4C1C}}
.cut{{position:absolute;filter:drop-shadow(0 0 0 #fff) drop-shadow(9px 0 0 #fff) drop-shadow(-9px 0 0 #fff) drop-shadow(0 9px 0 #fff) drop-shadow(0 -9px 0 #fff) drop-shadow(0 30px 40px rgba(0,0,0,.5))}}
.pill{{position:absolute;font:800 46px RH;padding:14px 34px;border-radius:60px;background:#fff;color:#111;box-shadow:0 10px 30px rgba(0,0,0,.35)}}
.logo{{position:absolute;right:44px;top:60px;height:96px}}
.credit{{position:absolute;left:30px;bottom:24px;font:500 20px KBo;color:rgba(255,255,255,.75)}}
"""
ARROW = lambda x, y, rot, col="#FE4C1C", s=1: f"""<svg style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg) scale({s});filter:drop-shadow(0 8px 0 #111)" width="260" height="160" viewBox="0 0 260 160">
<path d="M10 120 C 70 30, 150 20, 200 60" fill="none" stroke="{col}" stroke-width="26" stroke-linecap="round"/><path d="M175 15 L 250 75 L 160 100 Z" fill="{col}"/></svg>"""

COVERS = {
 # เซฟพูด: Safe's own line "ใครอยากให้แบรนด์ดูแพงแบบประหยัดงบ" + "ฟรี" (both said in the clip)
 "pomelli": f"""<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 38%,#FF7A45 0%,#FE4C1C 45%,#8A1E05 100%)"></div>
  <img src="{u('jobs/type1_talkinghead/2026-11-22_google_pomelli/assets/web/z_poster.png')}" style="position:absolute;left:620px;top:400px;width:320px;transform:rotate(7deg);border:10px solid #fff;border-radius:18px;box-shadow:0 30px 60px rgba(0,0,0,.45)">
  <img src="{u('jobs/type1_talkinghead/2026-11-22_google_pomelli/assets/web/z_colors.png')}" style="position:absolute;left:80px;top:460px;width:400px;transform:rotate(-6deg);border:10px solid #fff;border-radius:18px;box-shadow:0 30px 60px rgba(0,0,0,.45)">
  <img class="cut" src="{u('work/covers/safe_cut.png')}" style="left:0;top:900px;width:1160px">
  <div class="big" style="top:250px;font-size:150px">แบรนด์ดูแพง</div>
  <div class="big" style="top:700px;font-size:200px">AI <span class="hl">ฟรี!</span></div>
  <div class="pill" style="left:50%;transform:translateX(-50%);top:1720px">Google Pomelli</div>
  <img class="logo" style="top:40px;height:80px" src="{u('brand/logo/DataEchooo-logo-WH.png')}">
  <div class="credit">ภาพหน้าจอ: Google (blog.google)</div>""",
 # เล่า Business: the hook line "IPO ใหญ่ที่สุดในประวัติศาสตร์ ... ขาดทุนแสนล้านดอลลาร์"
 "anthropic": f"""<img src="{u('jobs/type3_story/2026-11-22_anthropic_ipo/assets/photos/nasdaq.jpg')}" style="position:absolute;height:1920px;left:-700px;top:0;filter:saturate(1.2) brightness(.55)">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,12,30,.2),rgba(10,12,30,.85) 75%)"></div>
  <div style="position:absolute;left:50%;top:650px;transform:translateX(-50%) rotate(-3deg);background:#F0EEE6;border:12px solid #fff;border-radius:34px;padding:56px 70px;box-shadow:0 40px 80px rgba(0,0,0,.6)">
    <img src="{u('jobs/type3_story/2026-11-22_anthropic_ipo/assets/photos/antlogo.png')}" style="display:block;width:560px"></div>
  <svg style="position:absolute;left:120px;top:960px" width="840" height="300" viewBox="0 0 840 300">
    <polyline points="0,260 180,230 330,60 440,20" fill="none" stroke="#2FE07A" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>
    <polyline points="440,20 560,90 680,120 820,150" fill="none" stroke="#FF3B3B" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/></svg>
  <div class="big" style="top:250px;font-size:180px">IPO <span class="hl">ใหญ่สุด</span></div>
  <div class="big" style="top:450px;font-size:96px">ในประวัติศาสตร์</div>
  <div class="big" style="top:1230px;font-size:120px">แต่ขาดทุน</div>
  <div class="big or" style="top:1380px;font-size:170px">แสนล้าน $</div>
  <img class="logo" style="top:40px;height:80px" src="{u('brand/logo/DataEchooo-logo-WH.png')}">
  <div class="credit">ภาพ: ajay_suresh (CC BY 2.0) · Anthropic logo</div>""",
 # เล่าข่าว: the hook "โจทย์เลขที่ไม่มีใครแก้ได้มา 167 ปี Claude เพิ่งช่วยแก้ได้" — claim not yet verified, so "?"
 "math": f"""<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#2A3B5C 0%,#141C2E 60%,#0A0E18 100%)"></div>
  <div style="position:absolute;inset:0;font:italic 400 64px 'Times New Roman';color:rgba(255,255,255,.13);line-height:1.9;padding:40px 60px;transform:rotate(-8deg) scale(1.2)">
   ζ(s) = Σ 1/nˢ &nbsp; Re(s) = ½ &nbsp; π(x) ~ x / ln x &nbsp; ζ(½+it) = 0 &nbsp; 2, 3, 5, 7, 11, 13, 17 &nbsp; ζ(s) = Π 1/(1−p⁻ˢ) &nbsp; Re(s) = ½ &nbsp; ζ(s) = Σ 1/nˢ &nbsp; 19, 23, 29, 31 &nbsp; π(x) ~ Li(x)</div>
  <div class="big" style="top:250px;font-size:96px">โจทย์ที่ไม่มีใครแก้ได้</div>
  <div class="big hl" style="top:360px;font-size:330px;letter-spacing:-6px">167 ปี</div>
  <div style="position:absolute;left:60px;top:860px;background:#F0EEE6;border:10px solid #fff;border-radius:28px;padding:30px 40px;transform:rotate(-4deg);box-shadow:0 30px 60px rgba(0,0,0,.6)">
    <img src="{u('library/logos/claude_lockup.svg')}" style="display:block;width:380px"></div>
  <div class="big" style="top:1080px;left:20px;right:auto;width:520px;font-size:160px">แก้ได้<span class="or">?</span></div>
  <img class="cut" src="{u('brand/mascot/poses/wow.png')}" style="right:-50px;bottom:-40px;width:620px">
  <img class="logo" style="top:40px;height:80px" src="{u('brand/logo/DataEchooo-logo-WH.png')}">""",
}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"]); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for name, body in COVERS.items():
        f = C / f"{name}.html"; f.write_text(f"<!doctype html><meta charset=utf-8><style>{FONTS}</style><body>{body}</body>", encoding="utf-8")
        pg.goto(f.as_uri()); pg.wait_for_timeout(700); pg.screenshot(path=str(C / "out" / f"{name}.png")); print("wrote", name)
    b.close()
