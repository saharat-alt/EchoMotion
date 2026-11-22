# Mascot "เซฟการ์ตูน": extra gestures + mouth shapes (brief, 2026-11-22)

Why: owner feedback on เล่าข่าว (type2_news_fable52_v8): the mouth "opens and closes oddly" (today one mouth
shape is squashed by loudness, `engine/web/de.js`), and the mascot needs more hand gestures.
Use these prompts in any image tool (Codex / ChatGPT / Midjourney / the team's own generator).
Attach `brand/mascot/base_wave.png` as the character reference on every prompt.

## Delivery rules (so the engine can swap them in without manual fixing)
- PNG, transparent background, **900 x 1355 px** (same canvas as `base_wave.png`).
- Same framing as `base_wave.png`: bust cut at the bottom edge, **head in the same place and the same size**
  (eye line at y ≈ 560, chin at y ≈ 740, face centred at x ≈ 470). Only arms/hands change between poses.
- Face neutral with the **mouth closed** in every pose (mouths are layered on top by the engine).
- File names exactly as listed below, saved to `brand/mascot/`.

## Style paragraph (paste first in every prompt)
> Chibi-proportioned 2D cartoon bust of the same young Thai man as the reference image: brown messy short hair
> with warm highlights, round black glasses, big brown eyes, soft pink blush, plain black crew-neck T-shirt.
> Clean dark-brown outline (about 4 px at this size), soft cel shading, slightly textured warm skin, no gradients
> in the background. Transparent background. Front view, head and shoulders down to mid-torso, cut by the bottom
> edge of the canvas. Keep the head identical in size and position to the reference; only the arms and hands
> change. Mouth closed, relaxed. Hands have 5 clean fingers, simple cartoon shapes.

## Poses (one image each)
| file | prompt tail (after the style paragraph) | used for |
|---|---|---|
| `pose_point_up.png` | Right index finger pointing straight up next to his head, left arm relaxed. | "ข้อแรก", new fact |
| `pose_point_side.png` | Right arm extended to the viewer's left, open hand presenting something beside him. | pointing at a card/doc |
| `pose_explain.png` | Both hands in front of the chest, palms open and slightly apart, explaining. | default talking pose |
| `pose_count_1.png` | Right hand raised at shoulder height showing ONE finger. | "หนึ่ง" in a list |
| `pose_count_2.png` | Same, showing TWO fingers (V shape, back of hand to camera is fine). | "สอง" |
| `pose_count_3.png` | Same, showing THREE fingers. | "สาม" |
| `pose_shrug.png` | Both shoulders up, both palms up at waist height, shrug. | "ไม่แน่ใจ", caveats |
| `pose_wow.png` | Both hands up near the cheeks, fingers spread, surprised (eyebrows up, mouth still closed). | big numbers |
| `pose_chin.png` | Right hand on chin, left arm crossed under it, thinking. | questions |
| `pose_arms_crossed.png` | Arms crossed over chest, confident. | verdict / summary |
| `pose_ok.png` | Right hand making an OK sign near the shoulder. | "ใช้ได้" |
| `pose_hold_card.png` | Both hands holding a blank white card (about 300 x 200 px) in front of the chest, card face to camera. | the engine prints a number/logo on the card |
| `pose_phone.png` | Right hand holding a smartphone up, screen facing the viewer (screen blank white). | app / product demo |
| `pose_bye.png` | Both hands waving at shoulder height, big wave. | end card |

## Mouth shapes (one sheet, then cut into files)
Thai visemes the engine needs. Draw only the mouth, same outline weight, on a transparent 220 x 160 px tile,
centred, at the exact scale of the mouth in `base_wave.png`.
> Same cartoon style as the reference. A set of 8 separate mouth shapes for lip-sync, each on its own
> transparent tile, same size and line weight as the reference mouth, dark-brown outline, dark-red inner mouth,
> small white upper teeth where visible, pink tongue only where noted.

| file | shape | Thai sounds |
|---|---|---|
| `mouth_rest.png` | closed gentle smile (same as base) | silence |
| `mouth_mbp.png` | lips pressed flat | ม บ ป พ ผ ภ |
| `mouth_small.png` | slightly open, teeth just visible | most consonants, ะ |
| `mouth_a.png` | wide open, tongue low | า อา |
| `mouth_e.png` | wide and flat, teeth showing | อี เอ แอ |
| `mouth_o.png` | round O | โอ ออ |
| `mouth_u.png` | small round pucker | อู อุ ว |
| `mouth_fv.png` | upper teeth on lower lip | ฟ ฝ (English f/v) |
