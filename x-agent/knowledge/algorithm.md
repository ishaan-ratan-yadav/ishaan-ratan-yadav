# How X ranks posts (researched 2026-10-02)

## Source of truth: xai-org/x-algorithm (open source, Jan 2026, big update May 2026)
- A Grok-based transformer ("Phoenix") predicts, per viewer, the probability of ~19 actions:
  - **Positive:** like, reply, repost, quote, share, share via DM, copy link, click (post, profile, link, photo,
    video, quoted post), video quality view, dwell, dwell time, active seconds, **follow author**.
  - **Negative:** not interested, mute author, block author, report, not dwelled (scrolled past).
- `Final score = Σ weight × P(action)`. Weights multiply *probabilities*, not raw counts.
- After scoring:
  1. **Author diversity:** each extra post by the same author in a viewer's feed is multiplied by a decaying factor (to a floor).
     → space posts ≥ 3 h apart; never burst.
  2. **Out-of-network discount:** non-followers see you at a discount. → replies under big accounts + breakout-quality posts are how new people find you.
  3. **New/low-impression author boost:** small accounts get lifted toward a target position. → good for us now; use it.
- Candidates: "Thunder" (recent posts from accounts you follow) + Phoenix embedding retrieval / SimClusters (topic similarity).
  → Stay topically consistent so the model knows who to show us to. Random off-topic posts confuse the embedding;
    that's why every viral bridge must land back in our arena.

## Practical findings (industry analyses, 2026: directionally right, numbers approximate)
- Conversation beats likes: replies, and especially **the author replying to replies**, are among the strongest signals.
- Early velocity (first 30–60 min) strongly affects distribution → golden hour: Ishaan replies to every comment fast.
- **Links in the main post are heavily suppressed**, reportedly near-zero for non-Premium accounts since Mar 2026.
  → Link always goes in a self-reply.
- **Premium accounts get several times more reach.** We are NOT Premium → we must win on hooks, replies and media.
  Revisit Premium if growth stalls (weekly review decides).
- Hashtags: 1–2 relevant tags beat 0 and 3+ (2026 analyses). The semantic model finds topics anyway, but community
  hashtag feeds (#b3d, #freelance) have real people browsing them. Rules in `hashtags.md`. (Updated 2026-10-04.)
- Native video and images lift dwell and "video quality view". 3D motion is our unfair advantage.
- Generic best times: weekdays, audience morning to early afternoon. Our audience is global (US-heavy on X) + India.
  Use own data after ~2 weeks (`memory/schedule.md`).

## Non-Premium limits that affect formats
- 280 weighted chars per post (emoji/CJK = 2, any URL = 23). No long posts, no Articles, no edit button.
  → Use threads (reply chains) for depth. Pack page lists thread parts in order.
- Analytics dashboard is Premium-only. Public counters on each post (views, replies, reposts, likes, bookmarks)
  are still visible → that's what we log.

## Automation rules we stay inside
- X automation rules: scripting the website "may result in permanent suspension". Programmatic replies via API are
  restricted (since 23 Feb 2026). X is suspending accounts for AI reply automation (2026).
- Therefore: the agent only reads; Ishaan posts every post/reply/quote by hand via intent links.
- AI-drafted text is fine when a human reviews and posts it, but it must not *read* as AI (see `writing.md`).
