# Task 04: Weekly review (Sunday ~11:00 IST)

This is the part that makes the agent better every week. Be rigorous; small samples lie. Budget: ~40 Reddit page loads (refresh metrics, spot-check subs), human pace, read-only.

## 1. Collect
- Final metrics for all posts and comments of the last 7 days (refresh anything younger than 72 h) into `post-log.csv` / `comment-log.csv`.
- Daily rows from `karma-log.csv`: comment karma, post karma, followers, DMs, sample requests, removals, shadowban checks. Net karma and net followers this week. **Qualified conversations this week = north star** (DMs/chat requests + sample requests from relevant people).
- The lead agent's results this week (read `leads_log.csv` and outputs: how many of our attention-driven threads produced inbox items?).
- Rising-radar hit rate: of drafts posted, how many scored above our median; how many were top comments.

## 2. Analyse
- Rank posts and comments by score, comments, score per hour, and conversion (DMs/followers within 24 h).
- Break down by sub, pillar, format, hook type, slot (IST/ET), media vs text, early (<90 min) vs late, bridge vs niche, 70/20/10 bucket. Report sample sizes. **A pattern needs >=3 items before it's "proven".**
- Compare with this week's outliers in the target subs: what did winners do that we didn't? Add to `memory/swipe-file.md`; refresh its top patterns.
- Check each experiment in `memory/experiments.md`: confirmed / rejected / needs data.
- **Health:** any removals, warnings, modmail, rate-limit messages? Any sudden drop in score per comment across subs (possible filter)? Run the logged-out visibility check. Review each removal: which rule, which trigger; fix `memory/subreddit-intel.md`.
- Warm-up gate: has the account reached the karma/history goals for each target sub? Which subs are now postable?

## 3. Decide
- **Double down** on patterns that won -> move to the 70% bucket in the playbook.
- **Iterate** near-misses -> variations next week (20%).
- **Kill** patterns that lost twice. **New bets:** 2-3 wild ideas from the swipe file/trend log (10%).
- **Subs:** promote/demote/add/drop subs in `memory/subreddit-intel.md` and `knowledge/subreddits.md` (keep >=6 active comment subs, add 2-3 candidates from new sightings, drop dead or hostile ones). Re-verify rules for any sub with a removal or a `?` still open.
- **Cadence:** update `memory/schedule.md` (comments/day, posts/week, slots) from the data. Raise only if per-item medians held; lower if quality dropped. Never exceed safe limits (CLAUDE.md).
- **Funnel:** is anything converting? Which format/sub brought DMs? Adjust the offer wording (free samples) and the pinned post/bio. Promo share must stay <=10%.
- **Warm-up ended?** If today is past `warmup_until`, plan the first promo-eligible items (disclosed, only in subs whose intel row allows) and say which.

## 4. Write
- `memory/playbook.md`: bump version, add/remove rules with evidence (links and numbers), keep a changelog.
- `memory/experiments.md`: next week's hypotheses.
- `memory/weekly/YYYY-MM-DD.md` report: headline numbers vs last week (karma, followers, conversations), top 3 items and why, flops and why, health, what changes next week, the week's post calendar (subs, titles, slots), profile tweaks, and **decisions needed from Ishaan** (time per day, offer wording, facts/numbers we may cite, mod messages to answer by hand).
- Telegram (if configured): 8-line summary + path. Open the report: `Start-Process "H:\claude\reddit-agent\memory\weekly\<file>.md"`.

## 5. Monthly (first Sunday of the month)
Review positioning and pillar mix, profile (bio/pinned post) A/B result, the arena definition, and whether Reddit Pro (Reddit's free business analytics surface) is worth Ishaan setting up for profile/post analytics.
