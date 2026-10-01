---
name: cinema-director
description: "The unified cinematic prompt director. Merges Shotcaller (Seedance video), Motiondojo (Genjutsu motion transfer), Castkit (character references), Scenecraft (scene plates) and Story Bible Builder into one body of knowledge, so every prompt — video, motion transfer, character plate, scene plate or bible — uses the best technique from all five. Use this skill for ANY request to make a prompt, a shot, a scene, a character, a location, a first frame, a motion transfer, a dialogue scene, a lipsync, an extension, or a story bible. Load it first, every time; it tells you which verbatim templates to pull from the five source skills."
---

# Cinema Director — The Unified Doctrine

Five skills, one director. The source skills (`shotcaller-v1`, `motiondojo-v1`, `castkit-v1`, `scenecraft-v1`, `story-bible-builder`) hold the **verbatim templates** — the exact blocks and closes that must be pasted, not paraphrased. This file holds the **combined thinking**: how a prompt is planned, which technique from which skill strengthens it, and how the outputs chain into each other.

**Rule of use:** read this file, decide the output format, then open the matching source skill(s) for the verbatim blocks. Every prompt borrows across skills — a Seedance shot uses Scenecraft's composition planning and Motiondojo's individuality and population locks; a scene plate uses the bible's era palette; a Genjutsu prompt uses Shotcaller's dialogue system and lens table.

---

## 1. THE DOCTRINE (holds across every output)

1. **The model is a camera and a physics engine, not a mood board.** If a word doesn't produce a visible pixel or an audible sound, cut it.
2. **Write the visible.** Emotion as muscle ("shoulders lift, jaw locks, exhales through the nose"), never the emotion word. Speed in km/h, height in cm, mass in kg/tons, contact as deformation, direction labelled screen-relative or character-relative.
3. **References carry identity; the prompt carries what only words can say** — the moment, the motion, the camera, the light, the physics, the locks. Never re-describe what an attached reference shows unless it's load-bearing or drifts.
4. **Scope every reference.** When more than one is attached, say what each governs and what it does not ("controls geography, materials and light direction only"; "its flat lighting is not used"; "its silver finish is not used").
5. **Locks exclude as much as they include.** Every locked trait carries its "never" clause — `BROWN eyes, never blue`, `warm fair skin, never cool-shifted, never tan`.
6. **Never invent canon.** Missing a needed detail → ask. A guessed detail that renders becomes canon by accident.
7. **No lighting baked into references; all lighting lives in the scene.** Character plates are flat gray and shadowless; scenes do the lighting.
8. **Light is direction, quality, temperature.** Never a fixture. Every colour names a source in frame.
9. **Air is density, never shapes.** No fog, mist, smoke, haze banks, shafts, god rays, drifting particulate. Vapor only when something in frame emits it.
10. **Low macro contrast, high micro contrast.** Lifted blacks at every depth, razor texture in skin/fabric/stone/metal, grain heaviest in the shadows, bloom at point sources.
11. **Flattering realism.** Pores, peach fuzz, subsurface scattering — and never acne, blemishes, rough pores, plastic, wax, or glass-skin.
12. **Real time, real cadence.** 24fps, true 180° shutter, 1/48s exposure, genuine motion blur. Every shake is a real operator's weight, never broken footage.
13. **Silence is never neutral.** Every body in every beat gets an action; every listener gets "says nothing in this beat" plus what they do; every silence gets a duration and a sound.

### Universal house rules

No character names in a prompt (visual handles only) · no aspect ratio · no tool or platform names · age-blind · English only (non-English dialogue verbatim) · no negative prompt block — negations live inline · no lyrics, song titles or artists · no teeth-showing smiles unless asked · standalone (no "same as the last scene") · NO ON-SCREEN TEXT high in every prompt, never with a carve-out — in-world text is a physical object with shape, colour, material, placement and the exact words in quotes.

---

## 2. INTAKE — what to settle before writing

Read every reference first. Then settle, asking only for what can't be deduced (one compact question, not a quiz):

| Decide | Options | Source of the technique |
|---|---|---|
| **Output** | video shot · motion transfer · character plate · scene plate · story bible | — |
| **Target** | Seedance 2.0 (9 refs/15s) · Seedance 2.5 (50 refs/30s) · Genjutsu · Nano Banana Pro · Seedream 5.0 Pro · GPT-2 · other | Shotcaller, Scenecraft, Castkit |
| **Render** | photoreal (default) · animated (needs a style lock, verbatim every time) | Castkit |
| **Canon** | is a bible active? Pull voice / movement / stillness / era palette / locked traits from it | Story Bible |
| **People** | count, handles, screen positions, who's nearest the lens | All |
| **Mouth state** (every video) | closed · exact scripted words · follows attached track | Motiondojo + Shotcaller |
| **Camera register** | locked-off · gentle · heavy · violent handheld | Shotcaller + Motiondojo |
| **Runtime** | matches the motion video (Genjutsu) · within the version cap (Seedance) | Motiondojo, Shotcaller |

**Mouth state is decided for every video prompt, not only Genjutsu.** A silent Seedance shot gets the closed-mouth HARD LOCK sentence too — otherwise the model gives faces words.

---

## 3. THE COMBINED TOOLKIT

Each technique below came from one skill. All of them apply wherever they fit.

### 3.1 Composition planning (from Scenecraft — use in every visual output)

Plan silently on a 0–100% grid, then write positional prose. Never coordinates in the prompt.
- Subject on a third unless symmetry motivates centre. Horizon on the upper or lower third.
- **Foreground mass first**, then subject, then deep background.
- Lead room ahead of anything moving, never trail room.
- **Figures at different depths, never in a row.**
- **Resolution filter:** for every detail ask — would this lens resolve it at this distance? survive this motion blur? be visible at this light level? If not, cut it. A figure at 50m is silhouette, hair colour, wardrobe colour, posture. Detail is earned by proximity, stillness and light.

→ In video this becomes the **Geometry Map** (lateral position, depth plane per subject, vertical relationships, what's off-frame where, who the frame favours) and the **First Frame**. In plates it becomes paragraph 1.

### 3.2 Optics — degrees first, mm in brackets

| FOV | mm | Use |
|---|---|---|
| 107° | 14–16 | vast interiors, epic establish |
| 84° | 20–24 | full-body blocking, choreography, immersive action (Genjutsu default) |
| 63° | 28–35 | walking alongside, following one performer close |
| 47° | 40–50 | medium, two-shot, waist-up dialogue, upper-body motion |
| 34° | 60–70 | compressed group, stacked planes |
| 29° | 75–85 | isolated bust, hands, product hero |
| 18° | 100–135 | held emotional close-up |
| 12° | 180–200 | insert, object, texture |
| 8° | 300–400 | far observation |

- Lens lock per shot, no focal drift, no zoom — size changes by the operator walking.
- **Unusual FOVs get the defense battery** (WIDE: "NOT telephoto, no flattening… and no fisheye, no barrel bulge"; LONG: "strong compression, one face sharp at a time, NOT wide-angle, no deep focus").
- Video default glass: spherical large-format. Plate default: vintage anamorphic (spherical for editorial). Character plates: 50mm prime, flat.
- In plates, describe lens by feel in words; never equipment names.

### 3.3 Camera — one register, every move motivated

| Register | Cant | Cuts | Use |
|---|---|---|---|
| Locked-off | 0° | oner or 1–2 | stillness is the subject; precise symmetrical choreography |
| Gentle handheld | 3–10° | 3–5 at 2.5–4s | dialogue that matters, slow emotional movement |
| Heavy handheld | 12–25° | 4–6 at 1.5–2.5s | everyday action, mid-energy dance |
| Violent handheld | 15–45° | 4–6 at 1.5–2s | fights, high-energy choreography |

- **Dialogue defaults to locked or gentle** — a moving camera competes with the mouth.
- **Natural means motivated** (Motiondojo): every move comes from something a body does — charge in when a move lands, drop to ankle height on a foot plant, whip to the other performer and overshoot. The operator's footing reacts to the ground. Never a perfect orbit. Favour no one for long.
- Cant is a swinging range that never passes through level.
- Every non-locked register closes with the never-settles clause (never stabilized, never gimbal-glide, never floaty drone, real shoulder-mounted mass, every frame mid-move but continuous).
- A still subject inside a violent camera is stated as an explicit split.

### 3.4 Light & colour (Shotcaller + Scenecraft)

State: where the dominant light comes from relative to camera and subject · its quality (hard/raking, soft/wrapping, broad, pointed) · temperature and where two temperatures meet · what it catches and where it stops.
- **Three bands ~70/20/10, each tied to a source in frame.**
- **Night is mostly dark with hard sources cutting through.** Exterior: only sources that physically exist, no moonlight lift, figures read as silhouettes defined by edge light. Interior/urban: practicals drive a motivated warm-cool split. Never bright night, never teal flood.
- Skin renders true and warm where warm light touches it, never cool-shifted by the grade.
- On Seedream, a **HEX value** pins a load-bearing colour.
- **When a bible is active, the era's palette line is the starting point** for the light and colour block.

### 3.5 Atmosphere

A continuous scattering gradient from the lens to the farthest plane, **naming the actual planes nearest to furthest**, the foreground already carrying a whisper of air, blacks lifted at every depth. Scale the density: thin interior · moderate exterior · heavier night/weather/ruin — always density, never shapes. Wind is named by what it moves (hair across faces, sleeves flaring, scrub on the cliff). Vapor only with a source: a cigarette ribbon dissipating within 30cm, breath condensing, dust kicked by a footfall, steam off a cup.

### 3.6 Physics — the chain, rewritten for this ground and these clothes

**mass → contact → deformation → rebound → secondary lag → contact shadow → nothing floats, nothing slides.**
- **Surface-aware** (Motiondojo, applies everywhere): name how *this* surface answers *every* plant — pebbles shift and roll, sand gives and slides, wet concrete lets soles skid, grass compresses — and how the body absorbs it (ankles rolling and correcting, knees taking the landing). Name what gets kicked out behind each step.
- Hair and loose fabric lag every direction change and settle a beat late. Shadows travel with bodies.
- Effort, resistance, falling debris, structures that must hold — stated physically, never asserted.
- People in plates get the same: contact where feet meet floor, weight in the posture, height against the world ("the doorframe clearing her head by a hand's width").

### 3.7 Performance — faces, bodies, individuality

- **Brow matched to the line** is the highest-yield acting instruction. Natural blinking, active forehead, no mask-face, no dead eyes. Eyelines as stated targets; never into the lens unless asked.
- **Muscles, never emotion words** (Castkit expression sets): "brows drawn together and down at the inner ends, upper lids lowered a fraction, mouth corners pressed level, jaw set."
- Emotional arcs are slides, not states.
- **Four motion layers live at all times:** character · micro (breath, hair, fabric, jewellery) · environment · camera.
- **Individuality — for ANY multi-person video, not only Genjutsu:** two people doing the same thing get contrasting movement qualities (one behind the beat, weight low, generous follow-through; the other ahead of the beat, hits and stops dead). Different knee bend, torso angle, shoulder carriage; head snaps, breath and micro-stumbles land at different instants; silhouettes never match. In unison: same shape, own micro-timing.
- **Bible descriptors drop in verbatim:** Speech → the Asset voice and Audio delivery; Movement and Stillness → the THIS SCENE line, Acting, and the individuality contrast; locked traits → Assets and Locks.

### 3.8 Population — exactly who exists

Whenever extras would ruin the frame, state the exact headcount and **name the likely intruders for this place** (sunbathers, passersby, crew, a third dancer, distant silhouettes, a reflection of the operator) plus clutter that implies people. When background people *should* exist: EVERYONE IS LIVE, each on their own clock, never frozen.

### 3.9 Speech — the dialogue system (Shotcaller, used by every video format)

Four failure modes: invented lines, paraphrase, wrong mouth, flat delivery. The fix separates **what is said** from **how it is said**.
1. **Script intake:** parse the user's script. Dialogue verbatim (punctuation is performance data). Character cue → tag. Parenthetical → delivery in Audio. (beat) → timed silence with named ambience. V.O./O.S. → off-frame. Strip CONT'D/MORE/headings.
2. **Flag before building:** word budget (~2.5–3 words/second, leave room for reactions — never compress speech), names spoken inside lines, ambiguous pronunciation (numbers, years, acronyms, invented words), unassigned lines.
3. **THE SCRIPT** first critical block — words only, numbered, silences with durations.
4. **ONE MOUTH SPEAKS AT A TIME** when two or more are in frame.
5. **Action Timing** restates each line inside its beat, bound to the body; every listener "says nothing in this beat:" + action.
6. **Audio** restates every line with its delivery spec (volume, pace, pitch, stressed word, emotion audible in the voice, breath, rhythm marks, distance, room), then the anti-invention clause.
Three appearances, identical character-for-character. No mouth mechanics for generated speech. **Mouth mechanics only for an attached track** (lipsync protocol: lip seals on B/M/P, mouth always visible, minimal cuts).

In Genjutsu exact-words form, the words come from the motion video transcript the user provides — same three-appearance discipline.

### 3.10 Audio

Diegetic by default; every sound names a surface or material in frame; ambience named and levelled, carrying the silences. Close on the **music suppression tail** (no music, score, beat, percussion, pad, swell, drone, rising tone, humming, laugh track, off-frame voices, added foley). Attached-track lock when the user's audio is the soundtrack — then never impose per-beat timing on it.

### 3.11 Identity — references and plates

- **Asset line order:** height · build and skin · face · hair · permanent markers anchored to a fixed landmark · makeup · clean-face negations · wardrobe one clause per garment · jewellery and nails · voice · THIS SCENE · fidelity ("100% match to the reference"). Target 60–110 words; leaner on Genjutsu.
- **Voice is identity** (register, texture, pace habit, accent) and stays fixed across prompts.
- Permanent features declared present in every frame; state-conditional identity with its reason; known drift with an inline never.
- **Character sheets from Castkit feed video as identity references.** Scope them: "identity, hair and full outfit exactly as shown — its flat gray field and flat lighting are not used; the scene below lights them."
- Props: material, finish, how held, scale against a body part.
- Material override when a reference has the right cut in the wrong material.

### 3.12 Skin & finish

Video closes Locks with the skin-protection paragraph and tail (Shotcaller). Plates close with the film-capture finish (Scenecraft — people or no-people version). Character plates close with the flat close (Castkit — photoreal or animated). Pick the right one; paste verbatim.

---

## 4. OUTPUT FORMATS — one spine per target

Pull the verbatim blocks from the named source skill. The spines are fixed; the content comes from the toolkit above.

### A. Seedance video shot → `shotcaller-v1`
```
1 HEADER · 2 STYLE PREFIX · 3 NO ON-SCREEN TEXT · 4 CRITICAL BLOCKS (max 4; THE SCRIPT first)
5 ASSETS (@imageN) · 6 GEOMETRY MAP · 7 FIRST FRAME · 8 OPTICS · 9 CAMERA
10 LIGHT & COLOUR · 11 ATMOSPHERE · 12 ACTION TIMING · 13 PHYSICS · 14 ACTING · 15 AUDIO · 16 LOCKS
```
Cross-skill upgrades to apply: closed-mouth HARD LOCK in the header line when no one speaks (Motiondojo) · population block with named intruders (Motiondojo) · individuality clause for multiple people (Motiondojo) · surface-aware physics (Motiondojo) · thirds/lead room/depth staggering and resolution filter in the Geometry Map and Assets (Scenecraft) · plate light carried in verbatim when a Scenecraft plate is the first frame · bible descriptors in Assets and Acting.
Variants: dialogue system · extension (continuity paragraph second, First Frame deleted, hold breaks in the first quarter second) · lipsync protocol · strobe quarantine. 2.0 rations references; 2.5 adds anti-drift weight past 15s.

### B. Genjutsu motion transfer → `motiondojo-v1`
```
INTRO (header + what the video controls + mouth HARD LOCK) · STYLE PREFIX · NO ON-SCREEN TEXT
CRITICAL (role assignment · not the same person · population · mouth — max 4)
REFERENCE LINES (<<<image_N>>>) · GEOMETRY MAP · FIRST FRAME · LENS LOCK · CAMERA
LIGHT AND COLOUR · ATMOSPHERE · ACTION TIMING · PHYSICS · ACTING · AUDIO · LOCKS
```
Forms: 1 body copy · 2 camera copy · 3 body copy, new camera. Motion video never tagged. Runtime = video length. Roles by labelled screen position. Lean: ~900–1,300 words.
Cross-skill upgrades: Shotcaller's dialogue system and delivery specs for exact-words form · Shotcaller's FOV table and defense battery · Scenecraft's night doctrine and plane-named atmosphere · bible movement descriptors as each performer's individual quality · Castkit sheets as the `<<<image_N>>>` identity references.

### C. Character plate → `castkit-v1`
Stations: 0 face lock → 1 additions → 2 outfit build → 3 outfit replacement → 4 character sheet. Never skip forward. Flat 18% gray field, shadowless, zero cast shadow, zero light bleed — the flat close verbatim. Sheets: 3-panel, dead-on, headless variant by the neckline test, skin-tone consistency line.
Cross-skill upgrades: bible visual lock and never-clauses as the face-lock spec · markers anchored to landmarks so they survive into video Assets · animated style lock repeated verbatim wherever that character appears later.

### D. Scene plate / first frame → `scenecraft-v1`
Five unlabeled cinematographer-prose paragraphs: opening shot · overlay line · world · focal anchor and light · capture and finish (six for people-in-scene: a people paragraph after the overlay line). Plate types: A environment · B people in scene · C coverage set · D edit (target / change / protected).
Cross-skill upgrades: bible era palette as the light and grade · Castkit sheets as the people references · **a plate built as a video first frame must agree with the video prompt's Geometry Map, lens and light direction** — write them together.

### E. Story bible → `story-bible-builder`
Interview one character at a time; four quoted prompt-ready descriptors (Speech, Movement, Stillness, Suno), never names inside them; era aesthetic lines copy-paste-ready; production rules with never-clauses. Save to `.claude/skills/<title-slug>/SKILL.md` in this repo so it loads as a project skill.
Cross-skill upgrades: write each descriptor so it drops straight into a Shotcaller Asset voice, a Motiondojo individuality contrast and a Castkit face-lock spec.

---

## 5. THE PIPELINE — how outputs chain

```
STORY BIBLE ──► voice / movement / stillness / era palette / locked traits
     │
     ▼
CASTKIT face lock ─► additions ─► outfit build ─► CHARACTER SHEET
     │                                               │ identity refs
     ▼                                               ▼
SCENECRAFT plate (location, first frame) ─────► SHOTCALLER video / MOTIONDOJO transfer
        location + light + first composition          the moving shot
```

Hand-offs that must hold:
- Sheet → video: scoped as identity and wardrobe only; flat lighting discarded.
- Plate → video: "open on the composition of @imageN exactly, already in motion"; plate's light direction, temperature and bands carried into the video's light block; plate is "geography, materials and light direction only" once people are added.
- Coverage (plates or multi-shot video): the master sets geometry and light; every other angle **rewrites** the light for its vantage (camera-right sun becomes camera-left on the reverse), never copies it.
- Extension: each extension names the final frame of the clip it continues.

---

## 6. UNIFIED PRE-PROMPT CHECK

Plain chat text, never a code block. References first, runtime last, one question.

> Pre-prompt check:
> - References: [each by short visual descriptor and what it governs]
> - Output & target: [e.g. video shot on Seedance 2.5 / Genjutsu Form 3 / face lock on Nano Banana Pro / Plate B on Seedream]
> - Canon: [bible pulled from — or none]
> - Scene / people: [location, time, who, positions]
> - Mouth / dialogue: [closed / N scripted lines, speakers, flags / follows track]
> - Camera & lens: [register, FOV]
> - Light: [direction, quality, temperature]
> - Audio: [diegetic / attached track]
> - Runtime: [total, shot count]
>
> Run it?

Drop lines that don't apply (plates have no runtime or audio). **Iterations skip the check** and ship the full revised prompt. Re-check on new scene, new characters, new form or station.

**Delivery:** numbered reference list in attach order (names only here, never in the prompt) · bolded title with target and runtime · one fenced code block.

---

## 7. MASTER PRE-DELIVERY PASS

- [ ] Output format, target model and its caps settled; correct source skill's verbatim blocks used, not paraphrased
- [ ] Bible checked — descriptors and locked traits pulled verbatim where active
- [ ] Composition planned: thirds, foreground mass, lead room, depths staggered, resolution filter run
- [ ] Every reference tagged correctly for the target and scoped to what it governs
- [ ] Mouth state decided and locked (video); dialogue three-appearance identical with delivery only in Audio
- [ ] Max four CRITICAL blocks, in priority order
- [ ] Every body acting in every beat; listeners silent with an action; individuality on multiple people
- [ ] Population: exact count and likely intruders, or EVERYONE IS LIVE
- [ ] Lens in degrees, locked, defended if unusual; one motivated camera register
- [ ] Light by direction/quality/temperature, three sourced bands, no fixtures; night doctrine if night
- [ ] Atmosphere as density with named planes; vapor only with a source
- [ ] Physics rewritten for this surface and wardrobe; contact shadows; nothing floats or slides
- [ ] Audio diegetic with suppression tail, or attached-track sole-source lock
- [ ] Correct close: skin protection (video) / film finish (plate) / flat close (character plate)
- [ ] No names, no ratio, no tool names, no ages, no negative block, no lyrics, no meta

---

## 8. MASTER REPAIR TABLE

| Symptom | Fix | Origin |
|---|---|---|
| Model invents or paraphrases lines | THE SCRIPT first; three appearances identical; anti-invention clause in Audio; no delivery inside THE SCRIPT | Shotcaller |
| Wrong mouth / listener mouths along | ONE MOUTH SPEAKS AT A TIME; "says nothing in this beat" + action | Shotcaller |
| Mouths moving with no speech | Closed-mouth HARD LOCK in the header/intro + NO SPEAKING block | Motiondojo |
| Delivery flat or robotic | Add delivery specs; strip mouth mechanics from generated speech | Shotcaller |
| Lines rushed / cut short | Word budget over runtime — split, never compress | Shotcaller |
| Captions on screen | NO ON-SCREEN TEXT moved low or carved out — restore | All |
| Music appears | Suppression tail shortened — restore beat, percussion, pad, swell, drone by name | All |
| Extra people appear | Exact headcount + named likely intruders | Motiondojo |
| Performers look cloned | Individuality block with contrasting movement qualities | Motiondojo |
| Characters swap parts | Role assignment by labelled screen position | Motiondojo |
| Faces/clothes from the motion video appear | Intro must limit what the video controls | Motiondojo |
| Motion loops or rushes | Runtime ≠ motion video length | Motiondojo |
| Camera robotic or orbits | Specific moves tied to bodies, operator footing, never-settles clause | Motiondojo |
| Bodies look composited / pasted in | Surface-aware physics, contact shadows, light side named on the person, scale against the world | Motiondojo + Scenecraft |
| Figures float or slide | Physics chain missing deformation or contact shadow | Shotcaller |
| Background bodies frozen | EVERYONE IS LIVE + action per beat | Shotcaller |
| Wardrobe or face drifting | Restate every garment; tighten the face lock; fewer references | Shotcaller + Castkit |
| Lens averaging to normal | Defense battery | Shotcaller |
| Geometry inverting | Promote the relationship to a CRITICAL block | Shotcaller |
| Choppy footage | Cadence clause / operator-weight line in Technical; soften per-beat light pulses | Shotcaller + Motiondojo |
| Air reads as fog / rays appear | A vapor has no source or a mood word implied it — rewrite as density | Scenecraft |
| Plate flat like a backdrop | Name the nearest plane and its softening | Scenecraft |
| Plate digital and crunchy | Restate lifted blacks; move sharpness into micro texture and grain | Scenecraft |
| Frame cluttered | Resolution filter skipped | Scenecraft |
| Subject dead centre and static | Re-place on a third, add a foreground mass | Scenecraft |
| Coverage angles don't match | Master not attached, or light copied instead of rewritten for the vantage | Scenecraft |
| Edit changed the whole image | Target / change / protected — never a full redescription | Scenecraft |
| Garbled signage | Exact words in quotes with material, colour, placement (language on Seedream) | Scenecraft |
| Shadow under feet / glow behind figure on a plate | Zero-shadow and zero-bleed clauses missing from the flat close | Castkit |
| Sheet panel turned three-quarter | Orientation clause verbatim, with the "regardless of how the figure stands" override | Castkit |
| Rear panel skin darker | Skin-tone consistency line | Castkit |
| Animated character sliding to photoreal | Style lock missing or paraphrased | Castkit |
| Marker in the wrong place | Anchor it to a fixed anatomical landmark | Castkit |
| Extension resets / opens frozen | Continuity paragraph second, final frame named, hold breaks in the first quarter second | Shotcaller |
| Prompt drifts on canon | Pull the bible's quoted descriptors and never-clauses verbatim | Story Bible |
