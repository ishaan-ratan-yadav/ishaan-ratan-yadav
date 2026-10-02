# Task 01: Morning pack (daily, ~08:00 IST)

Read `CLAUDE.md`, `memory/positioning.md`, `memory/playbook.md`, `memory/schedule.md`, `memory/experiments.md`,
and the last 3 days of `memory/trend-log.md` and `memory/post-log.csv`. Budget: ~60 X page loads, human pace.

## 1. Scan (what's moving right now)
- X Explore: Trending (India + worldwide), For you, News, Entertainment, Sports. Note top ~20.
- X search, Top and Latest, last 24 h: arena keywords (freelance, freelancer, clients, agency, creative, designer, artist,
  animation, 3D, CGI, motion design, AI video, content creator, portfolio, pricing). Note posts with fast early traction.
- Core watchlist (`memory/creators.md`): last 24 h of posts. Any outlier (≥3× their median) → `memory/swipe-file.md`.
- **Outside the niche too:** the top viral posts/videos/memes/news of the day on X (Explore + viral-radar accounts in
  `creators.md`), Google Trends daily, big brand launches/ads, sports/entertainment moments. Anything viral is a candidate
  for a bridge.
- Niche news: creative/design/animation/AI-tool news, freelance/creator-economy news.
- **Discovery:** add at least 1 new creator per day to `creators.md` (a fast riser or someone behind an outlier) and
  demote stale ones. The watchlist must keep evolving.

## 2. Pick today's bets
- Score each trend: virality now (rising?), lifespan, bridge fit (`knowledge/formats.md`), can we produce it today,
  brand-safety. Keep the top 3. Log all considered trends in `memory/trend-log.md` (go/skip + reason).
- Decide today's post count and slots from `memory/schedule.md` (never exceed its safe max).

## 3. Plan the slots
For each slot choose: pillar, format, hook type, media, hypothesis (from `memory/experiments.md`), and whether it's
proven (70%), variation (20%) or wild (10%). Viral bridges of live trends (in or outside the niche) get the
share set in `memory/positioning.md` (default: about half of the day's posts, never less than one).
Media priority: Ishaan's real renders (`memory/media-library.md`) > card from `tools/make_card.py` > text-only.
If the best idea needs a new render (spec ad / FOOH / recreate), put it in the pack as a **"Render request"** with a
shot description, length, deadline (trend lifespan), and the post text ready to go once the render exists.

## 4. Write
- For every post: 5–10 hooks → pick best → body. Thread if depth is needed (each part ≤280).
- Follow `knowledge/writing.md`. Use only real facts; anything uncertain → note "NEEDS FACT CHECK" in `hypothesis`.
- Links only in `self_reply_link`.

## 5. Score (virality judge)
Rate each draft 1–10 on: stop-the-scroll (line 1), P(reply), P(repost/quote), P(bookmark/share), P(follow),
fit with positioning, and negative risk (mute/block/report; subtract). Rewrite anything under 7. Put the score in `score`.
Compare with `memory/playbook.md`: does it repeat something proven? If it's a wild bet, say so in `hypothesis`.

## 6. Engagement starter
Add 5–8 `replies` (targets from the scan: big arena accounts, posted < 60 min ago, where we can add value) and 0–2 `quotes`.
Each reply gets 3 options (value / counterpoint / funny or visual). Follow the reply rules in `knowledge/writing.md`.

## 7. Build & deliver
- Write `packs/YYYY-MM-DD.json` (format: `packs/EXAMPLE.json`, including `render_requests` when a new render is needed).
- Run `python tools/xpack.py packs/YYYY-MM-DD.json`. Fix every warning it prints, rebuild.
- Open `packs/YYYY-MM-DD.html` in a new Chrome tab. Telegram gets the summary + one-tap links.
- If Telegram send fails from the sandbox, open the printed `api.telegram.org/...sendMessage?...` URLs in Chrome tabs
  (that sends them), then close those tabs.
