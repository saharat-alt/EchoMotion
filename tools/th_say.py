"""Make a TTS line say English words with a Thai accent (user rule 2026-11-12, REF_SPEC 31).

Replaces every word in brand/pronunciation_th.json with its Thai spelling, then lists what is still not Thai
(Latin words, digits, $ % symbols) so they can be spelled out before any paid TTS call. Captions keep English.

usage: python tools/th_say.py <tts.txt | -> [--out spoken.txt]
  exit code 0 = clean, 1 = something is left to spell (listed on stderr)
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = json.loads((ROOT / "brand/pronunciation_th.json").read_text(encoding="utf-8"))["words"]
LATIN = re.compile(r"[A-Za-z][A-Za-z0-9'’.\-]*|\d[\d,.]*|[$%€£¥]")


def speak(text):
    for en in sorted(G, key=len, reverse=True):  # longest first: "Google Cloud" before "Google"
        text = re.sub(r"(?<![A-Za-z0-9])" + re.escape(en) + r"(?![A-Za-z0-9])", G[en], text, flags=re.IGNORECASE)
    return text


def leftovers(text):
    # ElevenLabs audio tags like [excited] are directions, not speech
    return sorted(set(LATIN.findall(re.sub(r"\[[^\]]*\]", "", text))))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--out")
    a = ap.parse_args()
    src = sys.stdin.read() if a.src == "-" else pathlib.Path(a.src).read_text(encoding="utf-8")
    out = speak(src)
    (pathlib.Path(a.out).write_text(out, encoding="utf-8") if a.out else sys.stdout.write(out))
    left = leftovers(out)
    if left:
        print("\nยังไม่ได้สะกดเป็นไทย (เพิ่มใน brand/pronunciation_th.json หรือเขียนเป็นคำอ่านในบท): " + ", ".join(left), file=sys.stderr)
        sys.exit(1)
