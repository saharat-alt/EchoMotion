#!/bin/bash
# EP02 music bed v7. Until the Envato pick is approved and downloaded (REF_SPEC 67), the bed is the track already on disk that
# earshot ranks closest to the owner's refs r2/r5 ("inspirational corporate background music, pizzicato strings"):
#   Kevin MacLeod "Investigations" (incompetech, CC BY 4.0, REF_SPEC 32): rank z +3.3 strong, cos 0.46 / 0.42 to r2 / r5 audio
#   (For Documentaries: z +2.3 weak, cos 0.29 / 0.27; the owner called it bad).
# Restart on the flashback (8.24 s) so the track's own ending lands on the end card and its last note closes the clip.
# Compressor: the piece has rests; 1 s loudness std 3.56 dB -> 1.9 dB (REF_SPEC 64 wants a steady bed, < 1.5 dB).
cd "$(dirname "$0")/../../.."
M=library/audio/music/incompetech_kevin-macleod_investigations.mp3
ffmpeg -v error -y -i $M -i $M -filter_complex "[0:a]atrim=0:8.24,afade=t=out:st=8.06:d=0.18[a];[1:a]atrim=0:93.5,asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1,acompressor=threshold=-28dB:ratio=4:attack=20:release=400:makeup=6,apad=whole_dur=100.43,atrim=0:100.43[o]" -map "[o]" -ar 48000 -ac 2 jobs/type3_story/2026-11-22_anthropic_ipo/out/music_bed_v7.wav
