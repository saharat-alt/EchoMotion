"""Voice prep: ElevenLabs take (Safe, one call, 1,301 credits) -> 1.6 s gap after the hook for the title card.
Word timing = local Whisper medium tokens (input/whisper/voice16.json), Thai comes back as short char runs; good enough to
align the caption script (captions.sets_from_script). Writes input/voice.wav, input/words.json, input/title_gap.json.
usage: python prep_voice.py"""
import json, pathlib, subprocess
here = pathlib.Path(__file__).parent
GAP = 1.6
d = json.loads((here / "input/whisper/voice16.json").read_text(encoding="utf-8"))
W = [{"text": w["word"].strip(), "start": w["start"], "end": w["end"]} for s in d["segments"] for w in s.get("words", []) if w["word"].strip()]
hook_end = next(s["end"] for s in d["segments"] if "ขาดทุน" in s["text"])
nxt = next(s["start"] for s in d["segments"] if s["start"] >= hook_end - 0.01)
cut = 6.45  # middle of the measured pause after the hook (silencedetect -40 dB: 6.18-6.70 s); Whisper put the next word too early
for w in W:
    if w["start"] >= cut: w["start"] += GAP; w["end"] += GAP
(here / "input/words.json").write_text(json.dumps(W, ensure_ascii=False), encoding="utf-8")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(here / "input/voice_raw.mp3"), "-filter_complex",
                f"[0]atrim=0:{cut},asetpts=N/SR/TB[a];[0]atrim={cut},asetpts=N/SR/TB[b];aevalsrc=0:d={GAP}:s=44100[s];[a][s][b]concat=n=3:v=0:a=1",
                "-ar", "48000", "-ac", "1", str(here / "input/voice.wav")], check=True)
(here / "input/title_gap.json").write_text(json.dumps({"at": cut, "dur": GAP}), encoding="utf-8")
print(f"title gap at {cut:.2f}s (+{GAP}s), {len(W)} tokens")
