# Installing the Reddit agent's scheduled tasks (Claude desktop app)

All times are **IST** (Asia/Kolkata), local to Ishaan's PC. Cron is the standard 5-field format (minute hour day-of-month month day-of-week).
They run on the PC with Chrome open and Claude desktop running (the tasks use Chrome via Claude in Chrome and the local folder `H:\claude\reddit-agent`).

## Before installing
1. Copy this repo's `reddit-agent/` folder to `H:\claude\reddit-agent`.
2. `copy config.example.json config.json`, set `reddit_username` (never committed), keep `warmup_until` = 2026-10-12, set `lead_agent_dir` if different. Telegram is optional.
3. `pip install playwright` (for `tools/make_media.py`; it uses installed Chrome, no browser download).
4. In Claude desktop allow: reddit.com, getfreshleads.io, trends.google.com, api.telegram.org (only if used).
5. Test by hand: `PYTHONIOENCODING=utf-8 python tools/rpack.py packs/EXAMPLE.json --no-send` then `Start-Process packs\EXAMPLE.html`.

## The tasks
| Task name (folder in this directory) | Cron (IST) | When | Prompt |
|---|---|---|---|
| `reddit-agent-day1-research` | none: run ONCE by hand, then disable | Day 1 | `SKILL.md` in its folder |
| `reddit-agent-morning-pack` | `15 10 * * *` | daily 10:15 | `SKILL.md` in its folder |
| `reddit-agent-rising-radar` (17:15) | `15 17 * * *` | daily 17:15 | `SKILL.md` in its folder |
| `reddit-agent-rising-radar` (19:45) | `45 19 * * *` | daily 19:45 | same SKILL, second schedule |
| `reddit-agent-rising-radar` (22:15) | `15 22 * * *` | daily 22:15 | same SKILL, third schedule |
| `reddit-agent-evening-log` | `15 0 * * *` | daily 00:15 | `SKILL.md` in its folder |
| `reddit-agent-weekly-review` | `0 11 * * 0` | Sunday 11:00 | `SKILL.md` in its folder |
If the scheduler cannot hold three times for one task, create three tasks named `reddit-agent-rising-radar-1715`, `-1945`, `-2215` with the same SKILL body.

## How to create each one
Claude desktop -> Scheduled tasks -> New task. Name = folder name, schedule = cron above (timezone IST), prompt = the body of that folder's `SKILL.md` (or place the folder under `C:\Users\<you>\.claude\scheduled-tasks\<name>\SKILL.md`, the same way the x-agent tasks are stored). Working folder: `H:\claude\reddit-agent`.

## Clash check (existing routines)
| Existing | IST | Nearest Reddit task | Gap |
|---|---|---|---|
| Social outreach | 09:00 | morning pack 10:15 | 75 min |
| Lead agent (Reddit leads) | 09:30 and 18:30 | morning pack 10:15 (after its 09:30 run, so it can read the fresh output); radar 17:15 and 19:45 around its 18:30 | 45+ min |
| X agent morning pack | 08:00 | morning pack 10:15 | 135 min |
| Agency leads | 12:30 | none | none |
| X reply radar | 13:00, 18:00, 21:00 | radar 17:15, 19:45 and 22:15 | 45-75 min |
| X evening log | 23:30 | evening log 00:15 | 45 min |
| X weekly review | Sun 10:00 | weekly review Sun 11:00 | 60 min |
All tasks use Chrome. If two overlap in practice, the later one waits: stagger rather than run two Chrome-driving agents at once.

## First week
- Day 1: run `reddit-agent-day1-research` by hand and answer the questions in `memory/weekly/day1-report.md`. Then enable the others.
- Days 2-7 (warm-up): packs contain comments only. About 15-30 minutes a day of pasting and posting by hand.
- 2026-10-12 onward: posts and (where allowed) disclosed offers.
Each task checks `warmup_until` itself; do not change it unless Ishaan decides the account is ready.

## Usage and limits
Browsing uses a lot of plan usage. If you hit limits, drop the rising radar to twice a day (17:15 and 22:15) before touching the morning pack.
