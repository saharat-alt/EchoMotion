# SFX pack (earshot 1.0)

ทำด้วย `earshot make` ทั้งหมด (user 2026-11-24: ไม่โหลดซาวด์เอฟเฟกต์แล้ว) ของเราเอง ฟรี commit ได้
ใช้กับมิกเซอร์: `--sfx-dir library/audio/sfx_earshot` (มิกเซอร์อ่านโฟลเดอร์หมวดย่อยชั้นเดียว ชื่อไฟล์ = ชื่อ role ใน cues,
`_2`, `_3` = variant ที่วนสลับกัน). ทำใหม่ / เพิ่ม variant: รันบรรทัดในตารางด้วย `--seed` ใหม่
(`.venv/bin/python -m earshot make "<words>" --seed N -o library/audio/sfx_earshot/<cat>/<role>_N.wav`)
แล้ว `earshot realness` เช็กก่อนใช้

## transition/ — ทรานซิชัน (ตัดฉาก/ย้อนเวลา)

| file | earshot make | seed |
|---|---|---|
| rewind.wav | a tape rewind | 0 |
| swish_paper.wav | a quick paper swish | 0 |
| tapestop.wav | a tape stop | 0 |
| whoosh.wav | a soft fast whoosh for a cut | 0 |
| whoosh_2.wav | a soft fast whoosh for a cut | 1 |
| whoosh_3.wav | a soft fast whoosh for a cut | 2 |
| whoosh_4.wav | a soft fast whoosh for a cut | 3 |

## ui/ — UI (ป๊อป คลิก ตัวเลข ติ๊ก แจ้งเตือน)

| file | earshot make | seed |
|---|---|---|
| chime.wav | a soft bright notification chime | 0 |
| click.wav | a soft mouse click | 0 |
| counter.wav | twelve soft ticks 0.07 s apart | 0 |
| ding.wav | a notification ding `--sound notify/single --pitch C6` (เล่า Business: เสียง ding ตามเรฟ r2 0:13.92 / r5 0:34.87) | 0 |
| ding_2.wav | a glockenspiel note `--sound mallet/glock` (เรฟ r2 0:06.80, r5 0:19.70) | 0 |
| msgpop.wav | a chat message pop (เรฟ r2 0:02.22, r5 0:05.65) | 0 |
| msgpop_2.wav | a bubble pop (เรฟ r2 0:10.94) | 0 |
| pop.wav | a soft pop | 0 |
| pop_2.wav | a soft pop | 1 |
| tick.wav | a clock tick | 0 |

## impact/ — อิมแพกต์ (โลโก้ สแต็บ สเวล ไรเซอร์)

| file | earshot make | seed |
|---|---|---|
| logo.wav | a logo reveal hit | 0 |
| riser.wav | a riser building up into a title, 2 s | 0 |
| stab.wav | a short dramatic stab hit | 0 |
| swell.wav | a reverse swell into a hit | 0 |

## foley/ — โฟลีย์ (กระดาษ ปากกา ชัตเตอร์ ของในครัว โทรศัพท์)

| file | earshot make | seed |
|---|---|---|
| cup_place.wav | a cup set down on a table | 0 |
| dishes_sink.wav | dishes clinking in a sink | 0 |
| paper.wav | a paper page turn | 0 |
| paper_tear.wav | paper tearing | 0 |
| pen.wav | a pen writing a short stroke on paper | 0 |
| pencil.wav | a pencil scribble on paper | 0 |
| phone_ring.wav | a phone ringing | 0 |
| shutter.wav | a camera shutter | 0 |

## ambience/ — บรรยากาศ (ลูปพื้นหลัง)

| file | earshot make | seed |
|---|---|---|
| diner_walla.wav | a busy cafe crowd murmur | 0 |
