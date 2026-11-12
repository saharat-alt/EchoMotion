"""Type 3 / Jensen Huang affair -> business impact, v2: caption_script_v2.txt + input/words.json -> scene.json for engine/pages/story2d.html.
Voice: Safe, one take (voice_el/full_v2.mp3 -> prep_voice_v2.py -> input/voice.wav + input/words.json, 1.6 s gap for the title card).
Grammar from the NVIDIA baseline (part1_scene_v3.py): one spoken phrase = one cut, counters on every number, photos as proof
on key beats (REF_SPEC 29), push on place changes, cards for the quote / the verdict, cast drawn in code.
usage: python scene_v2.py   (writes scene.json + music_mute.txt)"""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parents[2] / "engine"))
from captions import sets_from_script

words = json.loads((here / "input/words.json").read_text(encoding="utf-8"))
caps = sets_from_script((here / "caption_script_v2.txt").read_text(encoding="utf-8"), words,
                        ["NVIDIA", "Jensen", "4.5", "15", "33", "219", "2018", "2019", "FBI", "Intel", "McDonald's", "Bernstein"])
ALL = list(caps); TXT = ["".join(w["text"] for w in c["words"]) for c in ALL]
GAP = json.loads((here / "input/title_gap.json").read_text())
END = round(caps[-1]["end"] + 2.4, 2)

def T(s, n=1):  # start of the n-th caption set containing s
    hits = [c["start"] for c, x in zip(ALL, TXT) if s.replace(" ", "") in x]
    assert len(hits) >= n, (s, n); return hits[n - 1]

P = {k: f"assets/plates/{v}.png" for k, v in {
    "board": "j01_boardroom", "hearing": "j02_hearing", "news": "j03_newsstand", "trade": "j04_trading", "lab": "j05_research",
    "office": "b03_office", "city": "b04_city", "stage": "b05_stage", "meeting": "b07_meeting", "floor": "b08_floor", "desk": "b10_desk_top"}.items()}

def cam(z0, z1, x0=540, y0=960, x1=None, y1=None):
    return {"z": [z0, z1], "x": [x0, x1 if x1 is not None else x0], "y": [y0, y1 if y1 is not None else y0]}
S = []
def shot(t0, t1, **kw): S.append(dict(t0=round(t0, 3), t1=round(t1, 3), **kw))
def J(**k): return dict({"who": "jensen26", "x": 540, "y": 1180, "scale": 1.6, "pose": "idle", "face": "neutral"}, **k)
NUMC = dict(color="#214AFF", glow="rgba(255,255,255,.95)")
RED = dict(color="#FE4C1C", glow="rgba(255,255,255,.95)")
PH = {"jensen": "assets/photos/jensen_portrait.jpg", "jensen2": "assets/photos/jensen_portrait2.jpg", "hq": "assets/photos/nvidia_hq.jpg",
      "capitol": "assets/photos/us_capitol.jpg", "intel": "assets/logos/intel.png", "mcd": "assets/logos/mcdonalds.png",
      "nyt": "assets/logos/nyt.png", "nvlogo": "assets/logos/nvidia.png"}
CR = {"jensen": "ภาพ: Anderseidesvik / Wikimedia Commons (CC BY-SA 4.0)", "hq": "ภาพ: Coolcaesar / Wikimedia Commons (CC BY-SA 4.0)",
      "capitol": "ภาพ: Noclip / Wikimedia Commons (public domain)", "logo": "โลโก้: Wikimedia Commons"}
BOARD = [{"who": "board1", "x": 250, "y": 1250, "scale": 1.25, "pose": "idle", "face": "worried"},
         {"who": "board2", "x": 830, "y": 1250, "scale": 1.25, "pose": "think", "face": "neutral", "dir": -1},
         {"who": "board3", "x": 540, "y": 1300, "scale": 1.3, "pose": "idle", "face": "worried"}]

# ---- hook: real face first (frame 0 moving, voice from 0.27 s)
shot(0, T("ถึงสองคน"), plate="stage", cam=cam(1.1, 1.16, 540, 900),
     photos=[{"img": PH["jensen"], "at": 0.0, "x": 540, "y": 860, "w": 660, "h": 820, "focus": [0.5, 0.36], "rot": -0.02, "credit": CR["jensen"]}])
shot(T("ถึงสองคน"), T("และหลังข่าวนี้"), plate="news", **{"in": "push"}, cam=cam(1.05, 1.12, 540, 900),
     counters=[dict(RED, **{"from": 0, "to": 2, "suffix": " คน", "x": 540, "y": 640, "at": T("ถึงสองคน") + 0.25, "dur": 0.5, "size": 220})])
shot(T("และหลังข่าวนี้"), T("4.5แสนล้าน"), plate="trade", **{"in": "push"}, cam=cam(1.0, 1.12, 540, 760))
shot(T("4.5แสนล้าน"), T("เขาคือ"), plate="trade", cam=cam(1.12, 1.2, 540, 760),
     counters=[dict(RED, **{"from": 0, "to": 450, "prefix": "-$", "suffix": "B", "x": 540, "y": 980, "at": T("4.5แสนล้าน") + 0.1, "dur": 1.1, "size": 210,
                            "until": T("หรือราว15")}),
               dict(RED, **{"from": 0, "to": 15, "prefix": "฿", "suffix": " ล้านล้าน", "x": 540, "y": 980, "at": T("หรือราว15") + 0.15, "dur": 0.9, "size": 150})])
# ---- who
shot(T("เขาคือ"), T("ซีอีโอNVIDIA"), plate="stage", **{"in": "push"}, cam=cam(1.1, 1.16, 540, 940),
     actors=[J(x=230, y=1250, scale=1.45, pose="wave", face="smile")],
     photos=[{"img": PH["jensen2"], "at": T("เขาคือ") + 0.3, "x": 760, "y": 760, "w": 440, "h": 560, "focus": [0.48, 0.35], "label": "Jensen Huang", "credit": CR["jensen"]}])
shot(T("ซีอีโอNVIDIA"), T("ที่เพิ่งเขียน"), plate="city", cam=cam(1.12, 1.18, 540, 900),
     photos=[{"img": PH["hq"], "at": T("ซีอีโอNVIDIA") + 0.05, "x": 540, "y": 820, "w": 820, "h": 500, "focus": [0.5, 0.5], "label": "สำนักงานใหญ่ NVIDIA", "credit": CR["hq"]}])
shot(T("ที่เพิ่งเขียน"), T("บอกพนักงาน"), plate="desk", cam=cam(1.0, 1.08),
     props=[{"kind": "contract", "x": 540, "y": 900, "s": 1.8, "front": True}])
shot(T("บอกพนักงาน"), T("ผมนอกใจ"), plate="floor", **{"in": "push"}, cam=cam(1.02, 1.08, 540, 980),
     props=[{"kind": "crowd", "cols": 8, "rows": 6, "x": 330, "y": 760, "dx": 60, "dy": 70, "keep": 48, "cut": 999, "front": True}])
shot(T("ผมนอกใจ"), T("หลายคนอาจ"), card={"lines": ["“ผมนอกใจภรรยา”", "Jensen Huang · 8 พ.ย. 2026"], "hot": 0, "size": 80,
                                       "type": T("หลายคนอาจ") - T("ผมนอกใจ") - 0.2})
shot(T("หลายคนอาจ"), T("มันก็เรื่องส่วนตัว"), plate="office", **{"in": "push"}, cam=cam(1.12, 1.18, 540, 1000),
     actors=[{"who": "worker", "x": 540, "y": 1300, "scale": 1.6, "pose": "think", "face": "neutral"}])
shot(T("มันก็เรื่องส่วนตัว"), T("ทำไมหุ้น"), plate="office", cam=cam(1.18, 1.22, 540, 1000),
     actors=[{"who": "worker", "x": 540, "y": 1300, "scale": 1.6, "pose": "shrug", "face": "smile"}])
shot(T("ทำไมหุ้น"), GAP["at"], plate="trade", **{"in": "zoom"}, cam=cam(1.15, 1.35, 640, 620))
# ---- chapter title (voice gap; music stab)
shot(GAP["at"], T("คนซื้อหุ้น"), **{"in": "flash"}, card={"title": "นอกใจ", "sub": "แล้วธุรกิจเจ็บตรงไหน", "size": 200})
# ---- explainer: a share = a piece of the future
shot(T("คนซื้อหุ้น"), T("คือคนที่จ่าย"), plate="floor", cam=cam(1.0, 1.06, 540, 960),
     props=[{"kind": "crowd", "cols": 10, "rows": 6, "x": 270, "y": 720, "dx": 60, "dy": 70, "keep": 60, "cut": 999, "front": True}])
shot(T("คือคนที่จ่าย"), T("และอนาคตของ"), plate="desk", cam=cam(1.0, 1.06),
     props=[{"kind": "cash", "x": 400, "y": 1000, "s": 1.6, "r": 0.12, "front": True},
            {"kind": "check", "x0": 1200, "x": 620, "y": 760, "s": 1.5, "at": T("ซื้ออนาคต") + 0.05, "text": "อนาคต", "front": True}])
shot(T("และอนาคตของ"), T("ผูกอยู่กับ"), plate="city", **{"in": "push"}, cam=cam(1.15, 1.2, 540, 1300, 540, 700),
     photos=[{"img": PH["nvlogo"], "at": T("และอนาคตของ") + 0.5, "x": 540, "y": 620, "w": 520, "h": 96, "rot": 0, "focus": [0.5, 0.5]}])
shot(T("ผูกอยู่กับ"), T("อะไรที่ทำให้"), plate="stage", cam=cam(1.1, 1.18, 540, 940),
     actors=[J(x=540, y=1250, scale=1.6, pose="point", face="grin")],
     counters=[dict(NUMC, **{"from": 0, "to": 33, "suffix": " ปี", "x": 540, "y": 560, "at": T("Jensenมาตลอด33") + 0.6, "dur": 0.8, "size": 170})])
shot(T("อะไรที่ทำให้"), T("ราคาหุ้นก็ร่วงตาม"), plate="trade", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1000),
     actors=[{"who": "analyst", "x": 540, "y": 1300, "scale": 1.6, "pose": "think", "face": "worried"}])
shot(T("ราคาหุ้นก็ร่วงตาม"), T("NewYorkTimesรายงานว่า"), plate="trade", **{"in": "zoom"}, cam=cam(1.25, 1.45, 640, 600))
# ---- woman 1: secrets + government trust
shot(T("NewYorkTimesรายงานว่า"), T("ผู้หญิงคนแรก"), plate="news", **{"in": "push"}, cam=cam(1.05, 1.12, 540, 900),
     photos=[{"img": PH["nyt"], "at": T("NewYorkTimesรายงานว่า") + 0.1, "x": 540, "y": 560, "w": 700, "h": 104, "rot": 0, "focus": [0.5, 0.5]}])
shot(T("ผู้หญิงคนแรก"), T("ที่ทางการสหรัฐ"), plate="meeting", **{"in": "push"}, cam=cam(1.1, 1.16, 540, 1000),
     chip={"text": "สิงคโปร์", "at": T("บริษัทในสิงคโปร์")},
     tags=[{"text": "ผู้บริหารบริษัทในสิงคโปร์", "sub": "รายงานโดย New York Times", "ax": 540, "ay": 1050, "x": 300, "y": 700, "at": T("เป็นผู้บริหาร")}])
shot(T("ที่ทางการสหรัฐ"), T("ซึ่งทางจีน"), plate="city", cam=cam(1.05, 1.1, 540, 900),
     photos=[{"img": PH["capitol"], "at": T("ที่ทางการสหรัฐ") + 0.05, "x": 540, "y": 760, "w": 860, "h": 420, "label": "รัฐสภาสหรัฐ", "credit": CR["capitol"]}],
     tags=[{"text": "สายลับจีน?", "sub": "ตามที่ทางการสหรัฐเชื่อ", "ax": 540, "ay": 1100, "x": 340, "y": 1120, "at": T("เป็นสายลับจีน")}])
shot(T("ซึ่งทางจีน"), T("แต่สภาคองเกรส"), card={"lines": ["จีน: “เป็นการใส่ร้าย", "ไม่มีมูลความจริง”"], "hot": 1, "size": 80,
                                                   "type": T("แต่สภาคองเกรส") - T("ซึ่งทางจีน") - 0.2})
HEAR = [{"who": "lawmaker", "x": 300, "y": 900, "scale": 0.9, "pose": "point", "face": "neutral"},
        {"who": "board1", "x": 780, "y": 900, "scale": 0.9, "pose": "think", "face": "neutral", "dir": -1}]
shot(T("แต่สภาคองเกรส"), T("FBIเอง"), plate="hearing", **{"in": "push"}, cam=cam(1.0, 1.08, 540, 1000),
     actors=HEAR + [J(x=540, y=1420, scale=1.35, pose="idle", face="worried", look=0)])
shot(T("FBIเอง"), T("บอร์ดของNVIDIA"), plate="hearing", cam=cam(1.08, 1.16, 540, 1050),
     actors=HEAR + [J(x=540, y=1420, scale=1.35, pose="head", face="shock")],
     tags=[{"text": "FBI", "sub": "เข้ามาดูเรื่องนี้", "ax": 540, "ay": 1100, "x": 640, "y": 560, "at": T("FBIเอง") + 0.05}])
shot(T("บอร์ดของNVIDIA"), T("ยังไม่เห็นว่า"), plate="board", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1050), actors=BOARD)
shot(T("ยังไม่เห็นว่า"), T("แต่ก็ต้องตั้งทีม"), plate="board", cam=cam(1.1, 1.14, 540, 1050), actors=BOARD,
     chip={"text": "แถลงการณ์บอร์ด · 8 พ.ย. 2026", "at": T("ยังไม่เห็นว่า")})
shot(T("แต่ก็ต้องตั้งทีม"), T("เพราะถ้าสายลับ"), plate="board", cam=cam(1.14, 1.2, 540, 1050),
     actors=[dict(a, pose="point" if a["who"] == "board3" else a["pose"]) for a in BOARD],
     tags=[{"text": "ทีมสอบสวนอิสระ", "ax": 540, "ay": 900, "x": 560, "y": 560, "at": T("สอบสวนอิสระ")}])
shot(T("เพราะถ้าสายลับ"), T("ความลับของบริษัท"), plate="office", **{"in": "push"}, cam=cam(1.1, 1.16, 540, 1000),
     actors=[J(x=360, y=1300, scale=1.5, pose="idle", face="neutral")],
     links=[{"a": [440, 1030], "b": [860, 700], "at": T("เข้าถึงตัวซีอีโอ")}],
     tags=[{"text": "?", "ax": 860, "ay": 700, "x": 820, "y": 520, "at": T("เพราะถ้าสายลับ") + 0.2}])
shot(T("ความลับของบริษัท"), T("และNVIDIAจะขาย"), plate="desk", cam=cam(1.0, 1.12),
     props=[{"kind": "chip", "x": 540, "y": 900, "s": 2.0, "at": T("ความลับของบริษัท"), "label": "", "front": True},
            {"kind": "redx", "x": 540, "y": 900, "r": 170, "at": T("ก็เสี่ยง") + 0.2, "front": True}])
shot(T("และNVIDIAจะขาย"), T("ต้องให้รัฐบาล"), plate="city", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 900),
     props=[{"kind": "chip", "x": 280, "y": 1100, "s": 1.0, "at": T("ชิปAI"), "label": "AI"}, {"kind": "chip", "x": 540, "y": 1100, "s": 1.0, "at": T("ชิปAI") + 0.2, "label": "AI"},
            {"kind": "chip", "x": 800, "y": 1100, "s": 1.0, "at": T("ชิปAI") + 0.4, "label": "AI"}])
shot(T("ต้องให้รัฐบาล"), T("ถ้ารัฐบาลเริ่ม"), plate="desk", cam=cam(1.0, 1.06),
     props=[{"kind": "contract", "x": 540, "y": 900, "s": 1.8, "front": True}],
     tags=[{"text": "ใบอนุญาตส่งออก", "sub": "รัฐบาลสหรัฐ", "ax": 540, "ay": 700, "x": 560, "y": 560, "at": T("สหรัฐอนุญาต")}])
shot(T("ถ้ารัฐบาลเริ่ม"), T("ธุรกิจก้อนใหญ่"), plate="hearing", cam=cam(1.2, 1.28, 400, 860),
     actors=[{"who": "lawmaker", "x": 400, "y": 900, "scale": 1.0, "pose": "think", "face": "worried"}])
shot(T("ธุรกิจก้อนใหญ่"), T("ส่วนคนที่สอง"), plate="desk", cam=cam(1.0, 1.06),
     props=[{"kind": "contract", "x": 540, "y": 900, "s": 1.8, "tear": T("ธุรกิจก้อนใหญ่") + 0.9, "front": True},
            {"kind": "redx", "x": 540, "y": 900, "r": 160, "at": T("ธุรกิจก้อนใหญ่") + 1.2, "front": True}])
# ---- woman 2: rules about bosses and reports
shot(T("ส่วนคนที่สอง"), T("NewYorkTimesรายงาน", 2), plate="office", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1000),
     actors=[J(x=540, y=1300, scale=1.5, pose="idle", face="neutral")],
     counters=[dict(RED, **{"from": 1, "to": 2, "prefix": "คนที่ ", "x": 540, "y": 560, "at": T("ส่วนคนที่สอง") + 0.2, "dur": 0.4, "size": 130})])
shot(T("NewYorkTimesรายงาน", 2), T("NVIDIAยังไม่ได้"), plate="office", cam=cam(1.05, 1.1, 540, 1000),
     actors=[J(x=330, y=1250, scale=1.35, pose="idle", face="neutral"),
             {"who": "worker", "x": 760, "y": 1420, "scale": 1.1, "pose": "idle", "face": "neutral", "dir": -1}],
     links=[{"a": [400, 1000], "b": [760, 1150], "at": T("ที่รายงานตรง")}],
     tags=[{"text": "ผู้บริหารหญิง", "sub": "รายงานตรงกับ Jensen (ตาม NYT)", "ax": 760, "ay": 1150, "x": 330, "y": 520, "at": T("ว่าเป็นผู้บริหารหญิง")}])
shot(T("NVIDIAยังไม่ได้"), T("แต่ถ้าจริง"), plate="board", cam=cam(1.1, 1.14, 540, 1000),
     chip={"text": "NVIDIA ยังไม่ยืนยัน", "at": T("ยืนยันเรื่องนี้")})
shot(T("แต่ถ้าจริง"), T("ปี2018"), plate="stage", **{"in": "push"}, cam=cam(1.08, 1.14, 540, 980),
     actors=[{"who": "staff", "x": 540, "y": 1250, "scale": 1.6, "pose": "head", "face": "shock"}])
shot(T("ปี2018"), T("ปี2019"), plate="stage", cam=cam(1.04, 1.08, 540, 900), chip={"text": "2018", "at": T("ปี2018")},
     photos=[{"img": PH["intel"], "at": T("ปี2018") + 0.1, "x": 540, "y": 760, "w": 560, "h": 240, "rot": -0.02, "label": "ซีอีโอลาออก", "credit": CR["logo"]}])
shot(T("ปี2019"), T("เพราะคบกับ"), plate="stage", cam=cam(1.04, 1.08, 540, 900), chip={"text": "2019", "at": T("ปี2019")},
     photos=[{"img": PH["mcd"], "at": T("ปี2019") + 0.1, "x": 540, "y": 760, "w": 420, "h": 370, "rot": 0.02, "label": "บอร์ดปลดซีอีโอ", "credit": CR["logo"]}])
PAIR = [{"who": "staff", "x": 380, "y": 1280, "scale": 1.45, "pose": "idle", "face": "smile"},
        {"who": "worker", "x": 700, "y": 1290, "scale": 1.4, "pose": "idle", "face": "smile", "dir": -1}]
shot(T("เพราะคบกับ"), T("เจ้านายคบ"), plate="office", **{"in": "push"}, cam=cam(1.1, 1.15, 540, 1000), actors=PAIR,
     tags=[{"text": "ยินยอมทั้งคู่", "ax": 540, "ay": 880, "x": 560, "y": 560, "at": T("ทั้งที่ยินยอม")}])
TEAM = [{"who": "staff", "x": 300, "y": 1240, "scale": 1.3, "pose": "point", "face": "smile"},
        {"who": "worker", "x": 520, "y": 1250, "scale": 1.25, "pose": "idle", "face": "smile", "dir": -1},
        {"who": "analyst", "x": 760, "y": 1400, "scale": 1.15, "pose": "idle", "face": "neutral", "dir": -1},
        {"who": "board2", "x": 920, "y": 1420, "scale": 1.1, "pose": "idle", "face": "neutral", "dir": -1}]
shot(T("เจ้านายคบ"), T("คนอื่นในทีม"), plate="floor", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1000), actors=TEAM,
     links=[{"a": [300, 900], "b": [520, 920], "at": T("ลูกน้องเมื่อไหร่")}])
shot(T("คนอื่นในทีม"), T("แล้วถ้าเขาต้อง"), plate="floor", cam=cam(1.15, 1.25, 700, 1050, 760, 1050),
     actors=[dict(a, face="worried", look=-1, pose="think") if a["who"] in ("analyst", "board2") else a for a in TEAM],
     tags=[{"text": "เลื่อนขั้นแฟร์ไหม?", "ax": 760, "ay": 1100, "x": 520, "y": 560, "at": T("ว่าการเลื่อนขั้น")}])
# ---- succession
shot(T("แล้วถ้าเขาต้อง"), T("ตอนนี้ยังไม่มี"), plate="board", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1050),
     actors=[J(x=540, y=1350, scale=1.5, pose="idle", face="sad", dir=1, walk=True,
               keys=[{"t": T("แล้วถ้าเขาต้อง"), "x": 540}, {"t": T("ตอนนี้ยังไม่มี"), "x": 960}])])
shot(T("ตอนนี้ยังไม่มี"), T("นักวิเคราะห์"), plate="board", cam=cam(1.1, 1.25, 540, 1050, 540, 980),
     tags=[{"text": "ผู้สืบทอด?", "ax": 540, "ay": 1050, "x": 560, "y": 560, "at": T("วางตัวไว้แทน")}])
shot(T("นักวิเคราะห์"), T("และBernstein"), plate="trade", **{"in": "push"}, cam=cam(1.05, 1.12, 540, 1000),
     actors=[{"who": "analyst", "x": 380, "y": 1300, "scale": 1.6, "pose": "point", "face": "talk", "look": 0.5}],
     tags=[{"text": "NVIDIA ไม่มีผู้ก่อตั้ง", "ax": 760, "ay": 700, "x": 480, "y": 560, "at": T("แบบไม่มีผู้ก่อตั้ง")}])
shot(T("และBernstein"), T("งานวิจัยที่ดู"), plate="trade", cam=cam(1.12, 1.18, 540, 900),
     counters=[dict(NUMC, **{"from": 400, "to": 400, "prefix": "$", "x": 540, "y": 900, "at": T("และBernstein") + 0.1, "dur": 0.1, "size": 200, "until": T("ลงครึ่งหนึ่ง")}),
               dict(RED, **{"from": 400, "to": 200, "prefix": "$", "x": 540, "y": 900, "at": T("ลงครึ่งหนึ่ง"), "dur": 0.7, "size": 200})],
     chip={"text": "ราคาเป้าหมายหุ้น NVIDIA · Bernstein", "at": T("และBernstein")})
# ---- research
shot(T("งานวิจัยที่ดู"), T("พบว่าหุ้น"), plate="lab", **{"in": "push"}, cam=cam(1.05, 1.1, 540, 1000),
     counters=[dict(NUMC, **{"from": 0, "to": 219, "suffix": " กรณี", "x": 540, "y": 1000, "at": T("ฉาวของผู้บริหาร219") + 0.8, "dur": 0.9, "size": 170})],
     chip={"text": "งานวิจัย ปี 2015", "at": T("งานวิจัยที่ดู")})
shot(T("พบว่าหุ้น"), T("ต่อให้บอร์ดไล่"), plate="trade", cam=cam(1.15, 1.25, 640, 650),
     counters=[dict(RED, **{"from": 0, "to": 14, "prefix": "-", "suffix": "%", "x": 540, "y": 1000, "at": T("อีก11-14%") + 0.1, "dur": 0.9, "size": 230})],
     chip={"text": "หุ้นลงต่อ 11-14% ใน 12 เดือน", "at": T("อีก11-14%")})
shot(T("ต่อให้บอร์ดไล่"), T("สรุปง่ายๆ"), plate="board", **{"in": "push"}, cam=cam(1.1, 1.16, 540, 1050), actors=BOARD,
     tags=[{"text": "ไล่ออกแล้ว ก็ยังลง", "ax": 540, "ay": 900, "x": 540, "y": 560, "at": T("ซีอีโอออกไปแล้ว")}])
# ---- verdict
shot(T("สรุปง่ายๆ"), T("ตลาดถามแค่ว่า"), card={"lines": ["ตลาดไม่ได้ตัดสิน", "เรื่องศีลธรรม"], "hot": 1, "size": 96,
                                                 "type": T("ตลาดถามแค่ว่า") - T("สรุปง่ายๆ") - 0.3})
shot(T("ตลาดถามแค่ว่า"), T("ตราบใดที่"), card={"lines": ["ความลับยังปลอดภัยไหม?", "กฎในบริษัทยังใช้ได้ไหม?", "พรุ่งนี้ใครคุมบริษัท?"], "hot": 2, "size": 70,
                                               "type": T("ตราบใดที่") - T("ตลาดถามแค่ว่า") - 0.4})
shot(T("ตราบใดที่"), T("และนี่คือเหตุผล"), plate="trade", **{"in": "push"}, cam=cam(1.05, 1.2, 540, 900, 640, 650))
shot(T("และนี่คือเหตุผล"), T("กดติดตาม"), plate="city", **{"in": "push"}, cam=cam(1.2, 1.12, 540, 700, 540, 1100),
     counters=[dict(RED, **{"from": 0, "to": 15, "prefix": "฿", "suffix": " ล้านล้าน", "x": 540, "y": 900, "at": T("กว่า15ล้านล้าน") + 0.1, "dur": 0.9, "size": 150})])
shot(T("กดติดตาม"), END, noLogo=True, cta={"button": "กดติดตาม", "actors": [
    {"who": "analyst", "x": 250, "y": 1560, "scale": 1.4, "pose": "wave", "face": "grin"},
    {"who": "jensen26", "x": 540, "y": 1600, "scale": 1.55, "pose": "wave", "face": "smile"},
    {"who": "worker", "x": 830, "y": 1560, "scale": 1.4, "pose": "wave", "face": "grin", "dir": -1}]})

for a, b in zip(S, S[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6 and a["t1"] > a["t0"], (a, b["t0"])
quiet = [(x["t0"], x["t1"]) for x in S if x.get("card") or x.get("cta")]
caps = [c for c in caps if not any(c["start"] >= q0 - 0.05 and c["start"] < q1 for q0, q1 in quiet)]
for c in caps:
    for q0, q1 in quiet:
        if c["start"] < q0 < c["end"]: c["end"] = q0 - 0.02
D = {"jobBase": here.resolve().as_uri(), "brandBase": (here.parents[2] / "brand").resolve().as_uri(),
     "plates": P, "captions": caps, "capY": 1400, "duration": END,
     "pill": {"from": T("4.5แสนล้าน") + 1.2, "to": T("กดติดตาม") - 0.1, "label": "มูลค่า NVIDIA หายไป",
              "values": sorted([{"t": T("4.5แสนล้าน") + 1.2, "text": "$450B+", "hot": True}] + [v for x in S if x.get("card") for v in ({"t": x["t0"], "text": None}, {"t": x["t1"], "text": "$450B+"})] + [{"t": T("4.5แสนล้าน") + 3.5, "text": "$450B+"}], key=lambda v: v["t"])},
     "music_mute": [[GAP["at"] - 0.05, GAP["at"] + 0.02], [T("สรุปง่ายๆ") - 0.1, T("ตราบใดที่")]],
     "extra_cues": [
        {"t": T("ผมนอกใจ") + 0.05, "sfx": "pen", "db": -20},
        {"t": T("ที่เพิ่งเขียน") + 0.1, "sfx": "pencil", "db": -20, "dur": 1.0},
        {"t": GAP["at"] - 0.35, "sfx": "tapestop", "db": -20},
        {"t": T("ธุรกิจก้อนใหญ่") + 0.9, "sfx": "paper_tear", "db": -16},
        {"t": T("ตลาดถามแค่ว่า"), "sfx": "tick", "db": -24, "dur": T("ตราบใดที่") - T("ตลาดถามแค่ว่า")}],
     "shots": S}
(here / "scene.json").write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "music_mute.txt").write_text(",".join(f"{a:.2f}-{b:.2f}" for a, b in D["music_mute"]), encoding="utf-8")
d = sorted(x["t1"] - x["t0"] for x in S)
print(f"{len(S)} shots, median {d[len(d)//2]:.2f}s, min {d[0]:.2f}s, max {d[-1]:.2f}s, {len(caps)} caption sets, end {END}")
