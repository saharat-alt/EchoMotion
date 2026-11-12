"""Voice prep for v2: tighten (engine/tighten.py) then open a gap before "คนซื้อหุ้น" for the chapter title card.
usage: python prep_voice_v2.py   (reads voice_el/full_v2.mp3 + voice_el/words_raw_v2.json, writes input/voice.wav + input/words.json)"""
import json, pathlib, subprocess, sys
here = pathlib.Path(__file__).parent; root = here.parents[2]; py = sys.executable
GAP = 1.6  # seconds of silence for the title card (music stab carries it)
subprocess.run([py, str(root / "engine/tighten.py"), str(here / "voice_el/full_v2.mp3"), str(here / "voice_el/words_raw_v2.json"),
                str(here / "input/voice_tight.wav"), str(here / "input/words_tight.json"), "--max", "0.28", "--keep", "0.18", "--tempo", "1.1"], check=True)
d = json.loads((here / "input/words_tight.json").read_text(encoding="utf-8")); W = d["words"] if isinstance(d, dict) else d
# find "คนซื้อหุ้น": first char run "คนซื้อ" after "ร่วง"
txt = "".join(w["text"] for w in W); i = txt.find("คนซื้อ", txt.find("ร่วง"))
acc = 0
for w in W:
    if acc >= i: cut = w["start"] - 0.12; break
    acc += len(w["text"])
for w in W:
    if w["start"] >= cut: w["start"] += GAP; w["end"] += GAP
(here / "input/words.json").write_text(json.dumps(W, ensure_ascii=False), encoding="utf-8")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(here / "input/voice_tight.wav"), "-filter_complex",
                f"[0]atrim=0:{cut},asetpts=N/SR/TB[a];[0]atrim={cut},asetpts=N/SR/TB[b];aevalsrc=0:d={GAP}:s=48000[s];[a][s][b]concat=n=3:v=0:a=1",
                "-ar", "48000", str(here / "input/voice.wav")], check=True)
(here / "input/title_gap.json").write_text(json.dumps({"at": round(cut, 3), "dur": GAP}), encoding="utf-8")
print(f"title gap at {cut:.2f}s (+{GAP}s)")
