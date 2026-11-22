"""เล่าข่าว / Claude กับโจทย์เลข 167 ปี v1 -> plan_v1.json (pipelines/news/build_shots.py -> scene_v3.json, engine/pages/news3.html).
Voice: Safe, one take, sped up 12 % (input/voice.wav), times from local Whisper (input/segments.json, input/words.json).
Rules applied: REF_SPEC 43 (non-tech), 45 (every insert is a real ref: Al Jazeera / Clay / GitHub pages, Commons photos),
46 (hook), 48 (one focal point at a time, centred), 38 (mascot: viseme mouths + a gesture change every 2-4 s).
The hook keeps the generated line (user 2026-11-23: "เอาตามเดิมไปก่อน"), with an on-screen "ยังรอการยืนยัน" tag.
usage: python plan_v1.py && python ../../../pipelines/news/build_shots.py . plan_v1.json"""
import json, pathlib, re
here = pathlib.Path(__file__).parent
SEG = json.loads((here / "input/segments.json").read_text(encoding="utf-8"))
def S(i): return SEG[i][0]          # start of Whisper segment i (sped-up time)
END = round(SEG[-1][1] + 0.6, 2)

CAP = """โจทย์เลขที่ไม่มีใคร / แก้ได้มา 167 ปี / Claude เพิ่งช่วยแก้ได้ / แต่คำตอบยาวจนคนอ่านไม่ไหว
โจทย์นี้ชื่อ Riemann Hypothesis / เป็นเรื่องรูปแบบของจำนวนเฉพาะ / ที่ดูสุ่ม แต่จริงๆ มีระเบียบซ่อนอยู่
เป็น 1 ใน 7 โจทย์ / ที่มีรางวัลข้อละล้านดอลลาร์
วันที่ 20 พ.ย. / Levent Alpöge / นักคณิตศาสตร์ของ Anthropic / บอกว่าเขาพิสูจน์ได้แล้ว / โดยทำงานกับ Claude
แต่ถ้าเขียนออกมา / เป็นภาษาคน / จะยาวกว่า 250,000 หน้า / เขาเลยปล่อยเป็นโค้ด / ให้คอมพิวเตอร์ตรวจทีละขั้นแทน
วันเดียวกัน เขากับเพื่อน / ยังปล่อยอีกโจทย์ล้านดอลลาร์ / เรื่องสมการการไหลของน้ำ
แล้วคนในวงการว่ายังไง / ลองฟัง 3 ประโยคนี้
หนึ่ง Brian Conrey บอกว่า / ไม่คิดว่าจะมีมนุษย์คนไหนหาเจอ
สอง Kevin Buzzard บอกว่า / เรายังไม่รู้เลยว่ามันจริงเพราะอะไร
สาม Andrew Sutherland / จาก MIT ที่ลองรันโค้ดเอง / บอกว่า / นี่คือชัยชนะของมนุษย์
ตอนนี้ยังไม่ได้ / เงินรางวัลนะ / ต้องรอคนในวงการยอมรับอย่างน้อย 2 ปี
คิดว่าใครควรได้เครดิต AI หรือคน / คอมเมนต์บอกหน่อยครับ"""
(here / "caption_script.txt").write_text(CAP, encoding="utf-8")

X, W = 90, 900        # everything centred in the middle band (REF_SPEC 48); the mascot owns the bottom-right corner
def doc(d, y=420, at=0, hl=0.3, w=W, rot=-1.5): return {"k": "doc", "doc": d, "x": (1080 - w) // 2, "y": y, "w": w, "rot": rot, "at": at, "from": "bottom",
                                                         "highlights": [{"phrase": p, "at": hl} for p in DOCS[d]]}
def photo(img, w=640, y=400, at=0, rot=2): return {"k": "photo", "img": img, "x": (1080 - w) // 2, "y": y, "w": w, "rot": rot, "at": at, "from": "bottom"}
def card(html, y=520, at=0, size=72, bg="#FFF8EC", ink="#111", rot=-2, w=None):
    c = {"k": "card", "html": html, "x": 140, "y": y, "rot": rot, "at": at, "from": "drop", "bg": bg, "ink": ink, "size": size}
    if w: c["w"] = w; c["x"] = (1080 - w) // 2
    return c
def num(v, suf="", pre="", y=520, at=0, size=200, bg="#FFF8EC", ink="#111", dec=0): return {"k": "num", "value": v, "suf": suf, "pre": pre, "x": 150, "y": y, "rot": -2, "at": at, "from": "drop", "size": size, "bg": bg, "ink": ink, "dec": dec}
DOCS = {k: list(v["phrases"]) for k, v in json.loads((here / "assets/docs/docs.json").read_text()).items()}

shots = []
def shot(t0, t1, pieces, src=None, sfx="whoosh", **kw): shots.append(dict(t0=round(t0, 2), t1=round(t1, 2), bg="#FFF8EC", cut_sfx=sfx, pieces=pieces, sheet=False, **({"src": src} if src else {}), **kw))
# hook (<= 4.4 s): the number on frame 0, then the person's own words, tagged as a claim
shot(0, 2.2, [num(167, suf=" ปี", y=560, size=240, bg="#111", ink="#FFF8EC")])
shot(2.2, S(1), [doc("aj_alpoge", y=520), card("ยังรอการยืนยัน", y=860, at=0.4, size=46, bg="#FE4C1C", ink="#FFF8EC", rot=3)], src="Al Jazeera 21 พ.ย. 2026", sfx="shutter")
shot(S(1), S(2), [doc("aj_noread", y=560)], src="Al Jazeera 21 พ.ย. 2026", sfx="shutter")
# what the problem is
shot(S(2), S(3), [doc("aj_1859", y=520)], src="Al Jazeera", sfx="shutter")
shot(S(3), S(4), [card(" ".join(str(p) for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]), y=560, size=64, w=860, rot=-1),
                  card("จำนวนเฉพาะ", y=800, at=1.2, size=52, bg="#214AFF", ink="#FFF8EC", rot=2)])
shot(S(4), S(5), [doc("clay_prize", y=520)], src="Clay Mathematics Institute", sfx="shutter")
# who + what he claims
shot(S(5), S(6), [card("<div style='font:800 54px Kanit;letter-spacing:4px'>NOV</div><div style='font:900 300px/0.9 \"Red Hat Display\"'>20</div><div style='font:700 44px Kanit'>2026</div>",
                       y=440, size=60, bg="#F1E6D2", rot=-3, w=420)])
shot(S(6), S(6) + 2.6, [photo("assets/photos/alpoge.jpg", w=720, y=440), card("Levent Alpöge · Anthropic", y=960, at=0.5, size=46, bg="#111", ink="#FFF8EC", rot=2)],
     src="ภาพ: Marlene Ruf / MFO (CC BY-SA 2.0 de)", sfx="shutter")
shot(S(6) + 2.6, S(7), [doc("aj_alpoge", y=520, hl=0.2)], src="Al Jazeera 21 พ.ย. 2026", sfx="shutter")
# the size of the proof
shot(S(7), S(8), [card("250,000+ หน้า", y=560, size=130, w=900, rot=-2)])
shot(S(8), S(9), [num(17, suf=" ล้านบรรทัด", y=520, size=150, bg="#111", ink="#FFF8EC"), card("โค้ดบทพิสูจน์ที่คอมพิวเตอร์ตรวจ (Kevin Buzzard, Al Jazeera)", y=820, at=0.8, size=34, w=820, rot=1)])
shot(S(9), S(10), [photo("assets/docs/github_ns.png", w=680, y=380, rot=-1)], src="github.com/tristanbuckmaster/navier-stokes", sfx="shutter")
# three voices (the mascot hosts in the centre for the bridge)
shot(S(10), S(11), [card("1 · 2 · 3", y=520, size=120, rot=-2)], sfx="riser")
shot(S(11), S(12), [photo("assets/photos/conrey.jpg", w=420, y=360), card("“I don't think any human was about to find this”", y=860, at=1.4, size=40, w=880, rot=-1)],
     src="AFP via phys.org 20 พ.ย. 2026 · ภาพ: Sandrobt (CC BY-SA 3.0)", sfx="shutter")
shot(S(12), S(13), [doc("aj_buzzard", y=520)], src="Al Jazeera 21 พ.ย. 2026", sfx="shutter")
shot(S(13), S(14), [card("“to me this is a human triumph, and a day for celebration”", y=520, size=58, w=880, rot=-2), card("Andrew Sutherland · MIT", y=900, at=0.8, size=44, bg="#111", ink="#FFF8EC", rot=2)],
     src="Scientific American 20 พ.ย. 2026", sfx="whoosh")
# where it stands + CTA
shot(S(14), S(15), [num(2, suf=" ปี", pre="≥ ", y=560, size=220), card("Clay: ยังขึ้นว่า Unsolved", y=900, at=1.6, size=42, rot=2)], src="claymath.org")
shot(S(15), END, [card("AI <span style='color:#FE4C1C'>หรือ</span> คน?", y=480, size=120, rot=-3)], sfx="chime")

# ---- mascot: gesture every 2-4 s on the word, centre host on the bridge and the CTA
POSES = [(0, "wow"), (S(1), "shrug"), (S(2), "point_up"), (S(3), "explain"), (S(4), "point_side"), (S(5), "ok"), (S(6), "point_side"), (S(6) + 2.6, "hold_card"),
         (S(7), "wow"), (S(8), "phone"), (S(9), "point_side"), (S(10), "explain"), (S(11), "count_1"), (S(12), "count_2"), (S(13), "count_3"),
         (S(14), "chin"), (S(15), "arms_crossed"), (S(16), "bye")]
moves = [{"t": S(10) - 0.2, "x": 540, "y": 2050, "scale": 0.86}, {"t": S(11) - 0.1, "x": 830, "y": 2010, "scale": 0.56},
         {"t": S(15) - 0.2, "x": 540, "y": 2050, "scale": 0.86}]

# ---- visemes from the timed Thai text: each Whisper token's characters spread over its time, vowel/consonant -> mouth shape
V_OF = {}
for ch in "าะัำ": V_OF[ch] = "a"
for ch in "ีิเแึื": V_OF[ch] = "e"
for ch in "โอ": V_OF[ch] = "o"
for ch in "ูุว": V_OF[ch] = "u"
for ch in "มบปพผภ": V_OF[ch] = "mbp"
for ch in "ฟฝ": V_OF[ch] = "fv"
words = json.loads((here / "input/words.json").read_text(encoding="utf-8"))
vis, last = [], None
for w in words:
    chars = [c for c in w["text"] if not c.isspace()]
    if not chars: continue
    step = max(0.02, (w["end"] - w["start"]) / len(chars))
    for i, c in enumerate(chars):
        v = V_OF.get(c, "small" if re.match(r"[ก-ฮA-Za-z0-9]", c) else None)
        if v is None or v == last: continue
        vis.append({"t": round(w["start"] + i * step, 3), "v": v}); last = v
    vis.append({"t": round(w["end"], 3), "v": "rest"}); last = "rest"
vis = sorted(vis, key=lambda q: q["t"])
# rest only where the voice really pauses (> 0.12 s), so the mouth does not snap shut between syllables
clean = []
for i, q in enumerate(vis):
    if q["v"] == "rest" and i + 1 < len(vis) and vis[i + 1]["t"] - q["t"] < 0.12: continue
    clean.append(q)

plan = {"page": "engine/pages/news3.html", "caption_script": "@caption_script.txt",
        "keywords": ["167", "Claude", "Riemann", "Anthropic", "250,000", "MIT", "2 ปี", "AI"], "fixes": {"Echo": "Echooo"},
        "flashes": [], "grid": {"tints": [{"t": 0, "bg": None, "line": "rgba(33,74,255,.06)", "major": None, "w": 1}]},
        "desks": [], "shots": shots,
        "mascot": {"poses": [{"t": round(t, 2), "pose": p} for t, p in POSES], "emotes": [{"t": 0.3, "type": "hop"}, {"t": S(7) + 0.2, "type": "hop"}],
                   "moves": moves, "visemes": clean}}
plates = [("m01_hook", 0, S(2)), ("m02_primes", S(2), S(4)), ("m03_prize", S(4), S(5)), ("m04_person", S(5), S(7)), ("m05_pages", S(7), S(9)),
          ("m06_water", S(9), S(10)), ("m07_quotes", S(10), S(14)), ("m08_wait", S(14), END)]
for img, a, b in plates:
    plan["desks"].append({"img": f"assets/plates/{img}.png", "t0": round(a, 2), "t1": round(b, 2) if b != END else 1e9,
                          "keys": [{"t": a, "x": 0, "y": 0, "s": 1.06}, {"t": b, "x": 0, "y": 0, "s": 1.12}]})
(here / "plan_v1.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(shots)} shots, {len(clean)} viseme keys, {len(POSES)} gestures, end {END}")
