"""Screenshot paragraphs of a web article and record pixel boxes of key phrases (for highlighter sweeps).

usage: python engine/tools/grab_doc.py URL OUT_DIR spec.json
spec.json: {"name": {"anchor": "text inside the paragraph", "phrases": ["exact phrase", ...], "big": 40?}, ...}  (big = re-set the paragraph at that font size, 640 px wide)
writes OUT_DIR/<name>.png (2x) and OUT_DIR/docs.json {name: {w,h,phrases:{phrase:[[x,y,w,h],...]}}}
"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

url, out, spec = sys.argv[1], pathlib.Path(sys.argv[2]), json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))
out.mkdir(parents=True, exist_ok=True)
JS = """([anchor, phrases, sel, big]) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, el = null;
  while ((n = w.nextNode())) if (n.textContent.includes(anchor)) { el = n.parentElement.closest(sel || 'p,blockquote,li,div'); break; }
  if (!el) return null;
  if (big) {  // "big": re-set the real paragraph in large type so the quote reads on a phone (owner 2026-11-23: inserts "เล็กๆจิ๋วๆ มองยาก")
    // !important on the paragraph and every child: news sites set font-size with their own !important / per-span rules
    const set = (e, k, v) => e.style.setProperty(k, v, 'important');
    for (const [k, v] of Object.entries({'font-size': big + 'px', 'line-height': '1.45', 'max-width': '640px', 'width': '640px', 'padding': '20px 26px', 'background': '#fff', 'color': '#111'})) set(el, k, v);
    for (const c of el.querySelectorAll('*')) { set(c, 'font-size', 'inherit'); set(c, 'line-height', 'inherit'); }
  }
  el.scrollIntoView({block: 'center'});
  const box = el.getBoundingClientRect(); const res = {};
  for (const ph of phrases) {
    res[ph] = [];
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let t;
    while ((t = tw.nextNode())) {
      const i = t.textContent.indexOf(ph); if (i < 0) continue;
      const r = document.createRange(); r.setStart(t, i); r.setEnd(t, i + ph.length);
      for (const q of r.getClientRects()) res[ph].push([q.x - box.x, q.y - box.y, q.width, q.height]);
      break;
    }
  }
  el.setAttribute('data-grab', '1');
  return {w: box.width, h: box.height, phrases: res};
}"""
meta = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
    pg.goto(url, wait_until="domcontentloaded"); pg.wait_for_timeout(1200)
    for name, s in spec.items():
        r = pg.evaluate(JS, [s["anchor"], s.get("phrases", []), s.get("closest"), s.get("big", 0)])
        if not r:
            print("miss", name); continue
        pg.wait_for_timeout(300)
        pg.locator("[data-grab='1']").first.screenshot(path=str(out / f"{name}.png"))
        pg.evaluate("document.querySelector(\"[data-grab='1']\").removeAttribute('data-grab')")
        k = 2  # device_scale_factor
        meta[name] = {"w": r["w"] * k, "h": r["h"] * k, "phrases": {ph: [[v * k for v in q] for q in qs] for ph, qs in r["phrases"].items()}}
        print("ok", name, {ph: len(q) for ph, q in r["phrases"].items()})
    b.close()
old = json.loads((out / "docs.json").read_text(encoding="utf-8")) if (out / "docs.json").exists() else {}  # merge, never drop earlier grabs
old.update(meta); (out / "docs.json").write_text(json.dumps(old, indent=1), encoding="utf-8")
