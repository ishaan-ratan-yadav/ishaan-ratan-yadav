# Subreddit intel (live: the agent keeps this current from each sub's rules page, sidebar and removals)

`tools/rpack.py` reads the table below. Keep the column order and the values it understands:
- **Promo**: `no` (any product mention = removal/ban) · `thread` (only in the sub's designated promo thread) · `story` (allowed inside a genuine story post, disclosed) · `ok` · `?` (not verified yet)
- **Links**: `no` · `ok` · `?`
- **Flair req**: `yes` (AutoModerator removes unflaired posts) · `no` · `?`
- **Post types**: comma list of what the sub accepts (`text,image,link,gallery`) or `?`
- **Min karma / age**: anything you saw (`AutoMod filters <30 days`, `comment ~10x first`). `?` if unknown.
- **Verified**: date you read the rules page logged in, or `no`.
- **Title rules**: put `title-tag: ...` in Notes when the sub requires a title prefix (e.g. a bracketed region). `rpack.py` then BLOCKS titles that don't start with `[`.

Read a sub's rules page (`reddit.com/r/SUB/about/rules`, plus the sidebar and wiki) before the FIRST post there.
Update the row the same day. Any removal, warning or mod message → note it here with the date and what triggered it.

| Sub | Promo | Links | Flair req | Min karma / age | Post types | Notes | Verified |
|---|---|---|---|---|---|---|---|
| r/agency | ? | ? | ? | posts only from people who already comment there: ~10 comments first (lead agent note) | ? | core sub: agency owners selling to brands | no |
| r/marketingagency | no | ? | ? | ? | ? | small, described as promotion-free | no |
| r/SMMA | ? | ? | ? | ? | ? | young agency owners, outbound-heavy | no |
| r/agencynewbies | ? | ? | ? | ? | text | title-tag: every post title must start with a bracketed location like [US], [Global], [India] or AutoModerator removes it (mod announcement thread read 2026-10-05 via RSS). Slow sub: threads stay alive for days, 11 h old threads still have 0 human comments. Beginners: easy karma for clear answers | 2026-10-05 (partial: title rule only) |
| r/freelance | no | ? | ? | ? | text | self-promo banned (redship 2026 list) | no |
| r/UGCcreators | ? | ? | ? | ? | ? | creators pitching brands: 'gifted vs paid' pain (lead agent insight 10-04) | no |
| r/Emailmarketing | ? | ? | ? | ? | ? | email/Klaviyo people; deliverability threads | no |
| r/klaviyo | ? | ? | ? | ? | ? | small; ecommerce email specialists | no |
| r/PPC | ? | ? | ? | ? | ? | paid search; tactical, data-heavy | no |
| r/FacebookAds | ? | ? | ? | ? | ? | very active (most posts in lead agent scrape); Meta ads operators | no |
| r/copywriting | ? | ? | ? | ? | ? | cold email copy teardowns fit | no |
| r/coldemail | ? | ? | ? | ? | ? | core sub: cold email operators. NOTE 2026-10-05: its public /rising/.rss returned HTTP 404 on 3 tries (other subs returned 200 or 429): verify the sub's exact name/status on Day 1 | no |
| r/Coldemailing | ? | ? | ? | ? | ? | small; brand-outreach questions | no |
| r/coldoutreach | ? | ? | ? | ? | ? | core sub (lead agent rising list) | no |
| r/LeadGeneration | ? | ? | ? | ? | ? | many vendors pitching; value posts stand out | no |
| r/sales | no | ? | ? | ? | text | any promotion = instant permanent ban (sub rule, 2026) | no |
| r/b2b_sales | ? | ? | ? | ? | ? | B2B sellers | no |
| r/b2bmarketing | ? | ? | ? | ? | ? | titles like '(I will not promote)' appear: strict norm | no |
| r/Entrepreneur | no | ? | ? | ? | text | promo only in designated threads; recurring threads seen: 'Sunday Steam', 'Success Saturday' | no |
| r/EntrepreneurRideAlong | story | ? | ? | ? | ? | journey posts welcome; vendors posting 'I'll do X for you' get ignored | no |
| r/startups | no | ? | ? | ? | text | zero promo outside the pinned share threads | no |
| r/smallbusiness | thread | ? | ? | ? | ? | promo only in the weekly thread | no |
| r/SideProject | story | ? | ? | ? | ? | sharing projects is the point; needs a story/details | no |
| r/SaaS | thread | ? | ? | ? | ? | promo in the feedback thread; founder stories OK | no |
| r/indiehackers | ? | ? | ? | ? | ? | build in public | no |
| r/growmybusiness | ok | ? | ? | ? | ? | helpful posts that mention a product are tolerated | no |
| r/IMadeThis | ok | ? | ? | ? | ? | most lenient; low buyer intent | no |
| r/ecommerce | no | ? | ? | ? | ? | bans promo AND 'attempts to enlist personal contact' (DM offers) | no |
| r/shopify | no | ? | ? | ? | ? | help-only | no |
| r/digital_marketing | no | ? | ? | ? | ? | help-only | no |
| r/DigitalMarketing | no | ? | ? | ? | ? | 'no promotional posts' in description | no |
| r/marketing | no | ? | ? | ? | ? | no self-promo; AMAs and data posts can be allowed with mod OK | no |
| r/influencermarketing | no | ? | ? | ? | ? | help-only (lead agent config) | no |

## Removal / warning log
| Date | Sub | What was removed or flagged | Likely trigger | Fix |
|---|---|---|---|---|

## Changelog
- 2026-10-05: seeded from web research + the lead agent's config. Nothing verified logged in yet (Day 1 does that).
