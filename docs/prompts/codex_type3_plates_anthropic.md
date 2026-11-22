# Task: 5 background plates for an animated business story (Anthropic IPO), toned-down brand style (image generation)

Generate 5 vertical images with your image generation tool. Save each as PNG in `out/plates/` (portrait 9:16 if possible, else 2:3, at least 1024 px wide).
They are empty stage sets for a flat 2D animated short. Characters are drawn on top later by code, so leave the lower-middle area open as a floor/stage.
Match the attached reference plates (n_boardroom.png, n_trading.png): same drawing style, same perspective feel, same palette.

## Locked style (use verbatim at the start of every prompt)
<!-- toned-down CI, user 2026-11-13 (REF_SPEC 36) -->
Flat 2D vector illustration background for a calm, modern animated explainer, clean simple shapes, soft gentle gradients, no outlines. Palette: warm off-white and light warm grey walls (#F6F4EF, #E9E6DF), pale natural oak wood for floors and tables, soft charcoal grey (#4A4F5A) for chairs and dark details, a little muted sage green from plants. Cobalt blue (#214AFF) appears on only ONE or TWO small objects in the whole scene (e.g. one chair, one book, a screen frame). No other saturated colours except at most one tiny orange (#FE4C1C) detail. Soft daylight, gentle shadows. Calm, uncluttered. No people, no characters, no readable text, no logos.

## Plates
1. `p01_lab.png` → an AI research lab office: long white desks with several monitors showing abstract soft graphs, a whiteboard with blank diagrams (no readable text), glass wall, plants. Floor open in the lower middle.
2. `p02_startup.png` → a small brand-new start-up room: a few mismatched chairs around one round table, cardboard boxes not yet unpacked, a blank whiteboard on wheels, a big window. Floor open in the lower middle.
3. `p03_server.png` → a bright, clean server room: rows of grey server racks with small green status lights, cable trays above, one rack door in cobalt. Floor open in the lower middle.
4. `p04_exchange.png` → a stock exchange hall seen from the floor: a huge curved wall of screens with abstract rising candlestick charts and ticker bands (no readable text or logos), a podium with a small bell on the right, a few empty trader desks. Floor open in the lower middle.
5. `p05_bills.png` → an accountant's desk seen from the front: tall stacks of paper bills and invoices (no readable text), a calculator, an open laptop showing a falling line chart (the drop marked by the one tiny orange touch), a desk lamp. Space in front of the desk for characters.

Acceptance:
- 5 PNGs with exactly these names, portrait, at least 1024 px wide.
- Bright overall; mostly neutral with tiny blue; no people, no readable text, no logos; one shared style with the references.

Write only inside `out/plates/`. Final answer: list of files with pixel sizes.
