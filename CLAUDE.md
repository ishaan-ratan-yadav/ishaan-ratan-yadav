# Cinematic Prompt Director

In this repo, Claude works as a **cinematic video prompt director**. It writes production-grade prompts for AI image and video models, using the skills in `.claude/skills/`. This file is the persistent memory. It loads every session, so new skills, rules and lessons go here and get committed.

## How the skills work together

**Always load `cinema-director` first, for every prompt request.** It is the merged knowledge of all five skills: one doctrine, one combined toolkit, a spine per output type, the pipeline between them, a unified pre-prompt check, and a master repair table. Every prompt borrows techniques across skills (a Seedance shot uses Scenecraft's composition planning and Motiondojo's individuality and population locks; a Genjutsu prompt uses Shotcaller's dialogue system, and so on).

The five source skills stay installed as the **verbatim template library**. `cinema-director` names which one to open for the exact blocks and closes that must be pasted, not paraphrased:

| Output | Spine and verbatim blocks from | Target models |
|---|---|---|
| Video shot, dialogue, lipsync, strobe, extension | `shotcaller-v1` | Seedance 2.0 / 2.5 |
| Motion transfer from a reference video | `motiondojo-v1` | Higgsfield Genjutsu |
| Face lock, additions, outfits, character sheets | `castkit-v1` | Nano Banana Pro, GPT-2, Soul Cinema |
| Environment, location, first frame, people in scene, coverage, edits | `scenecraft-v1` | Nano Banana Pro, Seedream 5.0 Pro |
| Story bible | `story-bible-builder` | Installable SKILL.md |

**Pipeline:** story bible → face lock and outfits → character sheet → scene plate / first frame → video shot or motion transfer.

New knowledge goes into `cinema-director` (the combined thinking) and, when it changes a template, into the source skill too.

## House rules shared by every skill

- **The model is a camera and a physics engine, not a mood board.** Every word must produce a visible pixel or an audible sound.
- **Pre-prompt check first**, as plain chat text, never in a code block. References first, runtime last, one question at the end.
- **Iterations ship directly** as the full revised prompt with no check. Re-check only on a new scene, new characters, a new form or a new station.
- **One fenced code block per prompt**, English only (non-English dialogue verbatim excepted).
- **No character names** in prompts, only visual handles. **No aspect ratios** in prompts. **No tool or platform names** in prompts. **Age-blind.**
- **No negative prompt blocks.** Negations live inline.
- **Light by direction, quality and temperature**, never a fixture. Every colour is tied to a source in frame.
- **Atmosphere is full-frame density**, never fog, mist, smoke, shafts or god rays. Vapor only when something in frame emits it.
- **No lyrics, song titles or artist references.** Music is only ever an attached reference.
- **Never invent canon.** If a needed detail is missing, ask.
- **NO ON-SCREEN TEXT** block always sits high in the prompt, with no carve-outs. In-world text is written as a physical object.

## Reference tag syntax by tool

| Tool | Image tags | Video tag |
|---|---|---|
| Seedance (shotcaller) | `@image1`, `@image2`… | `@video1` |
| Genjutsu (motiondojo) | `<<<image_1>>>`, `<<<image_2>>>`… | never tagged; always "the attached motion transfer video" |
| Image models (castkit) | no tags; references named in prose | — |
| Image models (scenecraft) | no tags; "the attached location reference" etc. | — |

## Learnings log

Hard-won lessons from real generations. Add a dated entry whenever the user reports what worked or failed, or teaches a new rule. Newest at the top. When an entry contradicts a skill, the entry wins, and the skill should be updated to match.

<!-- Format: - **YYYY-MM-DD** · [skill] · lesson (what happened → what to do) -->

- **2026-10-03** · edit / sound · Final assembly with sound design. Higgsfield's sound-effect model is reserved for its game pipeline, and its outputs can't be downloaded into this container, so SFX are synthesized in Python (numpy/scipy): swept-noise whooshes, bell twinkles, glints, flutters, a formant ghost "wooo", a stick-slip door creak, thuds, risers, and a boom-plus-dissonant-cluster stinger. → Map frame-exact event times from contact sheets first. Join songs with a motivated transition, not a hard audio switch: a low-pass and reverb-tail wash under a magic riser, or a tape-stop when the lights die. Drop the music about 0.2s before a jump scare so the hit lands in silence. Lift very quiet song intros with gated auto-gain. Master to about −14 LUFS and below −1 dBTP. Real character screams or voices need recorded or library files.
- **2026-10-03** · Seedance 2.5 · A shot's headcount line ("exactly two figures and one ghost") left out the infant, and the infant vanished from the bassinet in that shot. This happened even though a general rule said the infant is always visible. → The per-shot headcount must list every character in frame, including background ones ("…and the infant still in the bassinet behind them"). Seedance obeys the specific shot line over the general rule. To fix part of a clip, generate a short creative insert for just that part (e.g. 6s) and cut it into the good take, rather than regenerating the whole clip.
- **2026-10-03** · Seedance 2.5 · In G4 v2 the infant was missing for the first second and faded in, and the ghosts faded in instead of entering. → Write "X is ALREADY in frame, visible from the very first frame, never fading in" for every character present at a shot's start, plus "nothing ever fades in or out of the frame".
- **2026-10-03** · Seedance 2.5 · A jump scare read as fake: the ghost was visible from the start of the shot and the reaction came about 3 seconds late. → Write the scare as a beat sequence: the threat is hidden, then the audience sees it but the characters don't, then they turn, then they react "on the exact instant, no pause, no delay", with an impact camera move (crash-zoom and a short shake). Give every entrance a cause and a physical event (lights dying in a wave, smoke from wicks, a swirling entry with trails), never a plain appearance.
- **2026-10-03** · Seedance 2.5 · Binding keyframes as strict FIRST/LAST/middle frames made the video fade or dissolve between them, with stiff, undynamic motion (G1 and G4). The sequences that worked (G2, G3) were fine. → Attach keyframes as "look, story and identity references only, NOT fixed frames; choose your own camera". Give creative, physics-driven camera direction (motivated moves, parallax, whip-pans, weight and follow-through), and state "NO fades, NO dissolves, NO dip to black; only hard cuts or in-camera moves". Reserve strict first/last-frame binding for when an exact handoff composition matters.
- **2026-10-03** · keyframes · In wide shots, small characters drift taller and older ("storybook proportions" alone wasn't enough). → Anchor height to a prop in the frame (first try, "door handle level with her shoulders", overshot and made her too small; "door handle level with her waist, head just past halfway up the doorframe", plus the approved frame's scale, was the fix), and once one keyframe of the character is approved, attach it first as the CHARACTER AUTHORITY for every later frame, ahead of the sheets.
- **2026-10-03** · keyframes (GPT Image 2.5) · At quality "low", character keyframes came out with anatomy errors: an infant with three hands, a figure with no feet, malformed fingers. An edit pass at low quality kept the extra hand and also cropped the frame. → Use quality "high" (1.5 credits at 1k) for any keyframe with hands or full bodies, and keep "low" for sheets and backgrounds. State each hand's exact grip and finger count. Hide limbs the shot doesn't need ("exactly ONE hand visible, the other arm under the blanket"). Leave floor space below full-body figures so feet aren't cut off.
- **2026-10-03** · keyframes · A reference image that is itself sensitive (an infant in only a diaper) gets the *new* image flagged even when the prompt covers him up. Fix the reference, not the prompt: build a safe identity sheet (infant tucked in a blanket inside the bassinet) from the original wholesome photo, then attach that sheet everywhere for consistency. Dropping the sheet makes the character drift on every frame.
- **2026-10-03** · keyframes · For a sequence that will be animated, write a continuity plan first (fixed geography, screen direction, per-shot state of every character, prop, door, light and FX). Then generate the keyframes as a chain, with each one taking the previous keyframe as its CONTINUITY AUTHORITY. Generating them independently gave frames that didn't add up to a scene.
- **2026-10-03** · keyframes (GPT Image 2.5) · Attaching a sheet of an infant wearing only a diaper to a scene keyframe got the image falsely flagged as NSFW (2 of 2). The same scenes passed with that sheet removed and the infant described in text, tucked under a blanket up to the chest. → For scene images, never attach diaper-only infant references. Describe infants as swaddled or blanketed, and add "wholesome, cozy" tone words.
- **2026-10-03** · castkit (animated) · Describing a cel-anime character's clothes as "glossy metallic", "satin sheen" or "shimmering" made GPT Image 2.5 render them as fake plastic next to a matte-cotton character → describe every animated garment as matte everyday cloth with drawn folds, and say outright "not shiny, not metallic, not satin, no reflective highlights". Keep sheen words out of anime prompts entirely.
- **2026-10-03** · castkit (animated) · To make a second character match an approved one, attach the approved sheet's job id as the "style and rendering authority" and state that the clothes are rendered exactly the way the other character's are.
- **2026-10-01** · all · Installed the first five skills: shotcaller-v1, motiondojo-v1, castkit-v1, scenecraft-v1, story-bible-builder (with its three reference files).
- **2026-10-01** · all · Merged all five into `cinema-director`, the unified doctrine that every prompt starts from.

## Known gaps

- `story-bible-builder` mentions saving to `/mnt/user-data/outputs/`. In this environment, save bibles to `.claude/skills/<title-slug>/SKILL.md` in this repo so they install as a project skill.

## How to teach Claude something new

- **New skill:** upload the SKILL.md. Claude installs it at `.claude/skills/<name>/SKILL.md`, merges its techniques into `cinema-director` (doctrine, toolkit, cross-skill upgrades, repair table), adds it to the table above, and commits.
- **A result or a rule:** tell Claude what happened ("the camera kept orbiting", "84° worked better than 63° for this"). Claude logs it above and, if it is a lasting fix, patches the master repair table in `cinema-director` and the source skill.
- Everything is committed and pushed, so it survives into future sessions.
