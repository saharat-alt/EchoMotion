"""เซฟพูด / Google Pomelli v2 -> scene_v2.json for engine/pages/talkinghead4.html.
v2.1 (user 2026-11-23 on v2: "ซับอยู่ต่ำไปหน่อย", "เอาหน้าใหญ่ๆไว้ใต้อินเสิทไม่มีใครเขาทำ"): captions raised to just under the chin (y 1520, was 1760),
insert shots = insert big on top + speaker small in the bottom-right corner (Safe's IG ref "20 video styles").
v2 = owner review 2026-11-23 on v1: "ทุกเฟรมมั่วไปมา", inserts "แคปจอมาแบบแปะโง่ๆ มองไรไม่เห็น", "คลิปเขย่าสั่นรัวๆ แสงวาปไปมา".
Fixes (REF_SPEC 49): static frame (no face-follow, no per-frame push; size changes only on cuts), no person cutout layer
(its edge flickered), no dimming, every insert = the ONE part of the real Pomelli screen being talked about, cropped and shown
big (full-frame cutaway or top half), one thing on screen at a time.
usage: python plan_v2.py"""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parents[2] / "engine"))
from captions import sets_from_script

EDL = json.loads((here / "edl.json").read_text(encoding="utf-8")); DUR = EDL[-1]["t1"]
wtok = [{"text": w["word"].strip(), "start": w["start"], "end": w["end"]}
        for s in json.loads((here / "input/whisper/aroll.json").read_text(encoding="utf-8"))["segments"] for w in s.get("words", [])]
caps = []
for e in EDL:   # per piece: Whisper tokens where it heard the piece, else the script spread over the piece
    chars = e["line"].replace(" / ", "").replace(" ", "")
    inside = [w for w in wtok if e["t0"] - 0.05 <= w["start"] < e["t1"]]
    if sum(len(w["text"]) for w in inside) < 0.6 * len(chars):
        inside = [{"text": ch, "start": e["t0"] + 0.06 + (e["t1"] - e["t0"] - 0.2) * i / len(chars), "end": 0} for i, ch in enumerate(chars)]
        for w in inside: w["end"] = w["start"] + 0.05
    part = sets_from_script(e["line"], inside, keywords=["Pomelli", "Google", "3 วัน", "ฟรี", "AI"], max_chars=34)
    for c in part: c["end"] = min(c["end"], e["t1"])
    caps += part
for a, b in zip(caps, caps[1:]): a["end"] = round(max(a["end"], b["start"] - 0.02) if b["start"] - a["end"] < 0.6 else a["end"], 3)
TXT = ["".join(w["text"] for w in c["words"]).replace(" ", "") for c in caps]
def T(s, off=0.0):
    hits = [c["start"] for c, x in zip(caps, TXT) if s.replace(" ", "") in x]; assert hits, (s, TXT); return round(hits[0] + off, 3)
def P(i): return EDL[i]["t0"]

CR = "ภาพ: Google (blog.google)"
IM = {k: f"assets/web/{v}.png" for k, v in {"landing": "ui_landing", "dna": "z_dna", "colors": "z_colors", "fonts": "z_fonts", "images": "z_images",
                                           "ideas": "z_ideas2", "poster": "z_poster", "edit": "z_edit"}.items()}
IM["logo"] = "../../../brand/logo/DataEchooo-logo.png"
S = []
def seg(t0, t1, layout, **kw): S.append(dict(t0=round(t0, 3), t1=round(t1, 3), layout=layout, **kw))
WORD = dict(y=380, size=230, color="#FFFFFF")    # big word in the free space ABOVE the head (refs 1 and 3), never over the face

seg(0, P(1), "full", zoom=1.0, behind=[dict(WORD, text="Pomelli", latin=True, at=T("คุมโทนแบรนด์ด้วย") + 0.6)])
seg(P(1), P(2), "full", zoom=1.1)                                   # jump cut 100 -> 110 %
seg(P(2), P(3), "full", zoom=1.0)
seg(P(3), P(4), "full", zoom=1.1, behind=[dict(WORD, text="3 วัน", color="#FE4C1C", size=260, at=T("ปวดหัวไป 3 วัน") + 0.55)])
seg(P(4), P(5), "pip", capY=1110, insert={"dy": -230, "img": "landing", "w": 1000, "credit": CR})
seg(P(5), T("ทั้งสีที่ใช่"), "pip", capY=1110, insert={"dy": -230, "img": "dna", "w": 1040, "credit": CR})
mid = round((T("ทั้งสีที่ใช่") + T("และสไตล์ของแบรนด์")) / 2, 3)
seg(T("ทั้งสีที่ใช่"), mid, "pip", capY=1110, insert={"dy": -230, "img": "colors", "w": 1000, "credit": CR})
seg(mid, T("และสไตล์ของแบรนด์"), "pip", capY=1110, insert={"dy": -230, "img": "fonts", "w": 1000, "credit": CR})
seg(T("และสไตล์ของแบรนด์"), T("ไม่ต้องมานั่งเซ็ต"), "pip", capY=1110, insert={"dy": -230, "img": "images", "w": 640, "credit": CR})
seg(T("ไม่ต้องมานั่งเซ็ต"), P(7), "full", zoom=1.1)
seg(P(7), P(8), "pip", capY=1110, insert={"dy": -230, "img": "ideas", "w": 1000, "credit": CR})
seg(P(8), P(9), "pip", capY=1110, insert={"dy": -230, "img": "poster", "w": 700, "credit": CR})
seg(P(9), T("พิมพ์ให้ AI เปลี่ยนฉากหลัง"), "full", zoom=1.12)
seg(T("พิมพ์ให้ AI เปลี่ยนฉากหลัง"), P(10), "pip", capY=1110, insert={"dy": -230, "img": "edit", "w": 1040, "credit": CR})
seg(P(10), P(11), "full", zoom=1.0, behind=[dict(WORD, text="ฟรี", color="#FE4C1C", size=320, at=T("ฟรีอีกด้วยครับ") + 0.45)])
seg(P(11), P(12), "full", zoom=1.1, badges=[{"text": "labs.google/pomelli", "at": P(11) + 0.4, "x": 540, "y": 380, "size": 64, "bg": "#1A1B1E", "rot": -0.04}])
seg(P(12), DUR, "full", zoom=1.0, logos=[{"img": "logo", "at": P(13), "x": 540, "y": 300, "h": 110}],
    badges=[{"text": "กดติดตาม", "at": T("กดติดตาม") + 0.3, "x": 540, "y": 470, "size": 70, "bg": "#FE4C1C"}])
for a, b in zip(S, S[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6 and b["t0"] > a["t0"], (a, b)

F = json.loads((here / "assets/face.json").read_text())
anchor = {"x": sum(f["cx"] for f in F) / len(F) * 1080, "y": sum(f["cy"] for f in F) / len(F) * 1920, "h": 0}
scene = {"duration": DUR, "jobBase": here.resolve().as_uri(), "brandBase": (here.parents[2] / "brand").resolve().as_uri(),
         "footage": "assets/footage.webm", "cutout": None, "static": True, "capY": 1520, "pip": {"x": 600, "y": 1190, "w": 420, "h": 600}, "anchor": anchor, "images": IM, "segments": S, "captions": caps, "face": F}
(here / "scene_v2.json").write_text(json.dumps(scene, ensure_ascii=False, indent=1), encoding="utf-8")
cues = [{"t": b["t0"], "sfx": "swish_paper" if "pip" in (a["layout"], b["layout"]) else "whoosh", "db": -17, "align": "peak"}
        for a, b in zip(S, S[1:]) if a["layout"] != b["layout"] or a.get("insert") != b.get("insert")]
for s in S:
    for o in s.get("behind", []) + s.get("badges", []) + s.get("logos", []): cues.append({"t": o["at"], "sfx": "pop", "db": -18})
cues.sort(key=lambda c: c["t"]); (here / "cues_v2.json").write_text(json.dumps(cues, indent=1), encoding="utf-8")
print(f"{len(S)} segments, {len(caps)} captions, {len(cues)} cues, {DUR:.1f}s")
