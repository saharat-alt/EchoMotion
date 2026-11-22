"""Cut the speaker out of a talking-head clip so graphics can sit BEHIND him (REF_SPEC 39: text behind subject).

usage: python engine/tools/person_matte.py footage.mp4 out_cutout.webm [--stills 1.0,5.0]
Writes a VP9 WebM with alpha, same size, fps and length as the input: the person in full colour, everything else
transparent. A page draws footage -> graphics -> this cutout, all with the same transform, so the speaker covers
the graphics. Model: MediaPipe selfie_segmenter (engine/models/selfie_segmenter.tflite, Apache-2.0), runs locally.
The mask is softened (feather) and smoothed over time so the edge does not crawl.
--stills writes out_cutout_<t>.png previews (person over magenta) to check the edge before using the clip.
"""
import pathlib, subprocess, sys
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

src, out = sys.argv[1], pathlib.Path(sys.argv[2])
stills = [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")] if "--stills" in sys.argv else []
model = str(pathlib.Path(__file__).resolve().parents[1] / "models" / "selfie_segmenter.tflite")
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=model), running_mode=vision.RunningMode.VIDEO, output_confidence_masks=True))

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(fps),
                        "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30", "-row-mt", "1",
                        "-deadline", "good", "-cpu-used", "4", "-auto-alt-ref", "0", str(out)], stdin=subprocess.PIPE)
det = cv2.FaceDetectorYN.create(str(pathlib.Path(model).with_name("face_detection_yunet_2023mar.onnx")), "", (W, H), 0.6, 0.3, 5000)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
prev, face, i, want = None, None, 0, {int(round(t * fps)): t for t in stills}
while True:
    ok, fr = cap.read()
    if not ok: break
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
    m = seg.segment_for_video(img, int(i * 1000 / fps)).confidence_masks[0].numpy_view().astype(np.float32)
    if m.ndim == 3: m = m[..., 0]
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    m = prev * 0.35 + m * 0.65 if prev is not None else m          # temporal smoothing: the edge does not crawl
    prev = m
    core = (m > 0.6).astype(np.uint8)                                # keep only the blob that holds the person
    n, lab, st, _ = cv2.connectedComponentsWithStats(core, 8)
    if n > 1:
        keep = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
        keep = cv2.dilate(keep, np.ones((9, 9), np.uint8))
        m = m * keep
    _, faces = det.detect(fr)                                        # head prior: next to the head only hair/ears count,
    if faces is not None and len(faces):                             # so a colourful bookshelf touching the ear is cut off
        f = max(faces, key=lambda r: r[-1])[:4]
        face = f if face is None else face * 0.7 + f * 0.3
    if face is not None:
        x, y, w, h = face
        cx, cy, rx, ry = x + w / 2, y + h * 0.10, w * 0.62, h * 1.0
        head = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
        m = np.where((yy < y + h * 0.80) & ~head, 0, m)
    a = np.clip((m - 0.5) / 0.22, 0, 1)                              # tighter band: no background bleeding at the hair
    a = cv2.morphologyEx(a, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))  # drop thin slivers (book spines next to the ear)
    a = cv2.GaussianBlur(a, (0, 0), 1.6)                             # feather
    bgra = np.dstack([fr, (a * 255).astype(np.uint8)])
    enc.stdin.write(bgra.tobytes())
    if i in want:
        pv = (fr * a[..., None] + np.array([255, 0, 255]) * (1 - a[..., None])).astype(np.uint8)
        cv2.imwrite(str(out.with_name(f"{out.stem}_{want[i]:g}.png")), pv)
    i += 1
enc.stdin.close(); enc.wait()
print(f"{out.name}: {i} frames {W}x{H} @ {fps:g}")
