# Task 03: Evening log (daily, ~23:30 IST)

Budget: ~25 X page loads.

1. Open our X profile. For every post/reply/quote Ishaan published in the last ~72 h, read the public counters
   (views, replies, reposts, quotes, likes, bookmarks) and the follower count on the profile.
2. Update `memory/post-log.csv`: match posts to the pack entries (by text) so each row keeps its tags
   (pillar, format, hook_type, slot, hypothesis, score). Record a checkpoint row per post: `h24`, `h72`
   (use the closest checkpoint to the post's age). Record today's follower count in the `followers_eod` column of a
   `type=daily` row.
3. Update `memory/reply-log.csv`: which drafted replies were posted, and their views/likes/replies.
4. Note anything that's breaking out (≥3× our median views) → Telegram alert: "P2 is taking off, reply to comments now."
5. Write 3 bullet "today's lessons" at the bottom of `memory/experiments.md` (data, not opinions).
6. Skipped posts: note them (Ishaan didn't post) so the weekly review doesn't count them as failures.
