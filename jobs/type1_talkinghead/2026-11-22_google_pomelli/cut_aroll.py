"""A-roll for เซฟพูด / Google Pomelli (REF_SPEC 40: raw 1080p landscape take, not th_sample).
Source: input/raw/take_103241.mp4 (2026-03-20 10-32-41, 1920x1080 30 fps). Speech starts at ~10 s; pauses from silencedetect
(-35 dB, 0.25 s), lines from local Whisper medium (input/whisper/). Retakes dropped: the half line at 64.3 s and the stumbles
"ฝาก... ฝาก..." at 72.6-77.0 s. Long pauses trimmed (type 1 rule: pauses > 0.35 s removed, handles kept).
Crop: 9:16 window (608x1080) centred on the face track (cx ~0.55, very steady), scaled to 1080x1920.
usage: python cut_aroll.py [--proxy]  ->  input/aroll.mp4 (or out/aroll_proxy.mp4) + edl.json
"""
import json, pathlib, subprocess, sys

here = pathlib.Path(__file__).parent
SRC = here / "input/raw/take_103241.mp4"
EDL = [  # (in, out, caption script for the piece; " / " = caption set break)
    (9.98, 14.32, "เจ้าของแบรนด์ต้องฟัง / คุมโทนแบรนด์ด้วย Pomelli / AI ตัวใหม่จาก Google"),
    (14.52, 17.42, "ใครมีเพื่อนเป็นเจ้าของแบรนด์ / อย่าลืมแชร์คลิปนี้ให้เขานะครับ"),
    (17.88, 20.80, "เจ้าของแบรนด์คงรู้ดีว่า / บรีฟงานที่ไม่ได้ดั่งใจ"),   # v3: the false start "กว่าจะได้… ปวดหัว" (21.0-22.6) cut, last take kept (user 2026-11-24)
    (23.08, 24.98, "กว่าจะได้โปรหนึ่ง / ปวดหัวไป 3 วัน"),
    (25.22, 28.52, "แต่ Pomelli ตัวเนี้ยครับ / เพียงแค่เราวาง website ของเราลงไป"),
    (28.70, 31.28, "AI จะดึงตัวตนของแบรนด์ของเรา / ออกมาให้ทันที"),
    (31.48, 36.10, "ทั้งสีที่ใช่ ฟอนต์ที่ชอบ / และสไตล์ของแบรนด์ / ไม่ต้องมานั่งเซ็ตเองให้เสียเวลา"),
    (36.35, 41.30, "แถมยังช่วยคิดไอเดียแคมเปญได้อีกด้วย / อยากทำโปรโมชันอะไร / แค่พิมพ์บอก AI ไปได้เลยครับ"),
    (42.48, 45.48, "มันจะเสนอคอนเทนต์ที่เข้ากับแบรนด์ / มาให้เลือกอีกเพียบ"),
    (48.98, 57.34, "และที่เด็ดที่สุดคือการแต่งรูปครับ / เราสามารถพิมพ์ให้ AI เปลี่ยนฉากหลัง / หรือเพิ่มลูกเล่นให้ภาพสินค้า / ได้ง่ายๆ เหมือนคุยกับกราฟิกส่วนตัว"),
    (60.30, 63.78, "ตอนนี้เปิดให้คนไทยได้ใช้แล้ว / และที่สำคัญ ฟรีอีกด้วยครับ"),
    (68.12, 71.08, "ใครอยากให้แบรนด์ดูแพงแบบประหยัดงบ / ต้องไปใช้กันแล้ว"),
    (71.22, 72.62, "และถ้าคลิปนี้มีประโยชน์"),
    (77.00, 79.45, "ฝากกดไลค์ กดติดตามเพจ / Data Echooo ไว้ด้วยนะครับ"),
]
CROP = "crop=608:1080:750:0"   # face cx 0.549*1920 = 1054 -> window 750..1358


def main():
    proxy = "--proxy" in sys.argv
    size = "540:960" if proxy else "1080:1920"
    out = here / ("out/aroll_proxy.mp4" if proxy else "input/aroll.mp4")
    out.parent.mkdir(exist_ok=True)
    parts, labels = [], []
    for i, (a, b, _) in enumerate(EDL):
        d = b - a
        parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,{CROP},scale={size}:flags=lanczos,fps=30[v{i}];"
                     f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d - 0.012:.3f}:d=0.012[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(EDL)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "26" if proxy else "14", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", str(out)], check=True)
    t, edl = 0.0, []
    for a, b, line in EDL:
        edl.append(dict(src_in=a, src_out=b, t0=round(t, 3), t1=round(t + b - a, 3), line=line)); t += b - a
    (here / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{out.name}: {len(EDL)} pieces, {t:.1f} s")


if __name__ == "__main__":
    main()
