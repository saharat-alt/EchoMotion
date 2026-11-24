"""Make a mouth-free copy of every rig pose (the drawn mouth painted out from the surrounding skin), so viseme mouths can be
drawn on a clean face instead of over a flat skin-coloured oval.
Why: user 2026-11-23 on EP03 ("ปากเป็นวงกลมมันเป็นวงๆ"): the flat patch colour never matched the face (darker on `wow`,
lighter on `shrug`), so a ring showed around every spoken mouth (REF_SPEC 59).
usage: python engine/tools/mascot_nomouth.py   -> brand/mascot/poses/<name>_nm.png and rig.json poses[name].nomouth
"""
import json, pathlib
import cv2
import numpy as np

M = pathlib.Path(__file__).resolve().parents[2] / "brand/mascot"
R = json.loads((M / "rig.json").read_text())
m = R["mouth"]
for name, p in R["poses"].items():
    rgba = cv2.imread(str(M / p["file"]), cv2.IMREAD_UNCHANGED)
    bgr, a = rgba[..., :3].copy(), rgba[..., 3]
    region = np.zeros(a.shape, np.uint8)   # where a mouth can be: a little wider and lower than the base mouth
    cv2.ellipse(region, (int(m["cx"]), int(m["cy"] + m["h"] * 0.2)), (int(m["w"] * 0.78), int(m["h"] * 0.8)), 0, 0, 360, 255, -1)
    skin = np.median(bgr[(region > 0) & (a > 200)], axis=0)
    diff = np.abs(bgr.astype(int) - skin).sum(axis=2)
    mask = ((diff > 70) & (region > 0) & (a > 200)).astype(np.uint8) * 255
    # keep hands/fingers that reach into the region (big components touching its edge are not the mouth)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 4000: mask[lab == i] = 0
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    out = cv2.inpaint(bgr, mask, 9, cv2.INPAINT_TELEA)
    out = cv2.GaussianBlur(out, (0, 0), 1.2) * (cv2.GaussianBlur(mask, (0, 0), 3)[..., None] / 255.0) + out * (1 - cv2.GaussianBlur(mask, (0, 0), 3)[..., None] / 255.0)
    f = f"poses/{name}_nm.png"
    cv2.imwrite(str(M / f), np.dstack([out.astype(np.uint8), a]))
    p["nomouth"] = f
    print(f"{name}: painted out {int((mask > 0).sum())} px")
(M / "rig.json").write_text(json.dumps(R, indent=1), encoding="utf-8")
