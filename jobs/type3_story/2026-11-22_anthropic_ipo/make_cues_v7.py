"""EP02 cues v7 + music bed v7 (owner 2026-11-24 on v6: "เพลงห่วย ซาวด์เอฟเฟกต์กาก"; REF_SPEC 67: follow the refs as earshot heard them).
Every cue answers one picture event and names the ref moment it copies (work/refs_business, earshot timeline 2026-11-24):
  thump  = heavy thing lands        r5 0:00.32 (boot stomps down, "punchy impact hit"), r5 0:29.07 (boot + label land, low hit), r2 0:20.32
  msgpop = label / small piece pops r5 0:05.65 (name label "Elias Howe" pops on, "chat message pop"), r2 0:02.22, r2 0:10.94 ("bubble pop")
  ding   = key word / name revealed  r2 0:06.80 (lone word card "impossible", glockenspiel note), r2 0:13.92 (ding), r5 0:19.70, r5 0:26.01
  sweep  = move into a new place     r2 0:03.48 (the only whoosh in 26 s: about one per 25 s here)
  logohit= logo on the end card      REF_SPEC 64; r5 ends on a note at 0:39.26
Out (no ref has them; earshot's 39-film study: never used): counter ratchets, tape stop, tape rewind, stab, clock tick, a whoosh on every push.
Music: no drop-outs (refs: 0 % silence, bed under the whole clip, docs/REF_BUSINESS_2026-11-24.md "Sound").
usage: python make_cues_v7.py   -> cues_v7.json, music_mute_v7.txt"""
import json, pathlib
here = pathlib.Path(__file__).parent
D = json.loads((here / "scene.json").read_text(encoding="utf-8"))
cues = [{"t": 0.0, "sfx": "thump", "db": -6, "why": "news photo lands (r5 0:00.32)"}]
SW = {8.24: "flashback tunnel", 42.42: "into IPO day", 68.0: "the turn: price slides"}
for s in D["shots"]:
    for t0, why in SW.items():
        if abs(s["t0"] - t0) < 0.02: cues.append({"t": s["t0"], "sfx": "sweep", "db": -15, "align": "peak", "why": why + " (r2 0:03.48)"})
    if s.get("card"): cues.append({"t": s["t0"] + 0.05, "sfx": "ding", "db": -9, "why": "word card alone (r2 0:06.80)"})
    for c in s.get("counters", []):
        big = c.get("d3") or abs(c["to"]) >= 900
        cues.append({"t": round(c["at"] + (0.0 if big else 0.02), 2), "sfx": "thump" if big else ("ding" if c["to"] in (83, 34) else "msgpop"), "db": -6 if big else (-9 if c["to"] in (83, 34) else -11),
                     "why": f"number {c.get('prefix','')}{c['to']}{c.get('suffix','')} " + ("lands heavy (r5 0:29.07)" if big else "key figure (r2 0:13.92)" if c["to"] in (83, 34) else "pops on (r5 0:05.65)")})
    for p in s.get("photos", []):
        if p["at"] < 0.1: continue
        logo = "logo" in p["img"] or "antlogo" in p["img"]
        cues.append({"t": round(p["at"], 2), "sfx": "ding" if logo else "msgpop", "db": -9 if logo else -11, "why": ("name / logo revealed (r5 0:19.70)" if logo else "print pops on (r5 0:05.65)")})
    for p in s.get("props", []):
        if p["kind"] == "crowd": cues.append({"t": round(p["at"], 2), "sfx": "msgpop", "db": -11, "why": "crowd pops on (r2 0:10.94)"})
    if s.get("cta"): cues.append({"t": round(s["t0"] + 0.55, 2), "sfx": "logohit", "db": -8, "why": "logo on the end card (REF_SPEC 64)"})
cues.sort(key=lambda c: c["t"])
# one sound per moment: a sweep into a shot wins over the pop of the print that arrives with it
out = []
for c in cues:
    if out and c["t"] - out[-1]["t"] < 0.35: 
        if out[-1]["sfx"] == "sweep": continue
        if c["sfx"] == "sweep": out[-1] = c; continue
    out.append(c)
(here / "cues_v7.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "music_mute_v7.txt").write_text("", encoding="utf-8")
print(len(out), "cues,", round(len(out) / D["duration"] * 60, 1), "per min")
for c in out: print(f"{c['t']:6.2f} {c['sfx']:8s} {c['db']:4d}  {c['why']}")
