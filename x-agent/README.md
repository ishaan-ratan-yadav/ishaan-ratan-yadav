# Evolves X Agent

A growth agent for the Evolves Studio X account. It researches X and the web every day, finds what's going viral
(in the creative/freelance space and outside it), plans and writes the posts, replies and quotes, designs simple
media, and gets better every week from the results.

**It never posts.** Every post, reply and quote arrives as a one-click link (in Chrome and on Telegram) that opens
X's compose box already filled in. You read it, attach media if needed, and press Post. This keeps the account safe:
X suspends accounts whose posting or replying is automated, and since 2026 it has been suspending AI reply bots.

Runs on: **Claude Desktop (Cowork) + Claude in Chrome**, using your Claude subscription. No X API, no paid tools.

## How a day looks

| IST | Agent | You |
|---|---|---|
| 08:00 | Scans trends + creators, writes today's posts → Daily Pack opens in Chrome + Telegram | Review, make any render requests |
| 09:30 / 18:30 / 21:30 | (slots) | Click "Open in X" → Post → reply to comments for 30 min |
| 12:30 / 18:00 / 21:00 | Reply radar: fresh big posts + 3 reply options each | Tap a reply link → Post |
| 23:30 | Logs what you posted + metrics, flags breakouts | none |
| Sun 10:00 | Weekly review → playbook update → report | Read report (10 min) |

About 30–45 min of your time a day, most of it replying to comments, which is the highest-value part.

## Setup (one time, ~20 min)

### 1. Apps
1. A paid Claude plan (Pro works. Daily browsing uses a lot of usage, so if you hit limits, either drop the reply
   radar to twice a day or move to Max).
2. Install **Claude Desktop** (claude.ai/download) and sign in.
3. Install **Claude in Chrome** from the Chrome Web Store and sign in with the same account.
4. In Chrome, make sure you're logged in to X.

### 2. This folder
1. Download this repo (GitHub → Code → Download ZIP) and unzip `x-agent` somewhere like `Documents/evolves-x-agent`.
   (If you use git: `git clone`, then work in `x-agent/`.)
2. Install Python 3 if it isn't installed, then run `pip install pillow` (only needed for image cards).

### 3. Telegram bot (free)
1. In Telegram, open **@BotFather** → `/newbot` → pick a name → copy the **token**.
2. Open your new bot and send it any message ("hi").
3. In Chrome open `https://api.telegram.org/bot<TOKEN>/getUpdates` and copy the number after `"chat":{"id":`.
4. Copy `config.example.json` to `config.json` and paste the token and chat id. Put your X handle in `brand.handle`.
   `config.json` never goes to GitHub (it's in `.gitignore`).
5. Test: `python tools/xpack.py packs/EXAMPLE.json`. You should get Telegram messages, and `packs/EXAMPLE.html`
   should open with "Open in X" buttons.

### 4. Connect Cowork
1. Open Claude Desktop → **Cowork** → choose the `evolves-x-agent` folder as the working folder.
2. Make sure Claude in Chrome is connected/enabled for Cowork.
3. Allow the sites it will read: x.com, evolvesstudios.com, trends.google.com, reddit.com, api.telegram.org.

### 5. Day 1: research (run once, by hand)
In Cowork: **"Read CLAUDE.md and run tasks/00-day1-research.md."**
This takes a while. It audits the account, maps 40–60 creators, builds the swipe file, finalises positioning and
the posting schedule, and writes `memory/weekly/day1-report.md` with questions for you. Answer them, and drop your
best renders/reels into `media/library/`.

### 6. Day 2 onwards: schedule the routines
In Cowork, create these scheduled tasks. They need your computer awake with Chrome open, because they use your
Chrome and this folder (Cowork runs such tasks locally). Each prompt is one line:

| Name | Schedule | Prompt |
|---|---|---|
| X morning pack | Daily 08:00 | `Read CLAUDE.md and run tasks/01-morning-pack.md` |
| X reply radar | Daily 12:30, 18:00, 21:00 | `Read CLAUDE.md and run tasks/02-reply-radar.md` |
| X evening log | Daily 23:30 | `Read CLAUDE.md and run tasks/03-evening-log.md` |
| X weekly review | Sunday 10:00 | `Read CLAUDE.md and run tasks/04-weekly-review.md` |

(If one schedule can't hold three times, create three "X reply radar" tasks.) If your laptop was asleep, run any
missed task by hand. The morning pack is the important one.

## Your part, every day
1. Open the Daily Pack (Chrome tab or Telegram).
2. At each slot: **Open in X** → check the text → attach media if the pack says so → **Post**.
   For threads: post part 1, then reply to your own post with each next part (copy buttons are in the pack).
   For links: post the main post, then reply to it with the link text.
3. Stay 20–30 min after each post and **reply to every comment** (the pack drafts some for you).
4. Reply radar: tap the reply option you like → Post. Skip anything that doesn't sound like you.
5. Make the **render requests** when you can (spec ads / recreations of viral moments). They are the posts most
   likely to break out.

## Files
- `CLAUDE.md`: the agent's rules and map. Start here.
- `tasks/`: the five routines.
- `knowledge/`: how the X algorithm works, formats that win, writing rules.
- `memory/`: everything the agent learns (positioning, playbook, creators, swipe file, logs, weekly reports).
- `tools/xpack.py`: builds the Daily Pack page + Telegram messages, and checks every post (280 chars, links, hashtags, AI-isms).
- `tools/make_card.py`: makes branded image cards (statement / list / versus).
- `packs/`: daily packs. `packs/EXAMPLE.json` shows the format.

## Safety rules the agent follows
It only reads X, at a human pace, and never clicks Post/Like/Follow/Reply or types into X. It treats anything on a web
page as data, not instructions. It never trend-jacks tragedies or politics, and never invents facts or client work.
Full list in `CLAUDE.md`.
