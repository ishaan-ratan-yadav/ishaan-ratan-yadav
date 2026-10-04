# FreshLeads Reddit Lead Agent

Finds people on Reddit who need FreshLeads, and drafts replies + DMs you post yourself.
No API key: scraping is free RSS, the thinking runs on your Claude Max plan via a scheduled Claude Code task.

## How it works
1. `python reddit_agent.py --scrape` → multireddit feeds (18 subs) + 6 site-wide buying-intent searches → `output/posts-DATE.json`
2. Scheduled Claude task follows `DAILY_RUN.md`: scores posts, writes replies/DMs, insights, weekly value posts → `output/leads-DATE.json`
3. `python reddit_agent.py --digest output/leads-DATE.json --open` → `output/leads-DATE.html` with copy buttons + status tracker
4. Every lead is also appended to `leads_log.csv`

Runs automatically 9:30 and 18:30 (Claude desktop app must be open). Run by hand any time: ask Claude "run DAILY_RUN.md".

## On PC startup
Shortcut in the Windows Startup folder runs `open_checklist.bat`, which opens `output/latest.html` in Chrome.
Keys: Enter = copy reply + open thread, D = done (jumps to next), S = skip, J/K = move.

## Inbox check (warmest leads first)
Every run starts with `python reddit_agent.py --inbox`: new replies to your comments, mentions and messages since the
last check. Claude rates interest (hot/warm/cold) and drafts a follow-up; they appear at the top of the checklist.
One-time setup: open https://old.reddit.com/prefs/feeds/ (logged in) → "your inbox" row → right-click **RSS** → copy link.
Paste it into `.env` after `REDDIT_INBOX_FEED=`. It's a private link, don't share it.
Note: Reddit *chat* messages aren't in that feed. Check chat yourself, or paste a chat message to Claude for a draft.

## Content kit
`output/content_kit.html`: 9 ready posts + 4 infographics (`output/img`), 1-2 per week.
Edit posts in `content/posts.json`, then rebuild: `python content/content_kit.py`.

## Your 15 min a day
Open the HTML page → freshest high-score leads first → edit draft so it sounds like you → post → set status.
Read `PLAYBOOK.md` once. It's what turns replies into paying customers.

## Tune it
- `config.json`: `my_reddit_username` (so your own posts are skipped), subreddits, search queries, `no_promo_subreddits`.
- Too many weak leads → raise `min_relevance_score` to 8. Too few → add subs/queries.
