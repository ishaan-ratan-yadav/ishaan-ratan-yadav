# Daily Reddit lead run (Claude Code, Max plan, no API key)

Work in `H:\claude\reddit  scrap`. DATE = today, YYYY-MM-DD.

Read `STYLE.md` first. Every reply, DM and post you write must follow it (no AI-sounding text).

0. PRIORITY, the inbox: run `python reddit_agent.py --inbox`. Read `output/inbox-DATE.json`.
   Each item is someone who replied to our comment, mentioned us or messaged us. `context` holds their
   original post and what we replied. For each item:
   - `interest`: hot (asks what we do, price, samples, "DM me", "how do you find these") | warm (thanks, follow-up
     question, shares their situation) | cold (just agreeing) | none (spam, argument, bot).
   - `interest_score`: hot 10, warm 9, cold 7. Skip `none` (no draft).
   - `why`: one line on what they're interested in, based on their words and their original post.
   - `draft`: the reply. Hot: answer exactly what they asked, then offer 5 free sample leads in THEIR niche and
     ask 1 qualifying question (what they sell, to whom). Warm: keep helping on their specific problem, end with a
     question that invites them to share more; if a product mention is natural, mention it in one line.
     Cold: short friendly one-liner or no draft. Warm-up rules do NOT block answering someone who asked what we do.
   - `dm` (hot only): a private message that continues from the public thread, mentions what they said, offers the
     samples. Once they say yes: ask for niche + what they sell, then the user sends samples from FreshLeads.
   Put these in `inbox` in the leads JSON (step 5). They show at the top of the checklist.
   If `--inbox` prints "REDDIT_INBOX_FEED not set", note it in the final message and continue.
1. Run `python reddit_agent.py --scrape` (1-5 min). It writes/merges `output/posts-DATE.json`.
   If it reports 0 new posts, skip to step 6 and say so.
2. Read `config.json` (product, subreddits, `no_promo_subreddits`) and `output/posts-DATE.json`.
   If `output/leads-DATE.json` exists (second run today), keep its leads and only score posts not already in it.
3. Score every post 0-10: "is this author realistically a paying FreshLeads customer soon?"
   - 9-10: asks for leads / lead lists / how to find D2C or ecommerce clients / complains about Apollo, ZoomInfo, bounces, lead quality / hiring someone for lead gen
   - 7-8: runs an agency or freelances for D2C/ecommerce brands (email, Klaviyo, ads, CRO, design, UGC, 3D, dev) and struggles with pipeline, outbound or finding clients
   - 4-6 adjacent (general marketing chat, non-D2C B2B); 0-3 irrelevant (job seekers, vendors pitching, memes)
   - Be strict. People selling lead gen themselves are competitors: score <= 3.
   WARM-UP: if today is before `warmup_until` in config.json, the account is new/low karma. Then:
   NO product mention or link in any reply (set `"no_promo": true` on all), NO `dm`, and also add up to
   8 extra `leads` scoring 5-6 with `"intent": "karma"`: easy-to-answer questions in r/agency, r/Emailmarketing,
   r/coldoutreach, r/LeadGeneration, r/klaviyo where a short expert answer earns upvotes. Give those `ai_score` 7
   so they show on the page. Goal: ~150 karma + a visible history of helpful comments before promo starts.
4. For every post scoring >= 7 write:
   - `reply`: 50-150 words. First give real, specific help that answers their post (tactics, numbers, what works for D2C outreach: founder inbox not info@, a dated trigger like a launch/funding/retail deal, 3-line emails, etc.).
     Then, only if it fits naturally, one line near the end with disclosure, e.g. "full disclosure, I run getfreshleads.io which does exactly this for D2C brands, happy to send a few free samples". Vary the wording every time.
     If the subreddit is in `no_promo_subreddits`: NO product mention and NO link; set `"no_promo": true`.
     No emojis, hashtags, bullet walls, "Great question", or em dashes. Sound like a real practitioner. Match the sub's tone.
   - `dm` (only if score >= 8): 2-3 sentences, reference their exact post, offer 5 free sample leads in their niche. No link in the first DM.
   - `intent`: buying | problem | discussion. `why`: one sentence.
4b. VISIBILITY (karma, followers, profile clicks): posts with `source` starting "rising:" are climbing right now.
   Pick the 3-5 with the most discussion potential in our niche (outbound, agencies, ecommerce growth, founders),
   even if the author isn't a buyer. Write a comment built to become the TOP comment:
   - add something the post is missing: a sharp counterpoint, a specific number or tool, or a short "what actually
     worked for me" story. Agreeing-plus-nothing never gets upvoted.
   - first line is the whole point (people skim), 30-90 words total, zero promo, zero link, follows STYLE.md.
   - where natural, end with a question that makes others reply to you.
   Add them to `leads` with `"intent": "RISING"`, `ai_score` 8, `no_promo` true, `why` = why this comment can win.
   Prefer rising posts in subs listed in config `post_requirements` (we need comment history there before we can post).
   Also add 0-2 `growth_tasks` (short strings) if something specific stands out today, e.g. a trending topic worth
   a post ("r/agency is buzzing about X, ask Claude to turn it into a post"). They show in the routine box.
5. Write `output/leads-DATE.json`:
   ```json
   {"stats": {"scanned": N},
    "inbox": [ {...inbox item fields..., "interest": "hot", "interest_score": 10, "why": "...", "draft": "...", "dm": "..."} ],
    "leads": [ {...post fields from posts file..., "ai_score": 9, "intent": "...", "why": "...", "reply": "...", "dm": "...", "no_promo": false} ],
    "insights": ["3-5 short bullets: recurring pains, tools people complain about, exact phrases prospects use (useful for landing page + ads)"],
    "value_posts": []}
   ```
   On Mondays (or if `value_posts` is empty all week) add 1-2 `value_posts`: {"subreddit", "title", "body"} —
   an original, genuinely useful post for r/agency, r/LeadGeneration or r/coldoutreach (e.g. "What I learned pulling 500 D2C founder emails by hand", "The 3-line cold email that gets D2C founders to reply"), 200-400 words, no link in body, founder voice. These build the profile that makes DMs convert.
   Give each value post a `"flair"` list of likely flair names in priority order (e.g. ["Guide", "Tips", "Discussion"]).
   Never invent stats or results. Where a real number is needed write a placeholder like [YOUR REPLY RATE] for the user to fill in.
6. Run `python reddit_agent.py --digest output/leads-DATE.json --open`.
7. Final message: inbox items (hot/warm count, names of hot ones first), posts scanned, leads found, top 3 lead titles with score, and the HTML path.

Never post, comment, vote or DM on Reddit yourself. The user does all posting manually.
