# Viral playbook: every lever we pull (read this on every run)

Algorithm details are in `algorithm.md`, formats in `formats.md`, writing in `writing.md`, and tags in `hashtags.md`.
This file is the checklist that ties them together. Every pack applies it.

## 0. The one-line model
X shows a post to a few people and predicts whether they'll **reply, repost, quote, bookmark, share, dwell, click your
profile and follow**. If they do, it shows the post to more people. Everything below raises those odds or avoids the negatives
(mute, block, "not interested", report, scroll-past).
- X open-sourced its ranking weights in 2023. They're old but still directional: a like counts ~0.5, a repost ~1, a reply ~13.5,
  a profile click ~12, **a reply that the author then engages with ~75**, "not interested" ~−74 and a report ~−369.
  So conversations beat likes, and **you replying to your commenters is the most valuable thing you can do.**

## 1. Profile: turns viewers into followers (do once, then review monthly)
- **Name**: `Ishaan | 3D ads` or `Ishaan | Evolves Studio`. Say what you do in the name field, because it shows next to every reply.
- **Handle**: ideally matches the brand (@creasivestudio doesn't). Changing it keeps followers and posts.
- **Bio formula**: what you make + proof + why follow. Example: "3D ads for PRIME, boAt. Posting what AI can't fake and how creatives get paid."
- **Banner**: a billboard. Your best render plus one line ("3D ads that stop the scroll") plus "free 3D ad every week ↓".
- **Pinned post**: your single best piece of work (a video), or the weekly free-ad giveaway post. Never leave it empty.
- **Profile picture**: your face beats a logo for a personal-brand account (people follow people). Keep it the same everywhere.

## 2. Before posting: the post itself
1. **Hook (line 1)** decides everything. Write 5–10 and pick one. Keep it under 100 chars, specific, with a number or tension.
2. **One idea per post.** Short lines, white space, no filler. The last line is a question or a choice when it fits.
3. **Media on every original post.** 4:5 images (2160x2700 from `make_media.py`) take the most feed space on mobile.
   Ishaan's real renders and videos come before generated images.
4. **Video**: hook in the first second (motion right away, no logo intro), captions burned in (most people watch muted),
   6–45 s, loops if possible. A non-Premium account can post up to 140 s. 16:9 is native, but 4:5 or 1:1 take more screen.
   Upload the video directly to X, never as a YouTube link, and never with another platform's watermark.
5. **Image choices**: a 2–4 image set (for example "which one?" A/B, or before/after) gets replies. Add alt text to every
   image (pack field `alt_text`).
6. **Hashtags**: 1–2, following `hashtags.md`.
7. **No link in the main post.** Put it in a self-reply posted right after.
8. **Polls** (pack field `poll`) get 2–3× the reach of plain posts because one tap counts as engagement. Use them for
   "which is better" debates. Polls can't carry an image.
9. **Threads**: put the full value in post 1. Every part should stand on its own, and the last part asks a question
   or points back to the work.
10. **Tagging**: tag a brand in a spec ad made for that brand (brands repost these). Never tag big accounts just to beg for attention.

## 3. Timing and cadence
- **2–4 posts a day, at least 3 h apart** (the same author's posts decay in a viewer's feed). Never burst.
- Slots (IST): 09:30 (India + Europe), **18:30 (US morning + India evening: the best slot)**, 21:30 (US lunch).
- **Don't post and leave.** Only post when you can stay for the next 30–60 minutes (see §4).
- Don't delete posts that flop, and don't repost the same text. Rework it with a new hook a week later.

## 4. The golden hour (the highest-value 30–60 minutes of the day)
- Reply to **every** comment in the first hour, quickly. Ask a follow-up question so the thread keeps going.
  The pack drafts likely replies in `golden_hour_replies`.
- Like the good comments. Pin your own self-reply if it adds value.
- While you wait, do 5–10 replies from the reply radar. Being active on X while your post is live helps it.

## 5. Reply-guy system (main growth lever below about 1–2k followers)
- **20–30 quality replies a day** under accounts 10–100× bigger in the arena, plus viral posts from outside it.
- Be one of the **first 10 replies**, ideally within 15–30 min of the post. Turn on post notifications (the bell) for
  the 10–15 core-watchlist accounts so you see their posts first.
- Every reply adds something real: a number, an experience, a counterpoint or a joke. No "great post!", no self-promo,
  no hashtags. Lead with the point, under 200 chars.
- A **visual reply** (a quick render or card that answers the post) is the highest-stopping reply there is.
- Reply to the replies under big posts too: those threads are where the conversations happen.
- Build relationships with 10–20 peers at your size. Reply to each other's work genuinely (not as a pod; see §9).

## 6. Quotes and remixes
- Quote a viral post only when you add a take, a breakdown or a remix ("recreated this in 3D").
  A quote shows on your profile AND under the original's quote count.
- **Recreate the viral**: rebuild a viral video, meme or ad in 3D within 24–48 h. Post it natively, quote the original
  and reply under the original with the clip. This is the format most likely to break out.

## 7. Viral bridges (the core game)
Anything viral, in or out of the niche, gets connected to creatives and freelancers. Process and skip rules are in `formats.md`.
Speed matters: a bridge posted while the trend is rising beats a better one posted after it peaks.

## 8. Built-in reach multipliers
- **X Communities**: community posts can now show up in the main feed and in recommendations. Ishaan joins these once
  (see the list below), then cross-posts relevant work there. The pack names one community per post (`communities`: first = use this, second = backup). One post can go to ONE community only; never post the same text twice.
- **Recurring series**: numbered formats compound, because people follow to get the next one
  ("Free 3D ad #3", "Recreating viral ads in 3D, part 4").
- **The free-ad giveaway** (the bio already promises one a week): "reply with your brand, I'll make one a free 3D ad."
  It's a reply magnet: every brand that replies is a lead, and the finished ad is proof content. Pin it.
- **Spec ads for trending brands**: tag the brand. Fans of the brand repost.
- **Spaces**: co-host or speak in freelance and creative Spaces once the account has a few hundred followers.
- **Premium decision**: Premium adds a reply boost, edit, longer posts and analytics. With replies as the main lever,
  even the cheapest tier's reply boost could help. This is Ishaan's call (it's a cost); the weekly review notes the
  evidence if growth stalls.

## 9. What kills reach (never)
- Links in the main post · 3+ hashtags · posting 10+ times a day · reposting the same text · deleting and re-uploading
- Follow/unfollow churn, engagement pods, buying followers or engagement, mass tagging, copy-paste replies.
  These count as platform manipulation and can get the account suspended.
- Bots or any automation of posting, liking or replying (`algorithm.md`, "Automation rules")
- Self-promo replies, trend-hijacking with unrelated tags, and rage bait about tragedies or politics
- Other platforms' watermarks, low-effort AI images with obvious tells, and walls of text without line breaks

## 10. Measuring (evening log + weekly review)
- Per post: views at 1 h / 24 h, replies, reposts, bookmarks, profile clicks (when visible), **new followers that day**.
- Views per follower and follows per 1k views tell you whether a post converts or is only seen.
- Double down on any format that hit 3× our median twice. Drop anything below median three times in a row.

## X Communities (Ishaan JOINED these on 2026-10-05: don't put 'join communities' in checklists anymore)
| Community | Members | Use for | Link |
|---|---|---|---|
| The Design Sphere | 668K | design, brand, logo, creative takes | https://x.com/i/communities/1453877367030484992 |
| Generative AI | 254K | AI vs 3D, AI video takes | https://x.com/i/communities/1601841656147345410 |
| Startup Community | 193K | studio business, build in public, D2C | https://x.com/i/communities/1471580197908586507 |
| Memes | 517K | meme-format viral bridges | https://x.com/i/communities/1669501013441806336 |
| Branding & Brand Design | 26K | ad critiques, logos, spec ads | https://x.com/i/communities/1506780333034782720 |
| Ai community | 27.5K | AI tools takes | https://x.com/i/communities/1750982865117204723 |
| Blender | 17.7K | renders, breakdowns, #b3d | https://x.com/i/communities/1471902001629904896 |
| Motion Design | 6.4K | animation, motion work | https://x.com/i/communities/1510265079274557456 |
| Freelance Starters | 7.1K | freelance lessons | https://x.com/i/communities/1508982079245021185 |
| Freelance India | 3.7K | India freelance angle | https://x.com/i/communities/1868675400890769529 |
| AI Video & Filmmakers | 2.4K | AI video vs 3D | https://x.com/i/communities/1864486263094411711 |
