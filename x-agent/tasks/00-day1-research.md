# Task 00: Day 1 deep research (run once, before any posting)

Goal: by the end of this run we know (1) where the account stands, (2) who wins in our arena and how,
(3) what goes viral in the arena right now, and (4) the plan for Day 2. Take your time; this run can be long.
Read `CLAUDE.md` first. Reading only. Human pace (pause a few seconds between page loads; max ~150 X page loads total).

## 1. Studio & account audit
1. Open https://www.evolvesstudios.com. Note services, style, best work, clients, tone, contact/booking path.
   Write findings into `memory/positioning.md` (section "Studio facts").
2. Open X in Chrome. Find the logged-in account (profile icon). Record handle, display name, bio, banner, pinned post,
   followers, following, join date, posting history (last 50 posts: date, text, format, views, replies, reposts, likes,
   bookmarks). Save posts to `memory/post-log.csv` with `source=history`.
3. Compute the baseline: median views, median engagement, best 5 and worst 5 posts and why.
   Put the account handle into `config.json` → `brand.handle` (create from `config.example.json` if missing).
4. Profile conversion audit: does the bio say who we are, who it's for, and why to follow, in 1 line? Is the pinned post
   our best work? Draft 3 bio options + pinned post recommendation (Ishaan changes them by hand).

## 2. Map the arena's winners (`memory/creators.md`)
Find **40–60 accounts** across these lanes (aim for ≥5 per lane):
**Creative:** artists/illustrators · designers · 3D/CGI/VFX · animation · motion · video editors · AI-video/AI-art creators ·
creative culture & ad/marketing commentators.
**Freelance & business:** freelance educators · agency/studio founders building in public · solopreneurs/creator-economy accounts.
**Viral bridgers:** accounts that turn general viral moments into niche content (in any niche: study their mechanics).
**Viral radar:** accounts that surface viral videos/news/memes first (we watch them for trends, not to copy).
**Fast risers:** 1k–30k followers growing fast in any of the above (most useful to copy at our size).
Sources: X search (`freelance`, `freelancer clients`, `creative agency`, `designers`, `artists`, `animation`, `3D`, `CGI ad`,
`motion design`, `AI video`, `content creator`, sorted Top and Latest), "who to follow" suggestions on those profiles, the seed list already in `creators.md`,
web lists. Verify each handle exists.
For each: handle, lane, followers, posts/day, typical formats, median views of last ~20 posts, best recent post,
hook styles, reply behaviour (do they reply a lot? to whom?), what to steal. Mark top 15 as **core watchlist**.

## 3. Outliers → swipe file (`memory/swipe-file.md`)
For core-watchlist accounts, find posts from the last 30 days with **≥3× that account's median views**.
Collect ≥30 outliers. For each: link, format, hook (first line verbatim), topic, media style, length, time posted,
why it worked (1 line), reusable pattern, how WE would do it.
Then summarise: top 10 patterns by frequency × strength.

## 4. Trends & viral mechanics
1. X Explore → Trending / For you / News / Entertainment (logged-in view). Note what's trending in India and globally.
2. Web: Google Trends (daily), r/blender, r/Cinema4D, r/motiondesign, r/freelance, r/graphic_design top-week,
   creative news (80.lv, CG Channel, Motionographer, BlenderNation), AI-video news.
3. Write `memory/trend-log.md` entries: trend, lifespan guess, bridge (from `knowledge/formats.md`), go/skip.
4. Media-style scan: which visual styles are winning in the arena this month (e.g., FOOH, soft-body, clay, stylised toon,
   hyperreal product, lo-fi "made on my phone")? Record in `memory/playbook.md` → "Media styles" (as hypotheses).

## 5. Timing
From the account's own history (if ≥20 posts) and the core watchlist's best posts, estimate when the arena's audience is
most active. Convert to IST. Propose slots in `memory/schedule.md` (respect ≥3 h spacing).

## 6. Positioning & plan
1. Finish `memory/positioning.md`: one-line positioning, 4 pillars with % mix, voice rules, bridges, never-list.
2. Write `memory/experiments.md`: 5–8 hypotheses to test in week 1 (e.g. "breakdown videos beat finals on follows").
3. Write `memory/playbook.md` v0.1: starting rules from the research (marked "unproven" until our own data confirms).
4. Fill `memory/media-library.md`: ask in the report which renders/reels Ishaan can drop into `media/library/`.
5. Recommend the number of posts/day for week 1 with reasoning (see `memory/schedule.md`).

## 7. Deliver
- Write `memory/weekly/day1-report.md`: account baseline, arena map, top patterns, trend opportunities,
  week-1 plan, profile fixes, and **questions for Ishaan** (facts we need, media we need).
- Build tomorrow's first pack draft (`tasks/01-morning-pack.md` steps 3–6) so Day 2 starts ready.
- Send a Telegram summary (short) with the report path. Open the report in Chrome.
