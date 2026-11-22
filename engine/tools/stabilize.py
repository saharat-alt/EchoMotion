"""Lock a talking-head shot to the background: measure the camera's own micro-shake on a background patch that the
speaker never covers, and shift each frame back. Static camera look (REF_SPEC 49).

usage: python engine/tools/stabilize.py in.mp4 out.mp4 [--patch x,y,w,h] [--zoom 1.03]
  --patch  background area in the INPUT frame (default: top-left 22% x 25%, e.g. a bookshelf)
  --zoom   small scale-up so the shifted edges never show
Each frame's offset to the previous one (phase correlation) is summed into a path; the whole path is removed
(the camera is meant to be still), restarting at cuts (a jump > 12 px = a new piece of the edit). Audio is copied.
"""
import subprocess, sys
import cv2
import numpy as np

src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)); fps = cap.get(cv2.CAP_PROP_FPS) or 30
x, y, w, h = [int(v) for v in sys.argv[sys.argv.index("--patch") + 1].split(",")] if "--patch" in sys.argv else (0, 0, int(W * 0.22), int(H * 0.25))
zoom = float(sys.argv[sys.argv.index("--zoom") + 1]) if "--zoom" in sys.argv else 1.03
win = cv2.createHanningWindow((w, h), cv2.CV_32F)
frames, path, prev, acc = [], [], None, np.zeros(2)
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.cvtColor(f[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY).astype(np.float32)
    if prev is not None:
        (dx, dy), _ = cv2.phaseCorrelate(prev, g, win)
        acc = np.zeros(2) if max(abs(dx), abs(dy)) > 12 else acc + (dx, dy)   # a cut: start a new still shot
    path.append(acc.copy()); prev = g; frames.append(f)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                        "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                        "-c:a", "copy", out], stdin=subprocess.PIPE)
for f, (dx, dy) in zip(frames, path):
    M = np.float32([[zoom, 0, -dx * zoom + W * (1 - zoom) / 2], [0, zoom, -dy * zoom + H * (1 - zoom) / 2]])
    enc.stdin.write(cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
enc.stdin.close(); enc.wait()
p = np.array(path); print(f"{out}: {len(frames)} frames, removed drift up to {np.abs(p).max():.1f} px")
