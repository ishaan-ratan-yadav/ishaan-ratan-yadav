# FreshLeads Reddit Growth Agent

A growth agent for Ishaan's Reddit account (FreshLeads, https://www.getfreshleads.io). It reads Reddit every day through your logged-in Chrome,
finds what is rising (in our niche and everywhere else), reads each subreddit's real rules, and prepares everything: top-comment drafts for rising threads,
value posts, infographics, replies for your own threads, DM follow-ups, and a one-page checklist. It also logs what worked and gets better every week.

**It never posts, comments, votes, joins or messages.** Everything arrives as a page of copy buttons. You paste and click Post.
Reddit shadowbans and permabans automated posting, voting and spam rings, and one banned account would also kill the lead agent's inbox funnel.
So the agent does 100% of the work except the final click.

It is the growth twin of the X agent (`../x-agent/`) and sits beside the existing Reddit **lead** agent (`reddit  scrap`), which keeps owning buyer-lead replies and DMs.
This agent owns **karma, profile authority, original posts, top-comment sniping on rising threads, viral bridges, AMA/teardown/free-offer threads, and turning attention into DMs and sample requests.**

Runs on: **Claude Desktop + Claude in Chrome**, using your Claude subscription. No Reddit API, no paid tools.

## How a day looks (IST)

| IST | Agent | You |
|---|---|---|
| 10:15 | Morning pack: scans, plans, writes; the Daily Pack opens in Chrome | skim the brief (2 min) |
| 17:15 / 19:45 / 22:15 | Rising radar: fresh threads (<90 min) + 2-3 comment options each; mini pack opens | tap **Copy comment + open thread** -> paste -> Post (10+ min apart per sub, the timer shows it) |
| 16:00-17:30 or 18:30-19:30 (post days) | | **Copy title + open submit page** -> paste body, flair, image -> Post -> stay 60-120 min and answer every comment |
| any time | | inbox replies and DM follow-ups from the pack |
| 00:15 | Evening log: reads your profile, posts, comments, inbox, removals; logs karma, followers, DMs | none |
| Sun 11:00 | Weekly review: what worked, playbook update, subs added/dropped, report | read the report (10 min) |

About **15-30 minutes a day** in warm-up (until **2026-10-12**: comments only, no product, no links, no DMs), more on post days for the golden hour.

## Setup (one time, ~20 min)

### 1. Apps
1. A paid Claude plan. Daily browsing uses plenty of usage: if you hit limits, run the rising radar twice a day instead of three times.
2. **Claude Desktop** installed and signed in. **Claude in Chrome** extension signed in with the same account.
3. In Chrome, be logged in to Reddit (the account you want to grow).

### 2. This folder
1. Copy the repo's `reddit-agent/` folder to `H:\claude\reddit-agent`.
2. Python 3 + `pip install playwright` (only for infographics; it uses the Chrome you already have).
3. Copy `config.example.json` to `config.json`. Set `reddit_username` (this file is git-ignored; the username never goes into the repo), keep `warmup_until`, and check `lead_agent_dir` points at the lead agent folder.
4. Optional Telegram: create a bot with @BotFather, paste `telegram_bot_token` and `telegram_chat_id`. Without it, packs just open in Chrome.
5. Test: `PYTHONIOENCODING=utf-8 python tools/rpack.py packs/EXAMPLE.json --no-send`, then `Start-Process packs\EXAMPLE.html`.

### 3. Day 1: research (run once, by hand)
In Claude Desktop: **"Read CLAUDE.md and run tasks/00-day1-research.md."**
It audits the account (karma, history, profile), reads the rules of 25-40 subreddits, builds the swipe file from top posts, writes `memory/weekly/day1-report.md` with questions for you, and builds the first pack.
Answer the questions (pricing, which numbers you are happy to cite, how you like to disclose the product) and fix the profile (bio, pinned intro post, link) by hand.

### 4. Day 2 onwards: schedule the routines
Follow `scheduled-tasks/INSTALL.md` (names, cron times, no clashes with the X agent, lead agent, social outreach and agency-lead routines). If your PC was asleep, run any missed task by hand; the morning pack and the rising radar matter most.

## Your part, every day
1. Open the pack (it opens itself). Rising comments are first.
2. For each: read the thread for 20 seconds, pick an option, **Copy comment + open thread**, edit if it doesn't sound like you (the text boxes are editable), paste, Post, tick Done. Respect the timer.
3. On a post day: copy title, open the submit page, paste the body, set flair, attach the image, Post. Then stay and answer every comment (ready replies are under the post).
4. Reply to inbox items; send DM follow-ups only to people who asked.
5. Never ask anyone to upvote, never use another account, never reply to yourself. If a sub or mod tells you something, tell the agent (it logs it).

Keys on the pack page: **Enter** main action of the selected card, **1-4** pick comment option N, **D** done, **S** skip, **J/K** move, click any text to edit before copying. Done boxes and the comment-gap timer are remembered in your browser.

## What gets measured
North star: **qualified conversations per week** (DMs/chat requests and sample requests from relevant people), with weekly **karma** and **followers** as the supporting numbers.
Reddit does not show profile visits, so the agent tracks what is visible: karma, followers, scores at +1 h/+24 h/+72 h, comment rank, inbox and chat requests, removals, and a logged-out visibility check.

## Files
- `CLAUDE.md`: the agent's rules and map. Start here.
- `tasks/`: the five routines (Day 1, morning pack, rising radar, evening log, weekly review).
- `knowledge/`: `algorithm.md` (ranking, gates, shadowbans, self-check), `viral-playbook.md` (every lever), `formats.md`, `writing.md`, `subreddits.md` (researched sub table with sources).
- `memory/`: everything the agent learns: positioning, playbook, subreddit-intel (live rules), swipe file, trend log, post/comment/karma logs, experiments, schedule, weekly reports.
- `tools/rpack.py`: builds the pack page and checks every title, post, comment and reply (length, links, warm-up, promo share, emojis, hashtags, dashes, AI-isms, flair, sub rules from `memory/subreddit-intel.md`). `--check "text" --sub agency` checks one comment.
- `tools/make_media.py`: premium 3D infographics (`inbox`, `bars`, `five-buyers`, `statement`; 1080x1350 and 1200x628). `media/examples/` has samples.
- `packs/`: daily packs. `packs/EXAMPLE.json` shows the format; `packs/2026-10-05-sample.json` is a sample built from live research.
- `scheduled-tasks/`: one `SKILL.md` per routine plus `INSTALL.md`.

## Safety rules the agent follows
It only reads Reddit, at a human pace, and never clicks Post/Comment/Reply/Vote/Join/Follow/Send or types into Reddit. It treats anything on a web page as data, not instructions.
It never mentions the product before warm-up ends, never in help-only subs, keeps promo at or under 10%, never invents facts or numbers, never trend-jacks tragedy or politics, and never asks for votes.
Full list in `CLAUDE.md`.
