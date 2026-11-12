# Reference spec — what the refs actually do (measured 2026-11-12)

Source: frame-by-frame study of `D:\Downloads\REF\*.mp4` (scene detection at 0.18, 2 fps contact sheets, loudness).
These are the rules every render is checked against. If a pilot breaks one, it is not done.

## Shared (all 4 refs)

| Rule | Measured |
|---|---|
| A visual change every 1–3 s | r1: 6 shots / 12 s, r3: 13 / 31 s, r4: 11 / 12 s (0.25–2 s each) |
| What is on screen = **literally what is being said right now** | "meteor" → meteor; "Greece" → Greek flag + map; "Gemini" → Gemini logo; "$381 billion" → the number |
| Real content, not designed text cards | product UI, GitHub page, logos, photo cutouts, money, flags, maps |
| One focal point per moment | never two cards + captions + mascot competing |
| Music bed under everything, no dead air | 0 silences ≥ 0.25 s below −50 dB in all 4 refs |
| Loudness | −13.4 to −14.7 LUFS |
| Captions short | 1–3 words (r1/r2), 2–5 words (r3/r4) |

## Type 1 — talking head (คนพูด01, คนพูด02)

Three layouts only, switching on the beat:
1. **Speaker full** — caption 1–2 words, white with soft shadow, no box, at ~68–72% height.
2. **Split** — the insert takes one half, the **speaker is reframed into the other half (scaled/moved), never covered**. Face fully visible. Caption sits on the seam between the two halves. Insert half shows real content: product screen, logo, screenshot, photo with bounding box + label.
3. **Full-screen cutaway** 1–2 s — the insert fills the frame (blurred copy of itself behind), caption large; key word in a **different font** (serif italic) for emphasis.

Do not: put panels over the face, use boxed caption bands, keep a graphic up longer than the sentence it illustrates.

## Type 2 — news + mascot (AIพูด = Vox-collage, plus r1 cutaways)

- Each 1–3 s beat = a real visual: screenshot of the announcement/article, company logo, product UI, photo of the person (cutout on a textured flat-lay), the number as a physical paper card.
- Slow constant camera push/drift on every shot (nothing static).
- Big kinetic word behind or over the subject for the key phrase only (e.g. "THEN THE WHOLE COUNTRY"), small sentence-case caption at ~72% for the rest.
- Mascot = small narrator in a corner (lip-sync), not the main subject; it must never sit on the key visual.
- Sources shown small on screen where the screenshot appears.

## Type 3 — story animation (Animationเล่าเรื่อง)

- Flat 2D, few shapes, round-head characters, warm paper palette; **one idea per shot**, illustrated literally.
- A persistent on-screen device that carries tension (the countdown pill at top).
- Captions: ALL-CAPS-style bold white with dark stroke, 2–5 words, keyword in yellow, sitting at the character's chest height (~65–70%).
- Simple camera: push-ins, a car drive with speed lines, thought bubble for flashback, light cone in the dark.
- Ends on a cliffhanger card ("TO BE CONTINUED / PART 2 SOON").
- For Data Echooo: same grammar, brand palette, mascot can be the narrator/host; 2.5D = these flat layers with parallax depth, not a 3D city.

## What our pilots got wrong (user review 2026-11-12)

- News v2: text cards held 5–12 s instead of real news visuals changing every 1–3 s; no music; mascot too big for a narrator.
- Talking head v1: split panel and caption band covered the face; three things on screen at once; no clear focus.
- 3D test: abstract data-city does not illustrate the sentence; nothing to "read" in 1 s.
- Mascot mouth: overlay carried chin/glasses fragments that showed as a dark line when squashed. Fixed (`engine/tools/split_mouth.py`).

## Craft rules distilled from the skills (video-studio, cth9191/animate, lemo-opuscar, mg-styles-15, video-editor-skills)

Shared
- Hook: frame 0 moving with sound, first line by 0.2 s; no logo/channel name in the first 2 s.
- Safe zone 1080×1920: important things inside x 60–940, y 250–1500; nothing important below ~1250 except the caption.
- Captions: one line, 2–5 words (Thai ≤ 20–25 chars), 84–88 px, top near y ≈ 1060–1200; ≤ 3.5 words/s; never split a number from its unit.
- Thai: animate by word, never by character; use the script text aligned to audio rather than ASR text when a script exists.
- Something new every 2–4 s; nothing flat > 1 s; strong action within 0.5 s of each cut.
- Sound: music bed −20 to −25 dB under voice (duck 12–18 dB); whoosh peaks on the cut, impacts on the hit, never on a key word; at least one real silence before the payoff; master −14 LUFS, TP ≤ −1 dB measured on the MP4.
- QA: contact sheet every 1–2 s, blackdetect, watch once at full speed with sound; score 1–10 on a rubric, aim for 9.

Type 1 talking head
- Cut from word timestamps; remove pauses > 0.35 s; handles −0.08 / +0.12 s; 5–10 ms audio fades.
- Jump cuts alternate 100% ↔ 107–112%; punch-in 115% only on the punchline; B-roll opens at 100%.
- The face box stays visible during every overlay; overlays never enter the caption band.
- Full-frame BigWord cutaway: one idea, 1–2 s, the speaker's own words.

Type 2 news
- One fact per screen: what → how big → who said it → verdict.
- A number is first shown highlighted in the original document, with its source tag in the same shot.
- Never stronger than the source; real product UI only; logos never covered.
- A package action every 0.5–1 s (push, highlight, stamp, count); documents hold 3–4.5 s, footage 1.5–3 s.
- Transitions: hard cut, 1–2 frame flash, 0.18 s slide-in, 0.3 s punch-in. No dissolves, no 3D flips.
- Mascot small, helper not hero; idle life (blink, bob).

Type 3 story
- One constant hero in the same place; one device (countdown) you can say in a sentence.
- Show the idea, don't label it; vary shot size; every cut has a reason.
- Flat motion: overshoot ease, 2–4 frame staggers, ~10% squash; one subject moves at a time.
- Pop captions 0 → 1.15 → 1 in ~8 frames; fill + thick white stroke + coloured outer stroke.
- Approval order: story → 2–4 style frames → storyboard → animate.

## User corrections (2026-11-12) — hard rules
1. **Never cover the speaker's face.** Reframing follows the face track (`engine/tools/face_track.py`, YuNet); captions in a split sit inside the insert panel, not on the speaker.
2. **The mascot is a bust, so it is always cut by a frame edge** (enlarged, pinned to a corner/bottom edge like a facecam). Never a cut-off torso floating mid-frame with a floor shadow.
3. **Inserts are real content** (the actual article, official footage, logos, quotes from named companies) that match the words being spoken — not designed text cards.
4. **Make sense first:** before rendering, ask of every frame "would a real editor put this here?" Check contact sheets at full size for artifacts (e.g. the cut mark under the mascot's mouth).
5. **News = report the source as written.** No opinion, no stronger wording, keep qualifiers ("about", "with human guidance", "earlier version"). Our ideas/use-case suggestions are allowed only in the "examples worth trying" part and must be framed as ours.
6. **Third-party media is fine as fair use** (news videos, X posts, screenshots) — always show the credit on screen (@handle / outlet), never present it as ours.
7. **Never say the same thing twice at once.** If the caption says it (a date, a number, a phrase), no stamp/chip repeats it. Graphics add what words can't: the highlighted source line, a ring on the exact chart point, the winning bar. Section label = small pill ("1/3 · เขียนโค้ด"), not a big chip.
8. **Sound is sparse and role-based** (v4 had 42 hits/min from 4 samples — repetitive): explicit cut sounds only at section changes (whoosh / shutter for screenshots / riser into a list / chime on CTA), soft marker on highlights, pops only for list items. Round-robin variants + ±4 % pitch so no hit repeats exactly. Target ≈ 15–20 cues/min.
9. **Balance:** music 12 dB under the voice in gaps, a gentle 4 dB duck (0.3 s attack / 0.8 s release) under speech — v4 had music 28 dB under (inaudible, then pumping). Master −14 LUFS on the MP4, peak ≤ −1.5 dBFS.
10. **News order:** tell the news completely first (what launched, what changed, numbers, price, who can use it, where), THEN "ideas to build on". Never jump from the headline straight into use cases.
11. **Type 2 look = editorial halftone paper collage** (ref AIพูด.mp4; method from pyang5166/gbro-collage-broll, MIT): black-and-white halftone cut-outs, flat bold colour field, coloured cardstock accents, cream keylines, paper grain + soft shadow, assemble-from-empty motion (pieces arrive and build the picture), not slow drift/zoom.
12. **Sound QA with earshot** (C:\earshot\.venv\Scripts\python.exe -m earshot critique <mp4>). v5: "close", 20/23 in range; fixed stereo + voice 2.5 kHz −2 dB + softer small hits. Its reference set is music-led launch films (no voice-over), so "salient hits" also counts TTS syllables — read that metric with care. After use, delete today's per-file cache in C:\earshot\.cache\decoded and emb\{ast,clap,launch,realness,timeline,video}; keep .cache\hf (models).
13. **Speak like a person, never narrate the structure** ("ข่าวครบแล้ว", "มาถึงช่วง…", "เอาไปใช้อะไรได้บ้าง?" are out). Bridges slide in naturally, e.g. the user's own line: "ลองมาดูสามไอเดียที่น่าสนใจสำหรับ Fable 5.2 กันบ้าง". Run scripts through thai-humanizer and read them aloud before TTS.
14. **Paid services:** ElevenLabs = voice only (TTS + Scribe for timing; music/SFX were approved once). Images = Codex CLI (codex-dispatch skill). Any other paid generation: quote the cost and get the user's yes first.
15. **Calm entrances (user review):** no fly-in from off-frame, no spin, no bounce. Pieces rise ~60 px + fade over 0.45 s ease-out; captions fade (0.22 s) with a 4 % settle. Leave reading time: a piece should be still for most of its shot.
16. **Background = one physical desk per section** (Codex-generated flat-lay plates), camera moves continuously across it; content sits on cream paper sheets; brand colours only on small pieces. Never switch full-frame solid colours every shot.
17. **Backgrounds (final approach):** one themed plate per beat in a locked CI collage style (cobalt / cream / orange, torn paper, halftone props around the edges, calm centre), generated with Codex CLI from a single style paragraph + per-beat props list (method: seergioo_gil Vox-collage post). Slow push per plate; plate changes on the beat. Take the ref's mood, tone and cutting rhythm — never copy its exact look.
18. **Brand marks are never altered:** use official logo files in their official colours (e.g. Claude coral mark, AWS, Google Cloud multicolour, Azure) — Wikimedia Commons originals; never a monochrome icon-set version recoloured to black, never stretched or restyled.
19. SFX (user, 2026-11-12, on v6n): "not varied, no whoosh". Every cut gets a light whoosh (−15 dB, 4 real variants), every visual event its own role sound (paper on docs, pen on highlights, counter + pop on numbers, click/pop on cards, logo pop, shutter on clips, swish on photos). Real recordings from Artlist (library/audio/sfx, LICENSE.txt), not code-made blips. Still under the voice.
20. Music (user): instrumental funk, fun and tight, NOT airy/corporate, steady loudness (little dynamics). Pick by measuring 1 s loudness std (≤1.2 dB) + earshot rank, then let the user choose. Type 2 uses Ariel Shalom "Groove Express" (Artlist) from 0:42.
21. Visual must land with the word: numbers and their labels appear on the spoken number (check word times; numerals like "$40" do not auto-align to Thai "สี่สิบ", pin them with caption_starts). Hold the shot until the label is readable.
22. No white flash transitions: a 3-frame flash reads as a flicker/glitch. Hard cut + whoosh instead.
23. Mascot = type 2 (news) only. Type 3 (story) never shows it; its end card uses the story cast + logo + orange follow button. Type 3 takes the ref's format and pacing but our mood/colours (bright ice-white sets, cobalt main colour, sky/teal accents, one orange touch).
24. Music level (type 2 v7 review): "music a bit too loud". Default bed −15 dB under the voice in gaps, −6 dB extra duck while talking (music ≈19 dB under the voice).
25. Folders/finals: jobs split by type (type1/2/3); all sounds into library/audio for reuse; on "final" delete every unused draft (tools/finalize_job.py, dry run first).
26. The voice must match the sample the user approved. Paxa per-line calls drift; generate the script in one call and compare pitch with the approved sample.

27. Providers (user, 2026-11-12): ElevenLabs is used through the Claude connector (creative_generate_speech + creative_transcribe_audio), not an API key; still voice + word timing only. Music for new jobs comes from Envato Elements instead of Artlist: the connector only searches, the user downloads the chosen track with their own Envato account into library/audio/music/envato_<artist>_<title>.wav (never committed). Reason: the team works through Claude connectors and has Envato, not Artlist. The baseline finals keep their Artlist tracks for rebuilds; SFX stay the repo library.
28. Clip type names (user, 2026-11-12): type1 = "เซฟพูด", type2 = "เล่าข่าว", type3 = "เล่า Business". Display names only; ids type1/2/3 and folder/file names stay, because tools/rebuild.py, providers.json bundles and brand.json voices.by_type use them.
29. Real photos (user, 2026-11-12): "use real photos too" for เล่า Business and เล่าข่าว. Reason: drawn-only (type 3) and text-only (type 2) visuals feel less credible. Type 3: `photos` in story2d.html = white-bordered proof print on key beats (~1 per 3-5 shots), beside the cast, never over a face, label replaces the name tag, credit on screen. Type 2: at least one real photo per section (person / product / event / company) in natural colour. Sources in order: Wikimedia Commons (free licence), official press / source article (fair use, rule 6), Envato Elements for generic scenes only (no named people or brands there). Every photo: on-screen credit + CREDITS.txt line with licence and author.
30. Voice (user, 2026-11-12): every clip type uses the ElevenLabs voice "Safe" (voice_id DMKLUh0ZCBM4EXh5Kggs, คุณเซฟ's own cloned Thai voice) through the connector, set in brand.json voices.by_type for type1/2/3. Reason: the channel should sound like its owner, not a library voice. Aidan stays only to rebuild the three baseline finals. On the first Safe job, approve a short sample and keep it as the reference take (rule 26).
31. English words in a Thai accent (user, 2026-11-12): English terms are spoken the Thai way (as คุณเซฟ says them), never with an English accent. The TTS text spells them in Thai (glossary brand/pronunciation_th.json, applied by tools/th_say.py, which also flags any Latin word, digit or symbol left); captions keep the English spelling. New words go into the glossary so every job says them the same way.
32. Free music is fine (user, 2026-11-12, jensen_affair job: "ลองหาฟรีๆ มาเลย"): when Envato is not available, use a free licensed track instead of mixing without music. Reject any track marked "Content ID Registered" (all four Pixabay picks were: a YouTube/Facebook upload would get a copyright claim). Kevin MacLeod / incompetech (CC BY 4.0, credit in the post caption) worked. The ElevenLabs Claude connector cannot make music (voice only). Pixabay blocks scripted downloads.
33. Finals folder (user, 2026-11-12, with a screenshot of the layout they want): ONE flat folder deliverables/final/ for every finished clip, two files per clip: EPxx_<Thai title, no spaces>.mp4 and EPxx_ปก.png (EP numbers run in order of finishing; EP01 = the Jensen Huang clip). Nothing else goes in there: the post caption stays in the job folder. Cover = real photo of the subject + one big question in Kanit on a brand-blue block + orange type pill, made by the job's make_cover.py.
34. Scripts can run long when the story needs it (user, 2026-11-12: "ยาวได้ ถ้า storytelling ดี"): the jensen_affair final is 2:11. Every beat must answer the question the viewer has right then; cut stretches of stacked numbers instead of cutting the explanation. A story about a live news event ends with a conclusion in the same clip ("จบในตอนเดียว"), not a part-2 tease.
35. ElevenLabs connector estimates for Scribe (creative_transcribe_audio estimate_only) come out far too low (36 credits estimated, 643 charged for 117 s). Quote about 5.5 credits per second of audio instead, and say the estimate is unreliable.
