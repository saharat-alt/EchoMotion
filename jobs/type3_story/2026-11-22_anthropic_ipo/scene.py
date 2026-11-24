"""เล่า Business / Anthropic IPO v1: caption_script.txt + input/words.json -> scene.json for engine/pages/story2d.html.
Grammar from the type 3 baselines (one spoken phrase = one cut, counters on every number, push on place changes),
plus the owner review of EP01 (REF_SPEC 37): light captions (mode 'soft'), paper cards over a blurred plate instead of
plain blue cards, words appear by word, the price pill only while the IPO day is told, toned-down plates (REF_SPEC 36).
usage: python scene.py   (writes scene.json + music_mute.txt)"""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parents[2] / "engine"))
from captions import sets_from_script

words = json.loads((here / "input/words.json").read_text(encoding="utf-8"))
caps = sets_from_script((here / "caption_script.txt").read_text(encoding="utf-8"), words,
                        ["IPO", "Anthropic", "OpenAI", "Claude", "Dario", "Daniela", "Nasdaq", "SpaceX", "แสนล้าน", "ล้านล้าน", "34%"])
ALL = list(caps); TXT = ["".join(w["text"] for w in c["words"]).replace(" ", "") for c in ALL]
GAP = json.loads((here / "input/title_gap.json").read_text())
END = round(caps[-1]["end"] + 2.2, 2)

def T(s, n=1, off=0.0):  # start of the n-th caption set containing s
    hits = [c["start"] for c, x in zip(ALL, TXT) if s.replace(" ", "") in x]
    assert len(hits) >= n, (s, n, TXT); return round(hits[n - 1] + off, 3)

P = {k: f"assets/plates/{v}.png" for k, v in {"lab": "p01_lab", "startup": "p02_startup", "server": "p03_server", "exchange": "p04_exchange",
                                               "bills": "p05_bills", "board": "n_boardroom", "trade": "n_trading",
    # v5 (user 2026-11-24 "มีแต่ห้องประชุม ออฟฟิศ ห้องประชุม" + Pinterest refs r2/r5): one photoreal muted set per story beat (docs/prompts/codex_type3_cinematic_plates.md)
    "c_facade": "e01_exchange_facade", "c_ledger": "e02_red_ledger", "c_lab21": "e03_research_lab", "c_leaving": "e04_leaving", "c_caution": "e05_caution",
    "c_startup": "e06_small_startup", "c_launch": "e07_launch_night", "c_deals": "e08_term_sheets", "c_skyline": "e09_skyline_up", "c_tradeup": "e10_trading_up",
    "c_tradedown": "e11_trading_down", "c_build": "e12_datacenter_build", "c_bubble": "e13_bubble"}.items()}
def cam(z0, z1, x0=540, y0=960, x1=None, y1=None):
    return {"z": [z0, z1], "x": [x0, x1 if x1 is not None else x0], "y": [y0, y1 if y1 is not None else y0]}
S = []
def shot(t0, t1, **kw): S.append(dict(t0=round(t0, 3), t1=round(t1, 3), **kw))
NUM = dict(color="#214AFF", glow="rgba(255,255,255,.95)")
RED = dict(color="#FE4C1C", glow="rgba(255,255,255,.95)")
def A(who, x, y=1250, s=1.35, pose="idle", face="neutral", **k): return dict({"who": who, "x": x, "y": y, "scale": s, "pose": pose, "face": face}, **k)
FOUNDERS = [A("dario", 300), A("daniela", 470, face="smile"), A("staff", 640), A("analyst", 790, dir=-1)]
PH = {k: f"assets/{v}" for k, v in {"npr": "docs/npr.png", "aj": "docs/aj.png", "fox": "docs/fox.png", "claude23": "docs/claude23.png",
                                     "dario": "photos/dario.jpg", "nasdaq": "photos/nasdaq.jpg", "antlogo": "photos/antlogo.png"}.items()}
CR = {"npr": "ภาพ: NPR / AFP via Getty Images (หน้าข่าว 19 พ.ย. 2026)", "aj": "ที่มา: Al Jazeera 19 พ.ย. 2026", "fox": "ที่มา: Fox Business 19 พ.ย. 2026",
      "anthropic": "ที่มา: anthropic.com 14 มี.ค. 2023", "dario": "ภาพ: TechCrunch / Wikimedia Commons (CC BY 2.0)",
      "nasdaq": "ภาพ: ajay_suresh / Wikimedia Commons (CC BY 2.0)"}
LOGO = {"claude": "../../../library/logos/claude_official.png", "openai": "../../../library/logos/openai_official.png"}

# ---- hook (≤ 4 s, REF_SPEC 46): the record IPO, then the loss
shot(0, T("ของบริษัทที่9เดือน"), plate="c_facade", cam=cam(1.05, 1.15, 760, 800),
     photos=[{"img": PH["npr"], "at": 0.0, "x": 540, "y": 880, "w": 880, "h": 760, "rot": -0.02, "focus": [0.5, 0.62], "credit": CR["npr"]}])
shot(T("ของบริษัทที่9เดือน"), GAP["at"], plate="c_ledger", **{"in": "push"}, cam=cam(1.05, 1.14, 540, 820),
     counters=[dict(RED, **{"from": 0, "to": 104, "prefix": "-$", "suffix": "B", "label": "ขาดทุน 9 เดือนแรกของปี 2026", "x": 540, "y": 700, "at": T("ขาดทุนแสนล้าน") + 0.1, "dur": 0.9, "size": 230, "d3": True, "side": "#7A1E08"})])
# ---- title (voice gap, music stab): paper card, not a plain blue card (REF_SPEC 37)
shot(GAP["at"], T("ย้อนไปปี2021"), **{"in": "flash"}, card={"style": "paper", "plate": "c_facade", "lines": ["จากคนลาออก", "สู่ IPO ใหญ่ที่สุดในโลก"], "hot": 1, "size": 84, "type": 0.6})
# ---- why they left
shot(T("ย้อนไปปี2021"), T("Dario"), rewind={"from": 2026, "to": 2021, "plate": "c_lab21"})   # v7: over the dark blurred 2021 lab, not a flat blue card (REF_SPEC 37, 67)
shot(T("Dario"), T("ชวนน้องสาว"), plate="c_lab21", **{"in": "push"}, cam=cam(1.1, 1.16, 540, 1000),
     actors=[A("dario", 540, 1280, 1.6, "point", "neutral")],
     photos=[{"img": PH["dario"], "at": T("Dario") + 0.05, "x": 540, "y": 920, "w": 760, "h": 560, "rot": 0.03, "focus": [0.78, 0.38], "label": "Dario Amodei", "credit": CR["dario"]},
])
shot(T("ชวนน้องสาว"), T("เพราะรู้สึกว่า"), plate="c_leaving", cam=cam(1.0, 1.06, 540, 1000),
     actors=[A("dario", 300, pose="wave", face="smile", keys=[{"t": T("ลาออกยกแก๊ง"), "x": 1300, "walk": True}]),
             A("daniela", 480, face="smile", keys=[{"t": T("ลาออกยกแก๊ง") + 0.15, "x": 1300, "walk": True}]),
             A("staff", 640, keys=[{"t": T("กับเพื่อน") + 0.0, "face": "smile"}, {"t": T("ลาออกยกแก๊ง") + 0.3, "x": 1350, "walk": True}]),
             A("analyst", 800, dir=-1, keys=[{"t": T("ลาออกยกแก๊ง") + 0.45, "x": 1400, "walk": True}])],
     counters=[dict(NUM, **{"from": 1, "to": 7, "suffix": " คน", "x": 540, "y": 520, "at": T("ลาออกยกแก๊ง"), "dur": 0.7, "size": 170})])
shot(T("เพราะรู้สึกว่า"), T("เลยออกมาทำเอง"), plate="c_caution", **{"in": "push"}, cam=cam(1.15, 1.22, 540, 1050),
     actors=[A("dario", 540, 1300, 1.6, "think", "worried")])
shot(T("เลยออกมาทำเอง"), T("ต้นปี2023"), plate="c_startup", **{"in": "push"}, cam=cam(1.02, 1.08, 540, 1000),
     actors=[A("dario", 330, pose="cheer", face="grin"), A("daniela", 520, pose="wave", face="grin"), A("staff", 700, face="smile", dir=-1)],
     photos=[{"img": PH["antlogo"], "at": T("ชื่อAnthropic") + 0.1, "x": 540, "y": 1000, "w": 700, "h": 79, "rot": 0, "focus": [0.5, 0.5]}])
# ---- Claude + the money
shot(T("ต้นปี2023"), T("เขาก็ปล่อยClaude"), plate="c_launch", **{"in": "push"}, cam=cam(1.02, 1.08, 540, 1000),
     actors=[A("staff", 760, 1300, 1.4, "think", dir=-1)],
     photos=[{"img": PH["claude23"], "at": T("ต้นปี2023") + 0.2, "x": 540, "y": 920, "w": 760, "h": 560, "rot": -0.03, "focus": [0.5, 0.3], "credit": CR["anthropic"]}])
shot(T("เขาก็ปล่อยClaude"), T("แล้วเงินก็ไหลมา"), plate="c_launch", cam=cam(1.08, 1.14, 540, 980),
     actors=[A("dario", 380, pose="point", face="grin"), A("daniela", 700, pose="cheer", face="grin", dir=-1)],
     photos=[{"img": LOGO["claude"], "at": T("เขาก็ปล่อยClaude") + 0.5, "x": 540, "y": 900, "w": 260, "h": 260, "rot": 0, "focus": [0.5, 0.5]}])   # v6: square logo at its own proportions (was 420x140 = squashed; user "โลโก้ไม่บีบแบบนั้น")
shot(T("แล้วเงินก็ไหลมา"), T("ปีที่แล้วบริษัท"), plate="c_deals", **{"in": "push"}, cam=cam(1.02, 1.08, 540, 1050),
     actors=[A("investor", 300, pose="point", face="grin"), A("dario", 760, face="smile", dir=-1)],
     props=[{"kind": "cash", "x": 540, "y": 1080, "s": 1.6, "r": 0.1, "front": True}])
shot(T("ปีที่แล้วบริษัท"), T("แค่8เดือนต่อมา"), plate="c_skyline", cam=cam(1.08, 1.12, 540, 1000),
     counters=[dict(NUM, **{"from": 0, "to": 183, "prefix": "$", "suffix": "B", "label": "มูลค่าบริษัท · ก.ย. 2025", "x": 540, "y": 700, "at": T("เกือบ2แสนล้าน"), "dur": 0.9, "size": 190})])
shot(T("แค่8เดือนต่อมา"), T("ปีนี้แค่9เดือน"), plate="c_skyline", **{"in": "zoom"}, cam=cam(1.12, 1.3, 540, 700),
     counters=[dict(NUM, **{"from": 183, "to": 965, "prefix": "$", "suffix": "B", "label": "มูลค่าบริษัท · พ.ค. 2026", "x": 540, "y": 700, "at": T("ขึ้นไปเกือบล้านล้าน") - 0.2, "dur": 1.0, "size": 230, "d3": True})])
shot(T("ปีนี้แค่9เดือน"), T("แล้วก็มาถึงวันที่19"), plate="c_deals", **{"in": "push"}, cam=cam(1.02, 1.1, 540, 900),
     counters=[dict(NUM, **{"from": 0, "to": 33.2, "dec": 1, "prefix": "$", "suffix": "B", "label": "รายได้ 9 เดือนแรกของปี 2026", "x": 540, "y": 700, "at": T("สามหมื่นกว่าล้าน"), "dur": 0.9, "size": 190})])
# v5 (user 2026-11-24 "0:14 อย่าโยงเส้นมักง่าย"): the Daniela name tag + leader line over her face is removed; the caption already says her name
# ---- IPO day (the price pill lives only in this part). v3 (director pass 2026-11-23): the price-up beats sit on the rising-board
# set (exchange), the falling-board set (trade) only once the price slides; captions get a cream halo over the boards
shot(T("แล้วก็มาถึงวันที่19"), T("ตอนแรกตั้งราคา"), plate="c_facade", **{"in": "push"}, cam=cam(1.0, 1.08, 760, 900),
     photos=[{"img": PH["nasdaq"], "at": T("แล้วก็มาถึงวันที่19") + 0.1, "x": 540, "y": 920, "w": 820, "h": 620, "rot": 0.02, "focus": [0.5, 0.45], "label": "Nasdaq MarketSite, New York", "credit": CR["nasdaq"]}])
shot(T("ตอนแรกตั้งราคา"), T("เปิดตลาดปุ๊บ"), plate="c_tradeup", cam=cam(1.08, 1.14, 540, 1000),
     props=[{"kind": "crowd", "cols": 10, "rows": 5, "x": 270, "y": 1010, "dx": 60, "dy": 62, "keep": 50, "cut": 999, "front": True, "at": T("แต่คนแย่งกันซื้อ")}],
     # v6 (user "หุ้นละแปดสิบสาม อะไร ไม่เห็นบอก แปดสิบสามรูปีหรอ"): the unit on screen when the price is said
     counters=[dict(NUM, **{"from": 0, "to": 83, "prefix": "$", "label": "ราคาขายจริงต่อหุ้น", "x": 540, "y": 640, "at": T("สุดท้ายขายจริง") + 0.5, "dur": 0.6, "size": 200})])
shot(T("เปิดตลาดปุ๊บ"), T("ใครซื้อตอนIPO"), plate="c_tradeup", **{"in": "zoom"}, cam=cam(1.1, 1.3, 640, 640),
     photos=[{"img": PH["fox"], "at": T("เปิดตลาดปุ๊บ") + 0.3, "x": 540, "y": 900, "w": 880, "h": 720, "rot": -0.02, "focus": [0.5, 0.35], "credit": CR["fox"], "backdrop": True}])
shot(T("ใครซื้อตอนIPO"), T("เงินที่ระดมได้"), plate="c_tradeup", cam=cam(1.15, 1.2, 540, 900),
     actors=[A("investor", 540, 1190, 1.6, "cheer", "grin")],
     counters=[dict(NUM, **{"from": 0, "to": 34, "prefix": "+", "suffix": "%", "x": 540, "y": 520, "at": T("กำไร34%"), "dur": 0.7, "size": 220})])
shot(T("เงินที่ระดมได้"), T("แต่เดี๋ยวก่อนนะ"), plate="c_tradeup", **{"in": "push"}, cam=cam(1.02, 1.08, 540, 900),
     photos=[{"img": PH["aj"], "at": T("เงินที่ระดมได้") + 0.1, "until": T("ราว81,000ล้าน") + 0.2, "x": 540, "y": 920, "w": 880, "h": 580, "rot": 0.02, "focus": [0.5, 0.2], "credit": CR["aj"]}],
     counters=[dict(NUM, **{"from": 0, "to": 81, "prefix": "$", "suffix": "B", "label": "IPO ของ Anthropic", "x": 540, "y": 880, "at": T("ราว81,000ล้าน") + 0.25, "dur": 0.9, "size": 240, "d3": True}),
               dict(RED, **{"from": 0, "to": 75, "prefix": "$", "suffix": "B", "label": "SpaceX · มิ.ย. 2026", "x": 540, "y": 1260, "at": T("ล้มSpaceX"), "dur": 0.6, "size": 120})])
# ---- the other side
shot(T("แต่เดี๋ยวก่อนนะ"), T("แล้วแสนล้านที่ขาดทุน"), plate="c_tradedown", **{"in": "push"}, cam=cam(1.02, 1.1, 540, 900),
     actors=[A("investor", 540, 1190, 1.6, "head", "worried", keys=[{"t": T("แต่เดี๋ยวก่อนนะ"), "face": "neutral"}, {"t": T("ทั้งวันราคา") + 0.4, "face": "worried"}])])
shot(T("แล้วแสนล้านที่ขาดทุน"), T("แต่ก็ยังมีบิล"), plate="c_ledger", **{"in": "push"}, cam=cam(1.05, 1.12, 540, 850),
     counters=[dict(RED, **{"from": 0, "to": 104, "prefix": "-$", "suffix": "B", "label": "ส่วนใหญ่เป็นตัวเลขทางบัญชี", "x": 540, "y": 700, "at": T("แล้วแสนล้านที่ขาดทุน") + 0.2, "dur": 0.7, "size": 190})])
shot(T("แต่ก็ยังมีบิล"), T("เอาง่ายๆ"), plate="c_build", **{"in": "zoom"}, cam=cam(1.12, 1.25, 540, 760),
     counters=[dict(RED, **{"from": 0, "to": 900, "prefix": "$", "suffix": "B", "label": "สัญญาที่ต้องจ่าย", "x": 540, "y": 700, "at": T("เก้าแสนล้าน"), "dur": 0.9, "size": 190})])
# ---- the reading (our conclusion), paper card at the payoff
shot(T("เอาง่ายๆ"), T("ถ้าโตทัน"), plate="c_bubble", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1000),
     actors=[A("investor", 360, pose="think"), A("dario", 720, face="smile", dir=-1)])
shot(T("ถ้าโตทัน"), T("คิดว่าโตทันไหม"), card={"style": "paper", "plate": "c_bubble", "lines": ["โตทัน = ราคานี้ยังถูก", "ไม่ทัน = ฟองสบู่ลูกใหญ่ที่สุด"], "hot": 1, "size": 74, "type": 2.2})
shot(T("คิดว่าโตทันไหม"), END, noLogo=True, cta={"button": "กดติดตาม", "actors": [
    A("daniela", 250, 1560, 1.4, "wave", "grin"), A("dario", 540, 1600, 1.55, "wave", "smile"), A("investor", 830, 1560, 1.4, "wave", "grin", dir=-1)]})

for x in S: x["noLogo"] = True
for a, b in zip(S, S[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6 and a["t1"] > a["t0"], (a, b["t0"])
quiet = [(x["t0"], x["t1"]) for x in S if x.get("card") or x.get("cta") or x.get("rewind")]
caps = [c for c in caps if not any(c["start"] >= q0 - 0.05 and c["start"] < q1 for q0, q1 in quiet)]
for c in caps:
    for q0, q1 in quiet:
        if c["start"] < q0 < c["end"]: c["end"] = q0 - 0.02
pill = {"from": T("ตอนแรกตั้งราคา"), "to": T("แล้วแสนล้านที่ขาดทุน") - 0.05, "label": "ราคาหุ้น ANT", "y": 440, "values": [
    {"t": T("ตอนแรกตั้งราคา"), "text": "$70–78"}, {"t": T("สุดท้ายขายจริง") + 0.6, "text": "$83"},
    {"t": T("ราคาพุ่งไป111") + 0.5, "text": "$111.50", "hot": False}, {"t": T("ทั้งวันราคาค่อยๆ"), "text": "$111.50 → ?", "hot": True},
    {"t": T("ปิดที่97") + 0.3, "text": "ปิด $97.17", "hot": True}]}
D = {"jobBase": here.resolve().as_uri(), "brandBase": (here.parents[2] / "brand").resolve().as_uri(),
     "plates": P, "captions": caps, "capY": 1470, "captionStyle": {"mode": "soft", "size": 54}, "toonGrade": "brightness(.84) saturate(.75) sepia(.2)", "ctaDark": "c_facade", "duration": END, "pill": [], "focus": True, "handle": None,
     # v4 (user 2026-11-24): captions low like EP01 (y 1470, above the platform buttons), no date chip, no @dataechooo handle
     "look": "paper", "dateY": 110, "dateCenter": True, "dates": [], "dates_v3": [
        {"t": 0, "text": "19 พ.ย. 2026"}, {"t": T("ย้อนไปปี2021"), "text": "2021"}, {"t": T("ต้นปี2023"), "text": "มี.ค. 2023"},
        {"t": T("ปีที่แล้วบริษัท"), "text": "ก.ย. 2025"}, {"t": T("แค่8เดือนต่อมา"), "text": "พ.ค. 2026"}, {"t": T("ปีนี้แค่9เดือน"), "text": "ม.ค.–ก.ย. 2026"},
        {"t": T("แล้วก็มาถึงวันที่19"), "text": "19 พ.ย. 2026"}],
     "music_mute": [[GAP["at"] - 0.05, GAP["at"] + 0.02], [T("ถ้าโตทัน") - 0.1, T("คิดว่าโตทันไหม")]],
     "extra_cues": [{"t": GAP["at"] - 0.35, "sfx": "tapestop", "db": -20}, {"t": T("แต่เดี๋ยวก่อนนะ"), "sfx": "stab", "db": -18},
                    {"t": T("ถ้าโตทัน"), "sfx": "tick", "db": -24, "dur": T("คิดว่าโตทันไหม") - T("ถ้าโตทัน")}],
     "shots": S}
(here / "scene.json").write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "music_mute.txt").write_text(",".join(f"{a:.2f}-{b:.2f}" for a, b in D["music_mute"]), encoding="utf-8")
d = sorted(x["t1"] - x["t0"] for x in S)
print(f"{len(S)} shots, median {d[len(d)//2]:.2f}s, min {d[0]:.2f}s, max {d[-1]:.2f}s, {len(caps)} caption sets, end {END}")
