---
name: product-film-3d
description: Make premium, minimal, "3D studio" product commercials (stills and 10–15s videos) with Nano Banana / GPT Image keyframes and Seedance 2.5, learned from real client work. Covers studying a reference commercial, translating it into a brand's own world, the edit-the-reference image chain, real-product layout composites, falling-ingredient shots, macro drops, label macros, base views, liquid pours and fizz, and video built from an untimed image library plus our own grey clay blockout (never third-party footage). Use whenever the user wants a product/bottle/cosmetic/drink commercial, hero shots, ingredient shots, "3D render look, not AI", a reference ad recreated for their brand, or a Seedance product film.
---

# Product Film 3D: premium product commercials that don't look AI

Load `cinema-director` too (house rules, Director's Camera block). This skill is the product-film workflow that was proven on real jobs: a non-alcoholic spirit (bottle, glass, botanicals) and a skincare oil (dropper bottle, cactus, seeds).

## 0. Non-negotiables (each one cost a failed generation)

1. **Never spend credits on reference or mood images on your own initiative.** References come from the client's real imagery or the user's screenshots. Generate only when asked.
2. **Never upload third-party footage as `@video`.** Seedance on Higgsfield rejects it as "Protected content detected", even greyscale and blurred. Rebuild the motion as **our own clay blockout** (`scripts/blockout_scene.js`).
3. **Never tie an image to a shot or a timestamp in Seedance.** "SHOT 3, 4.5–7s (@image3)" turns the image into a keyframe: the shot starts frozen on it and skips the motion into it. The video drives the timeline; images are an **untimed library**.
4. **Don't describe a reference you can edit.** If a reference already has the look, make it the edit base (attach it first) and change only what must change.
5. **One concern per edit pass.** Stack passes: composition → action → colour/texture → product.
6. **Never scale by a multiplier** ("1.3× bigger" overshoots to a giant pasted product). Pin size to the frame ("height about two fifths of the frame height") or composite the real product yourself (`scripts/layout_composite.py`).
7. **Premium = one hero material + few accents, falling, with empty space.** Never "burst", "explode" or "swirl around"; never six ingredient types in equal parts.
8. **No render-engine words, no IOR numbers.** They pull toward glossy stock CGI. Write photographic terms: distance, focus, light quality, falloff, grain.
9. **About one shot per 2–2.5s per Seedance pass.** Six cuts in 7s failed.
10. **Text:** the only text is the product's own label "reproduced exactly as in the attached product images, never mirrored and never altered". Big letters render; tiny back-label text garbles (fine in motion, keep it soft).

11. **The reference frame goes in FIRST on every generation and every fix pass,** in greyscale, scoped "CAMERA AND COMPOSITION AUTHORITY ONLY". Without it the model pulls the camera back and centres the product. A fix pass that drops it loses the framing that was already right.
12. **Scope every change to exactly what the user named.** "Make the bottom translucent" means the bottom only; the sides stay as the real product. Before sending, repeat the user's words back into the prompt and list what is PROTECTED.
13. **Research the real ingredients before choosing elements** (label, INCI list, site). The best element is usually the product's own source in its most beautiful form: its blossom petals, its seed, its oil drop. Never a mixed "ingredient salad".
14. **Every hero frame needs one director's idea, not a literal staging of the brief.** The idea tells the brand story in one image: the drop as a lens holding the source plant upside down; backlit gold against the brand colour in darkness; forced perspective. Frame only the action (no ground plane or table unless it plays a part), and let references set proportion and materials, not layout.
15. **I can't see outputs from the cloud container** (cloudfront is blocked). So the self-critique has to happen BEFORE sending: run the §1.3 pre-flight on every prompt, and offer two distinct concepts per round when the shot is creative.

## 1. Workflow

```
1 STUDY  reference commercial → contact sheets → shot list with timings (scripts/motion_study.sh)
2 BRAND  research the brand; translate the reference look into the brand's own world
3 FRAMES one keyframe per shot (Nano Banana 2.1, 4K, thinking High). Approve the first, then it is
         the LOOK AUTHORITY attached last on every other frame
4 FIX    one-concern edit passes; layout composite for product placement
5 BLOCK  render a clay blockout of the camera choreography at the final runtime
6 VIDEO  Seedance 2.5 multi-reference: @video1 = blockout, images = untimed library
7 CUT    if one stretch fails, regenerate only that stretch and splice it in; add sound
```

### 1.1 Study the reference
- `scripts/motion_study.sh ref.mp4 out "4.8 6.3 11.5"` gives a 2fps contact sheet plus full-res frames and greyscale versions.
- Make fine sheets (6–8fps) around every cut to read the real motion: direction of travel, what falls, where the product sits, how big it is and how it is occluded.
- **Use greyscale frames as composition references for images** (they carry framing, not colour or logos). Crop picture-in-picture insets to their own frame.
- The reference's premium feel usually comes from: a **monochrome world** (backdrop, light and product share one colour family), soft wrapping light, wafer-thin focus on material texture, one material per shot, lots of empty space.

### 1.2 Translate to the brand
Research the brand (search results, product photos, label). Pick:
- **World colour.** Either the product's colour family (a honey-amber studio for an amber spirit) or the brand's shoot surface (warm sand / Marrakech plaster for an oil shot on raffia), with the **label colour as the one strong colour**.
- **Ingredients.** The real ones from the label or the story. One hero (seeds for a seed oil) plus 1–2 accents.
- **Canon only.** Don't invent equipment or process ("a copper still" is not their tool). Ask or keep it symbolic.

### 1.3 Pre-flight: one-go checklist (run it silently on every image prompt before sending)
1. **Reference:** is the matching reference frame attached FIRST (greyscale) and scoped to camera, angle, orientation and fill? Is the real product photo attached? Is the approved look authority attached LAST?
2. **Framing in words:** have I stated the camera distance and how much of the frame the subject fills ("fills the bottom half and runs off the edges"), the angle (low / grazing / profile / worm's-eye), and where the subject sits (third point, cropped by which edge)?
3. **Idea:** what is the one cinematic idea of this frame? If I can't say it in one line, the frame is basic. Would a commercial director present it?
4. **Scope:** for an edit, does the prompt change ONLY what the user named, with a PROTECTED list? Is it one concern per pass?
5. **Product truth:** the real shape (square vs round), real label text "exactly as in the attached product images", real oil colour, real ingredients only?
6. **Premium:** one hero material, empty space, downward fall, real scale (drop ≈ tip width, lentil-sized on a surface), pale tint, low contrast, nothing over-sharpened?
7. **Banned:** render-engine words, multipliers, "burst/explode/swirl", ground planes that add nothing, a hand unless asked, other brands?
8. **AI tells (§3.3), for video:** is every readable text large and front-facing, and every small label turned away or blurred? Is the side copy hidden? Are collisions and weight written for particles? Are refractions described as optics? Is it shot-by-shot for the edit, not one generic pass?
9. **Credits:** generate only what the user asked for. Two models (Nano Banana 2.1 + GPT Image 2.5) for a label-heavy or uncertain frame; two concepts only for a creative open brief.

## 2. Image recipes (Nano Banana 2.1, 4K, thinking High; GPT Image 2.5 at 2K High for a label-heavy fix)

**Attachment pattern for every keyframe:**
- The GRAY composition ref is NEVER optional: attach it first on every generation and on every fix pass, scoped as "CAMERA AND COMPOSITION AUTHORITY ONLY: copy its camera distance, angle, orientation and how much of the frame the subject fills". Without it, the model pulls the camera back and centres the product.
- `[GRAY composition ref]` → `[product photo(s)]` → `[ingredient photo]` → `[approved look authority, LAST]`.
- Scope each one: "WHAT EACH ATTACHED IMAGE CONTROLS … Nothing else from it."

**Look-authority line** (paste after the NO ON-SCREEN TEXT block):
```
The last attached image is the LOOK AUTHORITY: match its <studio background>, its soft wrapping light, its <liquid glow / material> and its clean real-render finish exactly, so this frame belongs to the same commercial.
```

**Finish line** (end of every image prompt):
```
A premium studio product render, indistinguishable from a real photograph: physically accurate <glass, liquid, paper, metal>, a shallow focus on <subject>, a creamy falloff, low contrast and fine natural grain. Clean and understated: nothing over-sharpened, no warped text, no plastic sheen.
```

### Recipes that worked
| Shot | Base / method | Key words |
|---|---|---|
| **Pour hitting ice** | Edit a real pour photo: pass 1 swap vessel + colour + backdrop, pass 2 add impact and bubbles (turbulence ref second), pass 3 restore colour depth and micro-bubbles | "same real photograph", "frosty cloud of pin-point micro-bubbles", "clusters with gaps", "no splash crown" |
| **Fizz macro through the glass** | Edit the macro ref and change **colour only** (no glass ref attached); add ribs as a separate pass | "lens pressed against the glass wall", "milky high-key haze", "low contrast", "wafer-thin focus" |
| **Label macro** | Build the base from the REAL product photo (cut, rotate onto the diagonal, crop tight, fake focus falloff), then edit with "keep every letter". Never recreate from a ref of a different-shaped bottle (round leaks into square, text garbles) | "label on a strong diagonal", "paper tooth", "pigment granulation", "glass beyond is smooth, clear, polished, no texture" |
| **Base from below** | Recreate the GRAY composition; if the angle is wrong, use the ref as base again | "camera looks almost straight up into the base", "base faces the camera almost head-on", "plain glass, no embossing" |
| **Macro drop** | Recreate the GRAY composition | "lentil-sized, one twenty-fifth of the frame's width", "slightly flattened dome", "pale tint, never deep orange, never glowing", "one tiny highlight", "soft contact shadow" |
| **Falling ingredients + product** | Edit the COLOUR reference frame itself (swap every petal for an ingredient, same position, size, blur), remove its product, then composite the real product (`layout_composite.py`), then blend | "falling downward like a gentle rain", "nothing bursts outward", "bottom third calm and empty" |
| **Hero close-up** | Recreate the GRAY composition, with a few ingredients only | "neck cropped by the top edge", "label centred and sharp", "plenty of calm, clean space" |
| **Dropper hero (drop leaving the tip)** | No ground. Extreme macro on the pipette tip; references for proportion and glass only. Concept A: the drop is a lens holding the source plant upside down, on a brand-colour wall warming to gold. Concept B: side profile, the drop just pinched off with a satellite droplet, backlit gold on deep brand-colour darkness | "thread finer than a hair", "drop as wide as the tip's outer diameter", "tiny trapped air bubble", "thin bright rim of light", "no ground, no leaf" |
| **Falling petals + product (botanical oil)** | Reference falling frame GRAY first; the pieces are the source plant's own blossom petals (one colour family), plus a few oil drops and seeds | "single thin silky petal", "translucent where the sun passes through", "falls gently downward like a slow rain", "two fifths of the frame height" |
| **Intro bottle in darkness** | Edit the product's own studio photo | "three precise touches of warm light", "thin crisp highlight along the top edge", "near-total darkness" |

### Product placement when words fail
The model keeps the hero huge, centred and in front. Use this instead:
1. `python3 scripts/layout_composite.py --scene cloud.png --product product.jpg --crop x0,y0,x1,y1 --height 0.46 --angle 26 --cx 0.5 --cy 0.27 --out guide.png`
2. Make the guide the edit base: "The bottle is already in its final position, size and angle: never move, resize, rotate, redraw or reshape it."
   - Pass 1: the ingredient mix.
   - Pass 2: push the product back (relight to the scene, a touch of focus softness) and add 6–8 large blurred pieces in front, covering about a quarter of the product but never the wordmark.
3. Attach the real product photos in every pass.

### Failure → fix
| Symptom | Fix |
|---|---|
| Stock CGI whiskey ad (centred, all sharp, gel liquid) | Edit the look reference; photographic words; keep its distance, focus and light |
| Toy-like "baby bottle" pour | Crop in with forced perspective (POV over the shoulder, macro on the lip); anchor real scale |
| Giant resin-marble drop | Real scale, pale tint, flattened dome, calm surface |
| Cluttered ingredient explosion | One hero material, falling band, empty lower third, edit the ref frame |
| Wrong product size or angle after edits | Layout composite; never a multiplier |
| Reference look lost in an edit | Too many changes in one pass; change one thing |
| Background or texture leaked from the ref product (frosted glass, purple) | Name it: "smooth, clear, polished glass, no texture"; "no purple remains anywhere" |

## 3. Video (Seedance 2.5, multi-reference mode, never first/last-frame mode)

### 3.1 Build the blockout (our own motion reference)
- Edit the shot windows and camera paths in `scripts/blockout_scene.js` (pure `seek(T)`; clay placeholders: bottle, label band, base ring, petal or pad and drop, falling pieces, glass and table).
- Serve the folder: `python3 -m http.server 8766`, with three.js in `./node_modules/three`.
- Render: `node scripts/blockout_capture.cjs frames all` (headless Chromium with SwiftShader: about 45s for 360 frames).
- Encode: `ffmpeg -framerate 24 -i frames/f%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p BLOCKOUT.mp4`.
- Match the reference: cut points, speed ramps (in code, `tau = t < 0.45 ? t*2.2 : 0.99 + (t-0.45)*0.35`), the same spin direction across a cut, and the full runtime including the ending.

### 3.2 Prompt spine (paste and fill)
```
A <N>-second luxury product film for <BRAND>, <product>, with the minimal, premium, calm finish of a high-end studio 3D product film. @video1 is a grey clay blockout previz of this film. Follow it for camera, timing and blocking only: its shots and their order, every camera path, its direction, speed and easing, every speed ramp, every cut point, where each object sits and how it moves, and the total length. Render every grey clay shape as the real materials, product and world shown in the attached images.

NO ON-SCREEN TEXT: … The only text is the product's own printed label, exactly as in the attached images, never warped, never mirrored, never altered.

READING THE BLOCKOUT. <clay shape → real thing, one line each>. Never keep the flat grey clay look. Everything becomes real.

THE IMAGE LIBRARY. @image1 to @imageN are reference material, not frames. They show what everything looks like: <list>. Use them for look, materials, product, light and colour, while @video1 decides how everything moves and when each shot begins and ends. No shot starts or ends frozen on an image; every shot moves continuously from its first frame to its last.

THE PRODUCT. Exactly one <bottle> whenever it appears, identical to the attached images: <shape, glass, cap, liquid, label>. In <shot A> and <shot B> it spins in the same direction and orientation, so the cut is seamless. No hand, no person.

[Director's Camera & Composition] (cinema-director §3.3b, with @video1 as the choreography)
LIGHT AND COLOUR / PHYSICS / AUDIO (no music, specific foley per beat) / FINISH (no clay, no warped text, no plastic liquid, no jitter)
```
**Attach:**
- `@video1`: the blockout.
- `@image1…`: the approved keyframes plus 1–2 clean product photos (for label fidelity), in any order.

## 3.3 AI tells a viewer will point at, and how to kill each one
A viewer who knows 3D and film will pick a generated spot apart on these six points. Every video prompt and every edit must answer all six.

| Tell | Why it happens | Fix |
|---|---|---|
| **Small type turns into squiggles** (the label in a wide shot) | The model redraws text every frame; it only stays clean when it is large on screen | Text is either LARGE (the label at least a third of the frame height, facing the camera) or NOT READABLE BY DESIGN: in wide shots the bottle turns its plain side or back to the camera, or the label is lost in deep blur or silhouette. Never a small, sharp, readable label. Generate label shots as their own single-shot pass |
| **Side or back copy half-legible** | Secondary text panels get invented | Only the front label face is ever seen sharp. A spin stops before the side copy faces the camera, or the side copy stays in deep blur; say "the side panels show only plain satin glass" if the real product allows |
| **Runtime is a model default** (exactly 5/10/15s) | The film is one generation, uncut | Never deliver a raw generation. Generate shots separately with heads and tails, cut them in the edit to the beat, and land on an editor's length (e.g. 9.6s, 12.4s), with a real end frame or logo hold |
| **Generic "premium ad" coverage** (soft hero moves, no hard cuts) | The prompt describes a genre, not a film | Every shot gets a specific idea and a specific camera decision (a locked macro, a rack focus, a speed ramp, a match cut, one moment of stillness, one moment of impact). Hard cuts on motion between separately generated shots. Vary the rhythm: some shots of 0.6s, some of 2s |
| **Particles don't feel simulated** (petals float plausibly but have no weight) | "Petals fall" gives a texture, not physics | Write the collisions: petals strike the bottle's shoulder and slide off along the glass, flip, catch on the collar, collide with each other and separate; big petals tumble and drift, small ones fall faster, oil drops fall straight and fastest; turbulence trails behind the moving bottle; a few come to rest. Fewer, larger pieces read more real than many small ones |
| **Glass is vague** (objects in or behind glass read as soft impressions) | Refraction is hard and the model fudges it | Describe the actual optics: what is seen THROUGH the glass, inverted, compressed and bent at the edges; a thick base magnifies; the edges go dark with total internal reflection; highlights are sharp, thin lines. Keep transparent props few, large and slow; avoid ice and citrus in motion unless they are the hero |

## 4. Platform notes (Higgsfield)
- Nano Banana 2.1 costs about 2 credits per image at 2K. Preflight with `get_cost`.
- Seedance on Higgsfield is "Protected content" sensitive. If flagged, test with fewer attachments to isolate the cause.
- Outputs on cloudfront can't be downloaded into the cloud container. The user's chat images arrive locally in `/tmp/.../images/`, and uploads land in `/root/.claude/uploads/`.
