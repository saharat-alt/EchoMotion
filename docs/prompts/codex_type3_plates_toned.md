# Task: 4 sample background plates, toned-down brand colour (image generation)

Generate 4 vertical images with your image generation tool. Save each as PNG in `out/toned/` (portrait 9:16 if possible, else 2:3, at least 1024 px wide).
They are empty stage sets for a flat 2D animated business story short. Characters are drawn on top later by code, so leave the lower-middle area open as a floor/stage.
Keep the same flat vector drawing style as the attached reference plates (shapes, perspective, soft light), but CHANGE THE COLOURS as below: the reference is too blue everywhere.

## Style N: neutral set, blue only as an accent (use verbatim at the start of N prompts)
Flat 2D vector illustration background for a calm, modern animated explainer, clean simple shapes, soft gentle gradients, no outlines. Palette: warm off-white and light warm grey walls (#F6F4EF, #E9E6DF), pale natural oak wood for floors and tables, soft charcoal grey (#4A4F5A) for chairs and dark details, a little muted sage green from plants. Cobalt blue (#214AFF) appears on only ONE or TWO small objects in the whole scene (e.g. one chair, one book, a screen frame). No other saturated colours except at most one tiny orange (#FE4C1C) detail. Soft daylight, gentle shadows. No people, no readable text, no logos.

## Style W: warm editorial (use verbatim at the start of W prompts)
Flat 2D vector illustration background for a warm, editorial-style animated business story, clean simple shapes, subtle paper grain, no outlines. Palette: cream and sand walls (#F3EBDD, #E6D8C3), walnut and honey wood furniture, deep navy (#1E2A4A) for chairs and dark accents, muted terracotta (#C8643B) as the one warm accent, faded sky blue only in windows. Pure cobalt blue does not appear. Late-morning sunlight, soft long shadows. No people, no readable text, no logos.

## Plates
1. `n_boardroom.png` (style N) → corporate boardroom seen from the front: long table running away from the camera, empty chairs both sides, big window with a city skyline, a blank wall screen. Open floor in the lower middle in front of the table.
2. `w_boardroom.png` (style W) → same boardroom composition as 1.
3. `n_trading.png` (style N) → stock market trading wall: a big wall of screens with simple line charts going DOWN (the drop marked by the one orange touch), a few empty desks with monitors in front, open floor in the lower middle.
4. `w_trading.png` (style W) → same trading composition as 3 (the drop marked in terracotta).

Acceptance:
- 4 PNGs with exactly these names, portrait, at least 1024 px wide.
- Bright overall; palettes as described (N: mostly neutral with tiny blue; W: warm, no cobalt); no people, no readable text or logos.

Write only inside `out/toned/`. Final answer: list of files with pixel sizes.
