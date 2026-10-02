# X Growth Agent for Evolves Studio: Ideation & Design (v0.1, draft for review)

> Status: **ideation, not built yet**. We finalize this doc together, then build in phases.
> Last researched: 2026-10-02.

---

## 0. The goal

Grow the Evolves Studio account on X: more followers, impressions, and engagement, every week.
The agent works as a **growth loop that runs experiments and learns from them**:

```
   ┌──────────── DAILY ─────────────┐
   │ 1. Scan (trends + competitors)  │
   │ 2. Plan (4 slots + engagement)  │
   │ 3. Create (copy + media)        │
   │ 4. Score & pick best variant    │
   │ 5. Publish + golden-hour engage │
   │ 6. Measure (1h / 6h / 24h / 72h)│
   └───────────────┬─────────────────┘
                   ▼
   ┌──────────── WEEKLY ────────────┐
   │ 7. Review: what won / what died │
   │ 8. Update the Playbook          │
   │ 9. Re-allocate: double down,    │
   │    iterate, kill, try new bets  │
   └─────────────────────────────────┘
```

No system can guarantee virality. What we can do is raise the odds on every post and improve them
each week, because each post is a test and the results feed the next week's plan.

---

## 1. Constraints we must design around

These come from X's own rules and recent changes. Ignoring them gets the account suspended, which ends growth.

| Your idea | Constraint | How we handle it |
|---|---|---|
| "Connect to my account on Chrome" and let the agent drive it | X's automation rules: *"Use of non-API-based forms of automation, such as scripting the X website, may result in the permanent suspension of your account."* | The agent connects through the **official X API (OAuth)**. Chrome stays yours. The agent never clicks around x.com as you. |
| Agent auto-comments on other people's posts | Since **23 Feb 2026** the API only allows a programmatic reply if the original author @mentions you or quotes your post. Since ~May 2026 X has also been **suspending accounts for AI-generated reply automation**. Keyword-based auto-replies have long been banned. | **Engagement Copilot**: the agent finds the best posts to reply to and drafts the replies. You get a one-tap link (`x.com/intent/post?in_reply_to=…&text=…`), check it, and post it yourself. This keeps the reply strategy and removes the ban risk. |
| Agent quote-posts others | Automated quote posts are allowed for informational or entertainment purposes. Spammy volume is not. | Allowed in small numbers (1–2 per day max), only high-quality ones, and they count toward the 4 daily slots. |
| Auto-like / auto-follow | Automated likes are prohibited. Aggressive follow/unfollow is a classic suspension trigger. | Not automated. The agent can suggest accounts to follow. |
| 4 posts a day | The For You ranker applies an **author-diversity decay**: each post after your first in a viewer's feed is multiplied by a decaying factor. | 4/day is fine if the posts are **spaced 3+ hours apart**. Never post in bursts. |

---

## 2. What we know about the algorithm (and how it shapes the agent)

Source of truth: xAI open-sourced the Grok-based For You ranker (`xai-org/x-algorithm`, Jan 2026, major update May 2026).

**How a post is scored.** A Grok transformer ("Phoenix") predicts, for each viewer, the probability of ~19 actions:

- **Positive:** like, reply, repost, quote, share, share via DM, copy link, clicks (post, profile, link, photo, video, quoted post), video quality view, dwell / dwell time / active seconds, **follow author**
- **Negative:** not interested, mute author, block author, report, "not dwelled" (people scrolled past)

`Final Score = Σ weight × P(action)`, then three adjustments: **author-diversity decay**, an **out-of-network discount**, and a **boost for authors with low impressions**.

**What that means for the agent:**

1. **Optimize for conversation and attention, not likes.** Replies, quotes, shares, and dwell matter most. Every post needs a reason to stop scrolling (hook) and a reason to respond (open loop, opinion, question, contrarian take).
2. **Negative signals are expensive.** Rage-bait that gets you muted or blocked hurts reach in later posts. The agent filters out "cheap viral" tactics that trigger mutes.
3. **"Not dwelled" is a penalty**, so the first line decides everything. The agent writes 5–10 hook variants per post and scores them.
4. **Out-of-network reach is discounted.** Growth comes from (a) posts strong enough to break out anyway and (b) replies under bigger accounts' posts in your niche, where new people see you.
5. **Speed matters.** Early engagement velocity drives distribution. Replying to every comment in the first 30–60 min ("golden hour") makes a big difference, so the agent alerts you.
6. **Links:** link posts get much less reach, and reportedly near-zero for non-Premium accounts since Mar 2026. Rule: **never put a link in the main post.** Put it in a self-reply.
7. **Hashtags:** they barely matter now; the ranker reads content directly. Use 0–1 relevant hashtag, never several.
8. **Premium:** industry data consistently shows Premium accounts get several times more reach. **Recommendation: get X Premium** (or Premium+) for the account. It's the cheapest lever available.
9. **Timing:** the generic "best times" (weekday mornings to mid-afternoon in the audience's timezone) are only the starting point. After 2–3 weeks the agent uses **your own audience's** response curve.

---

## 3. Architecture: 10 modules

### Module A: Connection, Safety & Control Layer
- X API OAuth 2.0 user-context token for @EvolvesStudio (posting, reading own metrics).
- **Guardrails:** max posts/day, minimum spacing, banned topics, brand-safety filter (no trend-jacking tragedies, politics unless you opt in), and fact-checking of claims and numbers.
- **Approval modes** (per action type): `autopilot` / `approve-first` / `draft-only`. We start everything at `approve-first` and graduate to autopilot after a couple of weeks of trust.
- **Kill switch** plus **anomaly detection**: a sudden reach collapse (possible throttling) pauses posting and alerts you.
- API-credit budget tracker with a monthly cap.

### Module B: Daily Intelligence Scanner (runs every morning)
Sources:
- X API trends (global plus your target countries), and search over niche keywords for posts gaining traction *right now*
- Google Trends, Reddit (niche subs), Hacker News / Product Hunt (if tech or AI), news feeds for the niche, YouTube/TikTok trending formats
- Competitor feed (Module C)

Output, a **Daily Brief** (sent to your phone):
- Top 5 trends **relevant to Evolves Studio**, each with an angle for how we'd post on it
- Formats and hooks working this week
- 10–20 high-leverage posts to reply to today
- Today's 4-slot content plan

### Module C: Competitor & Creator Reverse-Engineering
- Watchlist of **15–40 accounts**: direct competitors, aspirational creators in the niche, and fast-growing small accounts (the most useful to study, because what works for them works at our size).
- For every post they publish, store: text, format, length, hook type, media type, topic, posting time, and metrics over time.
- **Outlier detection:** flag posts that did **≥3× that account's median** engagement. Studying outliers relative to each account's own baseline shows *what* made a post work, separate from *who* posted it.
- An LLM analysis of outliers extracts the reusable pattern (hook structure, emotional trigger, format, CTA). These patterns go into the **Swipe File**.
- **Workflow reconstruction:** for each competitor, infer posting cadence, time slots, content-pillar mix, thread vs. single vs. media ratio, how fast they reply to comments, who they reply to and engage with, and follower growth curve (tracked daily).
- Weekly "Competitor Moves" section in the report: what changed in their strategy and what's working for them now.

### Module D: Strategy & Planner
- **Positioning doc** (built first, together): who Evolves Studio is for, 3–4 **content pillars**, voice, and what we never post. Niche clarity is the single biggest growth factor; the algorithm needs to know who to show you to.
- **Daily 4-slot plan**, e.g.:
  1. **Morning – Value:** a thread or deep post (bookmarks, dwell)
  2. **Midday – Trend-jack:** our angle on today's trend (reach, out-of-network)
  3. **Afternoon – Visual:** image, video, or meme (shares, dwell)
  4. **Evening – Conversation:** opinion, hot take, or question (replies)
- **Experiment budget: 70 / 20 / 10.** 70% proven patterns, 20% variations of winners, 10% wild new bets. Every post is tagged with its hypothesis so the weekly review can learn from it.
- Content recycling: winners get re-cut into a new format 4–8 weeks later.

### Module E: Content Generator
- **Voice model:** a style guide built from your best-performing past posts plus your edits to drafts. It keeps learning from what you change.
- For each slot: 5–10 hook variants and 2–3 body variants.
- **Hook library** (curiosity gap, contrarian, numbers/listicle, story, "how I…", before/after, mistake, prediction), updated from the Swipe File.
- **Anti-AI-slop pass:** strip AI writing tells (em-dash overuse, "delve", "game-changer", rule-of-three padding). AI-sounding posts get scrolled past ("not dwelled") and can be flagged.
- Formatting for X: line breaks, first line under ~80 chars, threads with a strong 1/ and a closing CTA, long posts (Premium), and X Articles for evergreen pieces.

### Module F: Pre-Post Scoring ("Virality Judge")
Before anything posts, an LLM judge scores each variant against the algorithm's actual signals:
- P(reply), P(repost/quote), P(share/bookmark), dwell (does line 1 stop the scroll?), P(follow) (does it show expertise or personality?), and negative risk (mute/block/report).
- It also checks: link placement, hashtag count, length, media fit, and brand safety.
- The top-scoring variant wins. Over time we **calibrate the judge against real results**, so it learns which predicted scores turn into actual performance on this account.

### Module G: Media Studio
- **Style research:** from the competitor and trend scans, track which visual formats win (screenshots with annotations, minimalist quote cards, data charts, memes, short vertical clips, before/after, UI mockups, AI-art styles).
- **Generation:**
  - Images: quote cards, charts and infographics, memes, branded templates (consistent colors and fonts = recognizability)
  - Video: short clips (5–30 s) with captions. Native video gets "video quality view" signals.
  - Tools: Higgsfield (connected in this environment: image/video generation plus a **virality predictor for video**), plus code-rendered templates (HTML→PNG) for charts and cards so they're on-brand and crisp.
- Up to 4 images per post. The agent decides when media helps and when text-only is stronger.
- Every generated asset is checked for copyright and likeness issues before use.

### Module H: Publisher & Golden-Hour Protocol
- Posts at the scheduled slot through the API (threads supported).
- Links go into a self-reply automatically.
- **Golden-hour alert:** "Post is live. Be on X for the next 30 min." The agent pre-drafts replies to incoming comments for you to send. (We'll verify whether API replies to people who replied to *you* are permitted under the Feb 2026 rule. If yes, they can be semi-automated with approval; if not, they stay one-tap.)
- Pins the best-performing recent post if it beats the current pinned one.

### Module I: Engagement Copilot (comments & quotes)
- Every few hours, it finds **high-leverage posts**: big accounts in the niche, posted in the last 15–30 min (early replies get seen most), on topics where Evolves Studio has something real to add.
- Drafts **3 reply options** per post (insight, counterpoint, a funny line) that add value. Never "Great post! 🔥".
- Sends a batch to you (Telegram/Slack/dashboard), each with a one-tap intent link to review and post.
- **Relationship map:** tracks 20–50 accounts with overlapping audiences. Regular, genuine interaction builds the "relationship strength" signal and can lead to collabs and mutual reposts.
- Target: about 10–20 quality replies per day. In early growth, smart replies on big accounts often bring more followers than your own posts do.

### Module J: Analytics & Weekly Learning Loop
**Data captured per post** (at 1h, 6h, 24h, 72h): impressions, likes, replies, reposts, quotes, bookmarks, profile visits, link clicks, video views, follower delta around the post, plus all the tags (pillar, hook type, format, media style, time slot, trend vs. evergreen, hypothesis).

**Daily:** quick health check and anomaly alerts.

**Weekly review (every 7 days), done by the strongest model:**
1. Rank all posts by engagement rate and by **followers gained**. Followers is the north star; impressions alone are vanity.
2. Analyze by dimension: which hooks, formats, pillars, slots, media styles, and lengths won or lost (with sample sizes, so we don't over-read noise).
3. Compare against competitors' outliers this week.
4. Decide on each pattern: **double down** (move to the 70%), **iterate** (20%), or **kill**.
5. Update the **Playbook**: a living document of rules learned for *this* account, versioned so we can see how strategy evolved.
6. Update the posting-time model, the voice guide, and the judge calibration.
7. Send you a **Weekly Report** with wins, losses, what changes next week, and decisions that need you.

**Monthly:** a deeper review covering positioning check, pillar rebalance, competitor-list refresh, and profile (bio, banner, pinned post) A/B test results.

---

## 4. Extra ideas I'm adding beyond your list

1. **Profile conversion optimization.** Virality only matters if visitors follow. The agent optimizes bio, banner, and pinned post, and tracks the profile-visit → follow rate.
2. **Positioning first.** One week of setup to nail the niche and pillars before the posting engine runs.
3. **Swipe File + Playbook as memory.** The agent's accumulated knowledge lives in versioned files, so it actually gets smarter each week instead of starting fresh.
4. **Experiment tagging.** Every post carries a hypothesis. This is what makes the weekly review rigorous rather than vibes.
5. **Virality judge with calibration.** Predicted vs. actual performance keeps improving the pre-post scoring.
6. **Golden-hour protocol.** The highest-leverage 30 minutes of each post's life, made into a routine.
7. **Relationship / collab map.** A systematic way to build a network in the niche.
8. **Negative-signal guard.** Avoids tactics that create mutes and blocks, which hurt future reach.
9. **Content recycling.** Old winners get re-cut into new formats.
10. **Long-form assets.** X Articles and evergreen threads that keep pulling followers over time.
11. **Spaces / live** (optional later). Co-hosting Spaces in the niche is a strong follower driver.
12. **Cross-posting** (later). Re-cut winners for Threads, LinkedIn, Bluesky, and Instagram.
13. **Funnel** (if Evolves Studio sells something). Lead magnet in the pinned post or link-in-reply, with conversion tracking.
14. **Anomaly / shadow-throttle detection** that pauses the agent automatically.
15. **Phone-first UX.** Daily Brief, approval queue, and reply copilot all on Telegram (or Slack), so the whole thing takes you about 15–20 min a day.
16. **Cost dashboard.** API and LLM spend tracked against a cap.

---

## 5. Proposed tech stack

| Layer | Choice | Why |
|---|---|---|
| Language | Python | Best ecosystem for X API, data, scheduling |
| X access | Official X API v2 (pay-per-use) | Only safe route; posting + metrics + search + trends |
| Brain | Claude API: Opus for weekly review and strategy, Sonnet for drafting and analysis, Haiku for cheap classification and tagging | Use the strongest model only where reasoning quality matters |
| Media | Higgsfield (image/video + video virality predictor) + HTML→PNG templates | Trend-styled visuals and on-brand cards |
| Storage | SQLite to start (Postgres later) + Markdown Playbook / Swipe File in git | Simple, versioned, auditable |
| Scheduling | Claude Code Routines (scheduled cloud runs) for the "thinking" jobs (daily scan, weekly review) + a cron runner (GitHub Actions or a small VPS) for exact-time posting | Reliable timing for posts; full agent reasoning for research |
| Interface | Telegram bot (brief, approvals, one-tap replies) + a simple web dashboard | You run it from your phone |

### Rough monthly cost (to be confirmed once we size the watchlist)
- **X API:** posts cost ~$0.015 each ($0.20 with a URL), post reads ~$0.005, user reads ~$0.01.
  - Posting: 4/day + link self-replies ≈ **$5–15/mo**
  - Reading (competitor tracking, trend search, metrics, reply-opportunity scans): **≈ $60–200/mo** depending on watchlist size and scan frequency. This is the main cost driver and we can tune it.
- **Claude API:** roughly **$20–80/mo** at this volume (with prompt caching).
- **Media generation:** depends on how much video. Images are cheap, video costs more.
- **X Premium:** strongly recommended (reach multiplier).

---

## 6. Daily & weekly timeline (example; times set to your audience's timezone)

| Time | What happens | You |
|---|---|---|
| 07:00 | Daily scan → Daily Brief + 4-slot plan + drafts | Approve or edit (5 min) |
| 09:00 | Post 1 (Value) → golden-hour alert | Reply to comments (15 min) |
| 12:00 | Reply-opportunity batch #1 | One-tap replies (5 min) |
| 13:00 | Post 2 (Trend-jack) | Golden hour |
| 16:00 | Post 3 (Visual) + reply batch #2 | Golden hour |
| 19:30 | Post 4 (Conversation) | Golden hour |
| 23:00 | Metrics snapshot + tomorrow's pre-plan | none |
| Sunday | Weekly review → Playbook update → Weekly Report | Read report, make decisions (15 min) |

---

## 7. Build phases

| Phase | What we build | Outcome |
|---|---|---|
| **0. Foundation** | X developer app + OAuth, repo structure, DB, config, guardrails, Telegram bot, positioning doc | Safe connection + clear strategy |
| **1. Intelligence (read-only)** | Daily Scanner + Competitor tracker + outlier analysis + Swipe File | Real data on what works in the niche **before** we post anything |
| **2. Create & Publish** | Planner, Content Generator, Virality Judge, Publisher (approve-first) | 4 quality posts/day on schedule |
| **3. Engagement Copilot** | Reply-opportunity finder, draft replies, one-tap links, golden-hour alerts, relationship map | Reply-driven growth |
| **4. Learning Loop** | Metrics collection, weekly review, Playbook versioning, judge calibration, timing model | Gets better every week |
| **5. Media Studio** | Visual trend tracking, templates, image/video generation | Media posts at scale |
| **6. Autopilot & extras** | Graduate trusted actions to autopilot, profile optimization, recycling, cross-posting | Less of your time, more output |

Each phase is usable on its own. Phase 1 alone already gives you a daily competitive-intel feed.

---

## 8. KPIs

- **North star:** net new followers per week
- Impressions per post (median, not just average; virality is spiky)
- Engagement rate, reply rate, bookmark rate
- Profile-visit → follow conversion
- % of posts beating the account's 4-week median
- Number of "breakout" posts (≥5× median) per week
- Time you spend per day (target ≤ 20 min)

---

## 9. Open questions for you (needed before we build)

1. **What is Evolves Studio?** What do you make or sell, who's the audience, and is the goal followers, clients, or both?
2. **Account basics:** handle, current follower count, and whether it has X Premium.
3. **Are you OK with the API-based approach** (agent posts via API, replies are one-tap by you) instead of the agent driving Chrome?
4. **Autonomy:** should main posts be autopilot from day 1, or approve-first?
5. **Competitors:** any accounts you already know you want to beat or learn from?
6. **Audience timezone(s) and language(s).**
7. **Where do you want alerts and approvals:** Telegram, Slack, WhatsApp, or email?
8. **Monthly budget** for API, models, and media.
9. **Topics to avoid** (politics, etc.) and the brand voice you want (bold/edgy vs. professional vs. playful).
10. **Where to run it:** Claude Code cloud routines + GitHub Actions (no server), or a small always-on VPS?
