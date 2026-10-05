---
name: reddit-agent-rising-radar
description: Finds fresh (<90 min) rising threads in target subs and viral threads elsewhere on Reddit, drafts 2-3 top-comment options each for the FreshLeads account, builds a mini pack and opens it
---

Working folder: H:\claude\reddit-agent (cd there first). Read CLAUDE.md, then run tasks/02-rising-radar.md exactly.

Key context:
- Read Reddit ONLY through Claude in Chrome (mcp__claude-in-chrome__* tools, loaded in one ToolSearch call; own tab, close when done). If Chrome isn't connected, use public RSS (/r/SUB/rising/.rss) and say so, or stop.
- NEVER click Post/Comment/Reply/Vote/Join/Follow/Send or type into Reddit. Human pace, at most 30 Reddit page loads. Stop on captcha/rate-limit/login prompts.
- Where to look: /r/SUB/rising and /new for the Tier A subs in memory/subreddit-intel.md, the strict subs (r/sales, r/Entrepreneur, r/shopify, r/ecommerce) for comment-only sniping, then r/popular and r/all Rising for viral bridges. Threads under 90 minutes old win. READ the thread (OP + top 3 comments) before writing; never write from the title alone.
- Each comment adds something real (a number, counterpoint, short story), 30-90 words, first line is the whole point. One comment per thread, 10+ min gap per sub. WARM-UP until 2026-10-12: no product, no link. No product in help-only subs ever. Follow knowledge/writing.md (no em dashes, emojis, hashtags, AI-isms).
- Skip threads the lead agent already drafted for (H:\claude\reddit  scrap\output\leads-*.json, leads_log.csv) or that memory/comment-log.csv shows we handled. Never modify the lead agent.
- Also check our latest post/comments for unanswered replies and draft replies as inbox items (golden hour).
- Write packs/YYYY-MM-DD-HHMM.json, build with: PYTHONIOENCODING=utf-8 python tools/rpack.py <file> --no-send, fix every BLOCKER/warning, open with PowerShell Start-Process on the HTML. Append targets to memory/comment-log.csv (status drafted).
