"""Turn generated mascot images (white background) into rig-ready layers that line up with brand/mascot/base_wave.png.

usage: python engine/tools/mascot_prep.py <poses_dir> [--wow <pose_wow.png>]
  poses_dir   folder with pose_*.png (Codex output, docs/prompts/codex_mascot_gestures.md) and mouth_sheet.png
writes brand/mascot/poses/<name>.png (900x1355 RGBA, head aligned to base_wave by the two glasses lenses),
       brand/mascot/visemes/<name>.png (8 mouth shapes, scaled to the base mouth), brand/mascot/rig.json
       (mouth centre on the canvas, mouth size, per-pose skin colour for the patch that hides the drawn closed mouth).
Why: owner review 2026-11-22 (REF_SPEC 38): the old rig squashed one mouth image by loudness ("ปากเปิดปิดแปลกๆ") and had
too few gestures. Every pose must share the head position or the head would jump at each pose change.
"""
import json, pathlib, sys
import cv2
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
M = ROOT / "brand/mascot"
src = pathlib.Path(sys.argv[1])
CW, CH = 900, 1355
VIS = ["rest", "mbp", "small", "a", "e", "o", "u", "fv"]   # grid order on the sheet (row 1 then row 2)


def white_to_alpha(bgr):
    """Background = near-white region connected to the image border (the dark outline keeps the inside white parts)."""
    h, w = bgr.shape[:2]
    near = (bgr.min(axis=2) > 232).astype(np.uint8)
    n, lab = cv2.connectedComponents(near, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border)).astype(np.uint8)
    bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    a = (1 - bg).astype(np.float32)
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    return np.dstack([bgr, (a * 255).astype(np.uint8)])


def lenses(rgba):
    """Centres of the two glasses lenses: the two biggest dark ring components in the head area."""
    bgr, a = rgba[..., :3], rgba[..., 3]
    h, w = a.shape
    dark = ((bgr.max(axis=2) < 70) & (a > 200)).astype(np.uint8)
    dark[int(h * 0.62):] = 0                       # head only (the T-shirt is black too)
    dark[: int(h * 0.15)] = 0
    n, lab, st, cen = cv2.connectedComponentsWithStats(dark, 8)
    cand = [i for i in range(1, n) if st[i, cv2.CC_STAT_WIDTH] > w * 0.06 and st[i, cv2.CC_STAT_HEIGHT] > h * 0.03]
    if not cand: raise ValueError("no glasses found")
    big = max(cand, key=lambda i: st[i, cv2.CC_STAT_AREA])
    x, y, bw, bh = st[big, :4]
    if bw > w * 0.3:                               # both lenses + bridge are one component: split it in two halves
        ys, xs = np.nonzero(lab == big); mid = x + bw / 2
        L, R = xs < mid, xs >= mid
        return np.array([[xs[L].mean(), ys[L].mean()], [xs[R].mean(), ys[R].mean()]])
    two = sorted(cand, key=lambda i: -st[i, cv2.CC_STAT_AREA])[:2]
    return np.array(sorted([cen[i] for i in two], key=lambda p: p[0]))


def match_eyes(rgba, base, ref_eyes):
    """Find the base's glasses band in the pose by multi-scale template matching (robust when hair touches the frames)."""
    def gray(img):
        a = img[..., 3:4].astype(np.float32) / 255 if img.shape[2] == 4 else 1
        return cv2.cvtColor((img[..., :3] * a + 255 * (1 - a)).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    x0, x1 = int(ref_eyes[:, 0].min() - 120), int(ref_eyes[:, 0].max() + 120)
    y0, y1 = int(ref_eyes[:, 1].min() - 90), int(ref_eyes[:, 1].max() + 90)
    tpl, img = gray(base)[y0:y1, x0:x1], gray(rgba)
    best = (-1, None, None)
    for sc in np.linspace(0.9, 1.5, 31):
        t = cv2.resize(tpl, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        if t.shape[0] >= img.shape[0] or t.shape[1] >= img.shape[1]: continue
        r = cv2.matchTemplate(img[: int(img.shape[0] * 0.7)], t, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]: best = (mx, sc, loc)
    mx, sc, loc = best
    return np.array([[loc[0] + (e[0] - x0) * sc, loc[1] + (e[1] - y0) * sc] for e in ref_eyes]), mx


def align(rgba, ref_eyes, base=None):
    e, score = match_eyes(rgba, base, ref_eyes)
    print(f"   match score {score:.2f}")
    s = np.linalg.norm(ref_eyes[1] - ref_eyes[0]) / np.linalg.norm(e[1] - e[0])
    c_src, c_ref = e.mean(axis=0), ref_eyes.mean(axis=0)
    A = np.array([[s, 0, c_ref[0] - s * c_src[0]], [0, s, c_ref[1] - s * c_src[1]]], np.float32)
    return cv2.warpAffine(rgba, A, (CW, CH), flags=cv2.INTER_AREA, borderValue=(0, 0, 0, 0))


def main():
    base = cv2.imread(str(M / "base_wave.png"), cv2.IMREAD_UNCHANGED)
    ref = lenses(base)
    ma = cv2.imread(str(M / "mouth_shape_wave.png"), cv2.IMREAD_UNCHANGED)[..., 3]
    ys, xs = np.nonzero(ma > 40)
    mouth = {"cx": float(xs.mean()), "cy": float(ys.mean()), "w": float(xs.max() - xs.min()), "h": float(ys.max() - ys.min())}
    (M / "poses").mkdir(exist_ok=True); (M / "visemes").mkdir(exist_ok=True)
    rig = {"canvas": [CW, CH], "mouth": mouth, "poses": {}, "visemes": VIS}
    files = sorted(src.glob("pose_*.png"))
    if "--wow" in sys.argv: files = [f for f in files if f.name != "pose_wow.png"] + [pathlib.Path(sys.argv[sys.argv.index("--wow") + 1])]
    for f in files:
        name = f.stem.replace("pose_", "")
        out = align(white_to_alpha(cv2.imread(str(f))), ref, base)
        cv2.imwrite(str(M / "poses" / f"{name}.png"), out)
        # skin colour right below the mouth (the patch that hides each pose's own closed mouth)
        x0, y0 = int(mouth["cx"] + mouth["w"] * 0.9), int(mouth["cy"])
        skin = out[y0 - 4:y0 + 4, x0 - 20:x0 + 20, :3].reshape(-1, 3).mean(axis=0)[::-1]
        rig["poses"][name] = {"file": f"poses/{name}.png", "skin": [int(v) for v in skin]}
        print(f"pose {name}: aligned, skin {rig['poses'][name]['skin']}")
    # mouth sheet -> 8 visemes, all scaled with ONE factor so their relative sizes stay as drawn
    sheet = white_to_alpha(cv2.imread(str(src / "mouth_sheet.png")))
    a = (sheet[..., 3] > 60).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(cv2.dilate(a, np.ones((9, 9), np.uint8)), 8)
    comps = sorted([i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 200], key=lambda i: -st[i, cv2.CC_STAT_AREA])[:8]
    rows = sorted(comps, key=lambda i: cen[i][1]); top, bot = sorted(rows[:4], key=lambda i: cen[i][0]), sorted(rows[4:], key=lambda i: cen[i][0])
    order = top + bot
    k = mouth["w"] * 1.05 / st[order[0], cv2.CC_STAT_WIDTH]      # the closed smile ("rest") = the base mouth width
    for name, i in zip(VIS, order):
        x, y, w, h = st[i, :4]; pad = 6
        crop = sheet[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad]
        crop = cv2.resize(crop, (max(1, int(crop.shape[1] * k)), max(1, int(crop.shape[0] * k))), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(M / "visemes" / f"{name}.png"), crop)
    rig["viseme_scale"] = k
    (M / "rig.json").write_text(json.dumps(rig, indent=1), encoding="utf-8")
    print(f"visemes: {VIS}, scale {k:.3f}; mouth at ({mouth['cx']:.0f}, {mouth['cy']:.0f})")


if __name__ == "__main__":
    main()
