# Task: 13 background plates for an animated business story reel (image generation)

Generate 13 vertical images with your image generation tool. Save each as PNG in `out/cine/` (portrait 9:16, at least 1024 px wide).
They are empty sets for a short business documentary. Small flat cartoon characters are drawn on top later by code, so keep the
lower-middle third calm and open (a floor, a desk front or empty ground) and keep the upper half free of clutter for titles.

Style source (owner's references, docs/REF_BUSINESS_2026-11-24.md: "history of money", "Pressure reveals you", "the zipper nobody
cared about"): photoreal cinematic stills, muted colour, one subject per frame, a lot of empty space, soft light, film grain.

## Locked style (use verbatim at the start of every prompt)
Photoreal cinematic still for a business documentary, muted desaturated palette (warm grey, soft sepia, faded teal, deep charcoal), soft directional light, gentle film grain, shallow depth of field, calm uncluttered composition with a lot of empty space, one clear subject, the lower-middle third open and quiet. Vertical 9:16. No people, no faces, no readable text, no logos, no brand names.

## Plates (file → what it shows; each is the place or object of one story beat)
1. `e01_exchange_facade.png` → a big stock-exchange building's glass corner facade at blue-hour dawn, giant blank screens on it, empty wet street in front.
2. `e02_red_ledger.png` → an accountant's desk at night: an open ledger with red ink totals (no readable digits), a calculator, one desk lamp.
3. `e03_research_lab.png` → an AI research lab at night in 2021: whiteboards covered with abstract diagrams, rows of monitors glowing, empty chairs.
4. `e04_leaving.png` → an office desk being cleared: a cardboard box with a plant and books on the desk, a jacket on the chair, late afternoon light.
5. `e05_caution.png` → a long dim server corridor with one amber warning light at the far end, cool haze.
6. `e06_small_startup.png` → a tiny new start-up room: two folding tables pushed together, a few laptops, a whiteboard with sticky notes, bare walls.
7. `e07_launch_night.png` → a single laptop glowing on a desk in a dark room, the screen lit (no readable UI), a coffee cup, city lights through a window.
8. `e08_term_sheets.png` → a polished desk with a tall stack of signed papers, a fountain pen and a closed briefcase, soft morning light.
9. `e09_skyline_up.png` → a city skyline at sunrise seen from a high floor, one tower catching the light, mist below.
10. `e10_trading_up.png` → a stock-exchange trading floor with rows of terminals and big wall screens showing rising green lines (no numbers).
11. `e11_trading_down.png` → the same kind of trading floor later in the day, dimmer, the wall screens showing falling red lines (no numbers).
12. `e12_datacenter_build.png` → a huge data centre under construction at dusk: steel frames, cranes, cable drums on the ground.
13. `e13_bubble.png` → one giant soap bubble floating over a city skyline at dusk, iridescent, about to pop.

Acceptance:
- 13 PNGs with exactly these names, portrait 9:16, at least 1024 px wide.
- One shared look (the locked style). No people, no readable text or logos anywhere.
- Lower-middle third calm and open in every image.

Write only inside `out/cine/`. Final answer: list of files with pixel sizes.
