# Task 02: Reply radar (daily, 12:30 / 18:00 / 21:00 IST)

Replies under bigger accounts are how new people discover us (out-of-network reach) and build relationships.
Early replies (first 15–30 min of a post's life) get the most visibility. Budget: ~30 X page loads, human pace.

1. Read `CLAUDE.md`, `knowledge/writing.md` (reply rules), `memory/creators.md`, today's pack.
2. Check the core watchlist + X search (Latest, our arena keywords) for posts **< 45 min old** with early traction,
   from accounts with ≥5× our follower count (and a few peers we're building relationships with).
3. Also check viral posts outside the arena where a creative/3D angle would stand out (the bridge game).
4. Check **our own latest post**: any unanswered replies? Draft responses (Ishaan answering every reply in the first
   hour is one of the strongest ranking signals).
5. Pick the best 6–10 targets. For each, 3 reply options. Skip if we can't add real value.
6. Optional: 0–1 quote post if something viral is squarely in our arena.
7. Write `packs/YYYY-MM-DD-HHMM.json` with `replies` (+ `quotes`), run `python tools/xpack.py` on it,
   open the HTML with Start-Process, Telegram sends the one-tap reply links.
8. Append targets to `memory/reply-log.csv` (status `drafted`).

Rules from knowledge/viral-playbook.md §5: be in the first 10 replies, add something real, no hashtags and no self-promo in replies, and suggest a visual reply (render/card) on the 1–2 best targets.
