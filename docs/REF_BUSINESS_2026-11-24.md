# เล่า Business: new tone refs (owner, 2026-11-24)

The owner sent 7 Pinterest pins: "อยากให้เล่า Business มันเป็นโทนนี้ ... หยิบสไตล์มาใช้ แต่คงตัวละครที่หน้าเหมือนคนในข่าว แบบหน้าโง่ๆ เหมือนเดิม".
Files are kept locally in `work/refs_business/` (gitignored; third-party media, never commit).

| # | Pin | Length | Cuts/s | What it is |
|---|-----|--------|--------|------------|
| r1 | pinterest.com/pin/933230354040919306 | 116 s | 0.18 | Flat vector illustration (teal + orange), Arabic narration, Spielberg biography |
| r2 | pinterest.com/pin/1086986060091863153 | 26 s | 0.84 | Photoreal vintage scenes + tiny serif words on blank grey; "history of money" |
| r3 | pinterest.com/pin/881157483365532978 | 13 s | 0.45 | Grey studio, one photoreal subject or object, big italic serif headline; motivational |
| r4 | pinterest.com/pin/1147643917677607792 | 28 s | 0.28 | Hormozi-style breakdown: cut-out real photo, grid paper, 3D brain/eye, bold + serif mix |
| r5 | pinterest.com/pin/1086986060090051457 | 40 s | 0.29 | Sepia archive collage (desk, old photos, newspaper, wax seal); "the zipper nobody cared about" |
| r6 | pinterest.com/pin/797911259025931429 | 30 s | 0.36 | Real-face cut-out on paper-doll body inside photo/painted collage sets (big-head look) |
| r7 | pinterest.com/pin/678214025173437276 | 15 s | 3.9 | Political poster collage, flashing cuts, music only |

## What they share (the style to take)
- **Picture:**
  - Photoreal, cinematic stills in a muted palette (sepia, warm grey, desaturated). One accent colour only (red/orange).
  - Lots of empty space around one centred subject.
- **One subject per shot:** a person, or a single object that floats with a real shadow (pocket watch, brain, boots, coin). Objects carry the idea (r3 "the timer" is a watch on a chain).
- **Type is part of the picture, not a caption box:**
  - Elegant serif, often italic, 1-4 words.
  - Sits above the subject and appears word by word on the voice.
  - Key word in the accent colour or a heavier weight (r5 "Still nobody cared.").
- **Motion:**
  - The picture never stops. A slow push or parallax runs inside each shot: 18-55 % of frames are still, the rest move.
  - Objects drop or slide in on the word.
  - A new shot every 1.2-3.5 s (0.3-0.8 cuts/s). r7's 3.9 cuts/s is the outlier.
- **Story shape (r5, r2):** a dated, concrete story told in short sentences. "Invented in 1851. Nobody cared for 70 years. Then World War I hit."
- **Characters (r6, r4):** real faces cut out and put on small paper or illustrated bodies, so they're recognisable but silly. Our toon cast with faces drawn like the real people does the same job, and the owner wants to keep it.

## Sound (measured; not checked by ear: earshot is not installed)
- **Narration is non-stop:** 133-180 words/min (r5 slowest, r2/r4 ~180), short punchy sentences.
- **No silence:** 0 % of the time under -45 dB.
- **Music bed under the whole clip:** level spread only 9-16 dB.
- **Loudness:** -14.1 to -14.8 LUFS (r3 -17.1).
- **r6 and r7:** music-only (r6 a rap track, r7 a beat). Not our case: เล่า Business keeps Safe's voice.

## How it maps onto เล่า Business (proposal)
- **Keep:**
  - The toon cast with faces like the real people (owner's point).
  - Safe's voice, the story structure and the lower captions (REF_SPEC 56).
- **Change:**
  - **Sets:** photoreal, muted, cinematic plates (Codex, new locked style paragraph) instead of the bright clean office. Mixed media like r6: toon characters standing in photo-like sets.
  - **Titles:** italic serif words on the beat (r3/r5), not pills or tags. One accent colour (brand orange) for the key word.
  - **Proof objects:** one floating object per idea with a soft real shadow (a stock certificate, a cheque, a bell, a stopwatch), instead of many props.
  - **Camera:** a slow push on every shot, plus an object or word arriving on the voice.
  - **Music:** continuous and a little more present than EP02's very quiet bed (EP02 sat ~-29 dB under the voice; these refs keep the bed audible all the way through).
