"""เซฟพูด / Google Pomelli v1 -> scene_v1.json for engine/pages/talkinghead4.html.
Inputs: edl.json (cut_aroll.py), input/whisper/aroll.json (local Whisper medium on the A-roll, char-level Thai tokens),
assets/face.json, assets/footage.webm, assets/cutout.webm (engine/tools/person_matte.py).
Inserts are Google's own Pomelli screens from blog.google (credited, fair use) — real content on the word (REF_SPEC rule 3).
Layout grammar from Safe's IG refs (docs/FEEDBACK_2026-11-22.md): big word behind the speaker, floating torn-paper cards
above the head, running checklist that ticks on the word, torn-paper split seam, full-frame screen over a blurred copy.
usage: python plan_v1.py
"""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parents[2] / "engine"))
from captions import sets_from_script

EDL = json.loads((here / "edl.json").read_text(encoding="utf-8"))
DUR = EDL[-1]["t1"]
# timing per EDL piece: Whisper tokens where Whisper heard the piece (it drops some stretches of Thai), else the piece's
# script spread evenly over its speech; then each piece's caption sets are aligned inside that piece only
wtok = []
wj = here / "input/whisper/aroll.json"
if wj.exists():
    for s in json.loads(wj.read_text(encoding="utf-8"))["segments"]:
        for w in s.get("words", []):
            wtok.append({"text": w["word"].strip(), "start": w["start"], "end": w["end"]})
caps = []
KW = ["Pomelli", "Google", "3 วัน", "ฟรี", "website", "AI"]
for e in EDL:
    chars = e["line"].replace(" / ", "").replace(" ", "")
    inside = [w for w in wtok if e["t0"] - 0.05 <= w["start"] < e["t1"]]
    if sum(len(w["text"]) for w in inside) < 0.6 * len(chars):
        inside = []
        for i, ch in enumerate(chars):
            a = e["t0"] + 0.06 + (e["t1"] - e["t0"] - 0.2) * i / len(chars)
            inside.append({"text": ch, "start": a, "end": a + 0.05})
    part = sets_from_script(e["line"], inside, keywords=KW, max_chars=34)
    for c in part: c["end"] = min(c["end"], e["t1"])
    caps += part
for a, b in zip(caps, caps[1:]): a["end"] = round(max(a["end"], b["start"] - 0.02) if b["start"] - a["end"] < 0.6 else a["end"], 3)
TXT = ["".join(w["text"] for w in c["words"]).replace(" ", "") for c in caps]
def T(s, n=1, off=0.0):  # start of the n-th caption set containing s
    hits = [c["start"] for c, x in zip(caps, TXT) if s.replace(" ", "") in x]
    assert len(hits) >= n, (s, n, TXT); return round(hits[n - 1] + off, 3)
def P(i): return EDL[i]["t0"]  # start of EDL piece i

CR = "ภาพ: Google (blog.google)"
IM = {"landing": "assets/web/ui_landing.png", "dna": "assets/web/ui_dna.png", "ideas": "assets/web/ui_ideas.png", "edit": "assets/web/ui_edit.png",
      "logo": "../../../brand/logo/DataEchooo-logo.png"}
FEAT = {"title": "Pomelli ทำอะไรได้", "x": 70, "y": 110, "items": []}   # filled below with times
S = []
def seg(t0, t1, layout, **kw): S.append(dict(t0=round(t0, 3), t1=round(t1, 3), layout=layout, **kw))

# 1 hook: speaker + "Pomelli" BEHIND him, the real Pomelli page floats above the head on "AI ตัวใหม่จาก Google"
seg(0, P(1), "float", zoom=1.0,
    behind=[{"text": "Pomelli", "latin": True, "at": T("คุมโทนแบรนด์ด้วย") + 0.6, "until": T("AI ตัวใหม่จาก Google"), "y": 560, "size": 240, "color": "#FFFFFF"}],
    cards=[{"img": "landing", "at": T("AI ตัวใหม่จาก Google"), "x": 540, "y": 300, "w": 470, "rot": -0.05, "credit": CR, "seed": 11}])
# 2 share line: jump-cut punch-in (type 1 rule: 100% <-> 108%)
seg(P(1), P(2), "full", zoom=1.1)
# 3 the pain: big "3 วัน" behind the speaker on the number
seg(P(2), P(3), "full", zoom=1.0, dim=True)
seg(P(3), P(4), "full", zoom=1.12, dim=True, behind=[{"text": "3 วัน", "at": T("ปวดหัวไป 3 วัน") + 0.55, "y": 470, "size": 300, "color": "#FE4C1C"}])
# 4 the turn: the real Pomelli page on top, torn-paper seam
seg(P(4), P(5), "split", insert={"img": "landing", "w": 760, "credit": CR})
# 5 Business DNA: full-frame screen, rings on the colours / fonts / images as he names them
seg(P(5), T("ไม่ต้องมานั่งเซ็ต"), "cut", insert={"img": "dna", "w": 1060, "credit": CR, "rings": [
    {"x": 580, "y": 636, "r": 180, "at": T("ทั้งสีที่ใช่") + 0.1}, {"x": 650, "y": 488, "r": 120, "at": T("ทั้งสีที่ใช่") + 1.0},
    {"x": 942, "y": 560, "r": 170, "at": T("และสไตล์ของแบรนด์") + 0.2}]})
seg(T("ไม่ต้องมานั่งเซ็ต"), P(7), "float", zoom=1.06,
    list={**FEAT, "at": T("ไม่ต้องมานั่งเซ็ต"), "items": [{"text": "ดึงตัวตนแบรนด์จากเว็บ", "at": T("ไม่ต้องมานั่งเซ็ต") + 0.1}]})
# 6 campaign ideas: the real "suggestions" screen on top
seg(P(7), P(8), "split", insert={"img": "ideas", "w": 1000, "credit": CR})
# 7 content: list ticks item 2-3, the content screen floats above the head
seg(P(8), P(9), "float", zoom=1.04,
    cards=[{"img": "edit", "at": P(8) + 0.1, "x": 700, "y": 330, "w": 520, "rot": 0.05, "credit": CR, "seed": 23}],
    list={**FEAT, "at": P(8), "y": 90, "items": [{"text": "ดึงตัวตนแบรนด์จากเว็บ", "at": P(8)}, {"text": "คิดไอเดียแคมเปญ", "at": P(8)},
                                               {"text": "เสนอคอนเทนต์", "at": P(8) + 0.4}]})
# 8 "ที่เด็ดที่สุด": punch-in on the face, then the edit screen with a ring on the product image
seg(P(9), T("พิมพ์ให้ AI เปลี่ยนฉากหลัง"), "full", zoom=1.15)
seg(T("พิมพ์ให้ AI เปลี่ยนฉากหลัง"), P(10), "split", insert={"img": "edit", "w": 1000, "credit": CR, "rings": [
    {"x": 300, "y": 470, "r": 230, "at": T("พิมพ์ให้ AI เปลี่ยนฉากหลัง") + 0.4}, {"x": 1120, "y": 140, "r": 90, "at": T("หรือเพิ่มลูกเล่น") + 0.3}]})
# 9 Thai + free: "ฟรี" big behind the speaker on the word
seg(P(10), P(11), "float", zoom=1.0,
    behind=[{"text": "ฟรี", "at": T("ฟรีอีกด้วยครับ") + 0.45, "y": 450, "size": 360, "color": "#FE4C1C"}],
    badges=[{"text": "ใช้ได้ในไทยแล้ว", "at": T("ตอนนี้เปิดให้คนไทย") + 0.5, "x": 540, "y": 250, "size": 64, "bg": "#214AFF", "until": T("ฟรีอีกด้วยครับ") + 0.3}])
# 10 where to get it: the address as a sticker (adds what the voice does not say)
seg(P(11), P(12), "float", zoom=1.06,
    badges=[{"text": "labs.google/pomelli", "at": P(11) + 0.4, "x": 540, "y": 300, "size": 64, "bg": "#1A1B1E", "rot": -0.05}])
# 11 CTA
seg(P(12), DUR, "full", zoom=1.08,
    logos=[{"img": "logo", "at": P(13), "x": 540, "y": 300, "h": 110}],
    badges=[{"text": "กดติดตาม", "at": T("กดติดตาม") + 0.3, "x": 540, "y": 470, "size": 70, "bg": "#FE4C1C"}])

for a, b in zip(S, S[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6 and b["t0"] > a["t0"], (a, b)
scene = {"duration": DUR, "jobBase": here.resolve().as_uri(), "brandBase": (here.parents[2] / "brand").resolve().as_uri(),
         "footage": "assets/footage.webm", "cutout": "assets/cutout.webm", "images": IM, "segments": S, "captions": caps,
         "face": json.loads((here / "assets/face.json").read_text())}
(here / "scene_v1.json").write_text(json.dumps(scene, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(S)} segments, {len(caps)} captions, {DUR:.1f}s: " + ", ".join(f"{s['layout']}:{s['t1'] - s['t0']:.1f}" for s in S))

# ---- SFX cues: every sound sits on a visual event (REF_SPEC 8/19), light and under the voice
cues = []
for a, b in zip(S, S[1:]):
    if a["layout"] != b["layout"]: cues.append({"t": b["t0"], "sfx": "swish_paper" if "split" in (a["layout"], b["layout"]) else "whoosh", "db": -16, "align": "peak"})
for s in S:
    for c in s.get("cards", []): cues.append({"t": c["at"], "sfx": "paper", "db": -18})
    for o in s.get("behind", []): cues.append({"t": o["at"], "sfx": "pop", "db": -17})
    for o in s.get("badges", []) + s.get("logos", []): cues.append({"t": o["at"], "sfx": "pop_2", "db": -18})
    for r in (s.get("insert") or {}).get("rings", []): cues.append({"t": r["at"], "sfx": "pen", "db": -20})
    if s.get("list"):
        for it in s["list"]["items"]:
            if it["at"] >= s["t0"]: cues.append({"t": it["at"], "sfx": "click", "db": -20})
cues.sort(key=lambda c: c["t"])
(here / "cues_v1.json").write_text(json.dumps(cues, indent=1), encoding="utf-8")
print(f"{len(cues)} cues ({len(cues) / DUR * 60:.0f}/min)")
