"""Brand watermark on a finished clip (user 2026-11-24: "โลโก้แรกจะแปะเป็นลายน้ำไว้ทุกคลิปตำแหน่งเดียวกัน").
Reads brand.json logo.watermark (file, x, y, w, opacity, shadow) so every clip and teammate uses the same place.
usage: python engine/tools/watermark.py in.mp4 out.mp4 --until END_CARD_START_SECONDS
  --until  hide the watermark from this time on (the end card already shows the big logo)
Audio is copied; video re-encoded with the project x264 settings."""
import json, pathlib, subprocess, sys
R = pathlib.Path(__file__).resolve().parents[2]
B = json.loads((R / "brand/brand.json").read_text(encoding="utf-8"))["logo"]["watermark"]
src, out = sys.argv[1], sys.argv[2]
until = float(sys.argv[sys.argv.index("--until") + 1]) if "--until" in sys.argv else 1e9
logo = str(R / "brand" / B["file"])
sh = ("[w]split[a][b];[b]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.45,boxblur=6:1[s];[s][a]overlay=3:4[w2];" if B.get("shadow") else "[w]copy[w2];")
fc = (f"[1:v]scale={B['w']}:-1,format=rgba,colorchannelmixer=aa={B['opacity']}[w];{sh}"
      f"[0:v][w2]overlay={B['x']}:{B['y']}:enable='lt(t,{until})'[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", logo, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", out], check=True)
print(f"{out}: watermark {pathlib.Path(logo).name} at ({B['x']},{B['y']}) w {B['w']}, hidden from {until:.2f} s")
