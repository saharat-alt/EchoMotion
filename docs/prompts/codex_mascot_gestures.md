# Task: mascot "Safe" extra gestures + mouth sheet (image generation)

Generate the images below with your image generation tool. Save each as PNG in `out/mascot/` with exactly the given name.
The attached images are the character: `base_wave.png`, `base_thumbs.png` (same character, two poses) and `Safe_Cartoon2D.png`.
Every new image must look like the SAME character drawn by the same artist: same face, hair, glasses, shirt, line weight, colours.

## Locked style (use verbatim at the start of every pose prompt)
Chibi-proportioned 2D cartoon bust of the same young man as the reference images: brown messy short hair with warm highlights,
round black glasses, big brown eyes, soft pink blush, plain black crew-neck T-shirt. Clean dark-brown outline, soft cel shading,
slightly textured warm skin. Front view, centred, head and shoulders down to mid-torso, the body cut by the bottom edge of the image.
Same head size and head position as the reference: the head fills the upper half, the face is centred horizontally.
Mouth closed in a small relaxed smile. Hands have five clean fingers, simple cartoon shapes.
Plain flat pure white background (#FFFFFF), no shadow on the background, no props unless listed, no text.
Portrait image, 2:3, at least 1024 px wide.

## Poses (one image each; only the arms and hands change)
1. `pose_point_up.png`: right index finger pointing straight up beside his head, left arm relaxed at his side.
2. `pose_point_side.png`: right arm stretched out to the viewer's left, open palm up, presenting something next to him.
3. `pose_explain.png`: both hands in front of the chest, palms open and slightly apart, as if explaining.
4. `pose_count_1.png`: right hand raised at shoulder height, showing ONE finger.
5. `pose_count_2.png`: right hand raised at shoulder height, showing TWO fingers.
6. `pose_count_3.png`: right hand raised at shoulder height, showing THREE fingers.
7. `pose_shrug.png`: shoulders up, both palms up at waist height, a shrug.
8. `pose_wow.png`: both hands up near his cheeks, fingers spread, surprised eyebrows (mouth still closed).
9. `pose_chin.png`: right hand on his chin, left arm folded under it, thinking.
10. `pose_arms_crossed.png`: arms crossed over the chest, confident.
11. `pose_ok.png`: right hand making an OK sign near the shoulder.
12. `pose_hold_card.png`: both hands holding a blank white card in front of the chest, card facing the viewer, card about 1/3 of the image width.
13. `pose_phone.png`: right hand holding a smartphone up beside his face (not covering it), screen facing the viewer, screen plain white.
14. `pose_bye.png`: both hands waving at shoulder height, a big friendly wave.

## Mouth sheet (one image)
15. `mouth_sheet.png`: the same character's mouth only, eight mouth shapes for lip-sync laid out in a 4 x 2 grid on plain white,
    each shape the same size and line weight as the mouth in `base_wave.png`, evenly spaced, nothing else on the sheet
    (no face, no labels). Dark-brown outline, dark-red inside, small white upper teeth where visible.
    Row 1: closed gentle smile; lips pressed flat (M/B/P); slightly open with teeth just visible; wide open "aa" with tongue low.
    Row 2: wide flat "ee" showing teeth; round "oh"; small round pucker "oo"; upper teeth resting on the lower lip "f".

Acceptance:
- 15 PNGs with exactly these names in `out/mascot/`, portrait 2:3 (the mouth sheet may be landscape).
- The character is clearly the same person as the references in every pose; head the same size and place in every pose.
- White background, no text, no extra props beyond those listed.

Write only inside `out/mascot/`. Final answer: list of files with pixel sizes.
