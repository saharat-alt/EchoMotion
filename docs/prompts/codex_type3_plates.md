# Task: 3 background plates for an animated story reel, in a neutral set with brand-blue accents (image generation)

Generate 3 vertical images with your image generation tool. Save each as PNG in `out/story_brand/` (portrait 9:16 if possible, else 2:3, at least 1024 px wide).
They are empty stage sets for a flat 2D animated short. Characters are drawn on top later by code, so leave the lower-middle area open as a floor/stage.
A previous version was too dark and moody (navy night + orange lamps). The client wants their own brand mood instead: bright, clean, friendly, optimistic tech.

## Locked style (use verbatim at the start of every prompt)
<!-- toned-down CI, user 2026-11-13 (REF_SPEC 36); old all-cobalt paragraph retired -->
Flat 2D vector illustration background for a calm, modern animated explainer, clean simple shapes, soft gentle gradients, no outlines. Palette: warm off-white and light warm grey walls (#F6F4EF, #E9E6DF), pale natural oak wood for floors and tables, soft charcoal grey (#4A4F5A) for chairs and dark details, a little muted sage green from plants. Cobalt blue (#214AFF) appears on only ONE or TWO small objects in the whole scene (e.g. one chair, one book, a screen frame). No other saturated colours except at most one tiny orange (#FE4C1C) detail. Soft daylight, gentle shadows. Calm, uncluttered. No people, no characters, no readable text, no logos.

## Plates
1. `b01_kitchen.png` → a small diner kitchen: a steel dish sink with a stack of plates centre-left, a round wall clock, a window, one hanging lamp. Floor area open in the lower middle.
2. `b02_booth.png` → a diner booth seen from the front: a booth seat and a table with three coffee cups and paper napkins, a big window behind. Space for three seated characters behind the table.
3. `b03_office.png` → a tiny start-up office in the 1990s: one desk with a beige CRT computer, a desk lamp, a wall calendar (no readable text), a few boxes, window with a city skyline. Floor open in the lower middle.

Acceptance:
- 3 PNGs with exactly these names, portrait, at least 1024 px wide.
- Bright overall (no night scenes); palette as above; one shared style; no people, no readable text or logos.

Write only inside `out/story_brand/`. Final answer: list of files with pixel sizes.
