# How Reddit ranks and polices content (researched 2026-10-05)

Reddit does not publish its current ranking code. What is public is the 2015-era open-source formula, which is still a
good model of how Reddit "thinks". Everything about 2026 behaviour (personalization, ML ranking, spam systems) comes from
industry analyses and Reddit's own announcements: treat numbers as directional and let our own logs overrule them.

## 1. Post ranking
- **Hot (archived formula):** `score = ups - downs`; `order = log10(max(|score|, 1))`; `rank = sign * order + seconds_since_epoch / 45000`.
  - 45,000 s = 12.5 h: **12.5 hours of freshness equals a 10x difference in score.** A 10-vote post now ranks with a 100-vote post from 12.5 h ago.
  - The log means the **first 10 votes count as much as the next 90.** So the first 10-30 minutes matter more than the next 10 hours.
- **Velocity beats total.** 10 upvotes in 10 minutes beats 30 over an hour. Most posts have their fate decided in the first 1-3 hours.
- **Rising** is the "faster than expected" list: new posts gaining votes quickly relative to the sub's norm. It is where early commenters get seen and where posts break into Hot.
- **Upvote ratio** and downvotes cost twice (they subtract from score and mark the post as divisive). Titles that overpromise get early downvotes and die.
- **Votes are fuzzed.** Displayed scores are noisy, especially in the first hour. Judge a post by trajectory over several looks, not one number.
- **Home feed is personalized** (since ~2023-24): Reddit mixes subscribed subs, recommended subs and ML-predicted interest. Early engagement from people who like similar content decides whether a post is pushed to non-subscribers. Subscribers' first reaction is the seed.
- **Comments, dwell and shares matter more in 2026** than a few years ago (analyst consensus, not Reddit-confirmed). Discussion depth (replies to replies) signals a good thread.
- **Time of day** matters because the first-hour voters are whoever is awake: see `viral-playbook.md` for timing.

## 2. Comment ranking ("Best")
- Default sort is **Best**, based on a Wilson-style confidence score (archived code): it penalises small samples. A 3-up/0-down comment can beat a 10-up/10-down comment.
- Early comments in a rising thread collect votes as the thread grows. Analyses put comments in the first hour at roughly 3-5x the upvotes of equally good ones posted hours later (directional, vendor claims).
- Replies to the top comment get the most views. Being the first good reply under a high-karma comment is a second route to visibility.
- **Contest mode / "Top" / "New" sorts** change what people see, but most readers stay on Best.

## 3. Karma, account age and the gates in front of you
- **Post karma and comment karma** are separate. Subs gate on either, plus account age. Typical gates are small (10-100 karma, 1-30 days) but are set by each sub.
- **AutoModerator** is each sub's own script: it can remove posts from low-karma/young accounts, posts without flair, posts with links or banned words, and repeat domains. Removals are often silent (you see your own post, nobody else does).
- **Contributor Quality Score (CQS):** since Sept 2023 mods can filter on a hidden Reddit-assigned score (Lowest/Low/Moderate/High/Highest) via AutoModerator. It uses account signals (email verified, behaviour history, network/location patterns). **New accounts and anything that tripped spam alarms start low.** Reddit's pilot found CQS filters cut false positives and removals compared with karma/age gates. Practical consequence: a clean, human-looking history is the asset; mass activity burns it.
- **"You're doing that too much. Try again in X minutes."** New-to-a-sub accounts have comment and post cooldowns. Reaching roughly 10 karma in that sub is reported to lift it (community reports, not official). Our pack tracks a per-sub comment gap (default 10 min).
- **Karma by sub:** karma in a sub is the only karma that helps you in that sub's AutoMod. Ten good comments in r/agency are worth more there than 500 from r/aww.

## 4. What Reddit punishes (and how it shows up)
Five different things get confused. The fix differs for each.
| Mechanism | What you see | Who can undo it |
|---|---|---|
| **Site-wide shadowban / suppression** | everything you post is visible only to you; profile looks empty logged-out | Reddit admins only (appeal at reddit.com/appeals, once, then wait 1-2 weeks) |
| **Account suspension** | login blocked or a notice | admins |
| **Sub-level spam-filter catch** | one post in the sub's mod queue, invisible to others | that sub's mods can approve |
| **AutoModerator removal** | removed, sometimes with a bot comment, sometimes silent | fix the cause (flair, karma gate, link), resubmit once, or message mods |
| **Mod removal / sub ban** | message from mods | message mods politely; never evade |
- Triggers (industry consensus): new account dropping links; high-volume or machine-regular cadence; identical or near-identical posts across many subs in a short window; mass unsolicited DMs; self-promo above ~10% of activity; vote manipulation (asking for votes anywhere, vote rings, upvote buying); multiple accounts (ban evasion, sockpuppets); VPN/datacenter IPs; repeated domain submission.
- Reddit's rule 2: post authentic content into communities where you have a personal interest; no spam, vote manipulation, ban evasion or subscriber fraud. Penalties escalate: removal, sub shadowban, site shadowban (hardest to reverse), sub ban, account suspension, plus domain blacklisting.
- The 90/10 guideline (reddiquette): if more than about 10% of what you submit is your own stuff, you look like a website with a Reddit account. Disclosure of affiliation is expected ("full disclosure, I run X").

## 5. How to self-check for suppression (the agent does this weekly and after any odd drop)
1. **Logged-out view:** open `reddit.com/user/<our username>` in a private/logged-out context. Our last posts and comments should be visible. If the profile says not found or looks empty while logged-in shows content, suspect a site-wide shadowban.
2. **Per-post check:** open the post URL logged-out (or in a private window). If the title shows but you see `[removed]` or it is absent from `/r/SUB/new`, it was removed or filtered.
3. **/r/SUB/new check:** a fresh post that is not in the sub's New feed within a minute or two, logged-out, was filtered.
4. **Signals in our own data:** a post stuck at 1 point and 0 comments for 2+ hours in a normal-traffic sub, when similar posts get views, is a filter signal. A sudden 90% drop in comment karma per comment across all subs is a site-wide signal.
5. **r/ShadowBan bot** (third-party tool, tells whether recent content is visible) is a legitimate neutral check, but it means posting there: that is Ishaan's decision, never the agent's.
- Report findings to Ishaan with evidence. Do not "test" by posting extra content.

## 6. Search and AI visibility (a reason to write for the long tail)
- Reddit threads rank well in Google (users append "reddit" to queries; Google licenses Reddit data) and are cited heavily in AI answers: a Semrush study found about 40% of LLM references pointed to Reddit in mid-2025, but ChatGPT's share of Reddit citations has been volatile through 2026 (reported swings of 86%).
- **Reddit Answers** (Reddit's native AI search) rolled out to all logged-in users on 2026-05-05 and cites individual comments and threads (about 4 threads per answer in one sample; three subs made up 28% of citations). A clear, specific, well-formatted comment in a question thread can be quoted for months.
- Implication: evergreen **help threads and detailed teardowns** compound. A post titled the way people search ("how to find a D2C founder's email") keeps getting views and profile visits after the Hot window closes. Time-sensitive viral bridges are the opposite: fast, short-lived.

## 7. Cadence limits we stay inside
- New account: **about 1 comment per 10 minutes per sub**, no bursts. Fewer than 8-12 comments a day in week 1, spread across hours and subs.
- **At most 1 original post per day, usually 3-5 a week**, in different subs, never the same title twice, crossposts spaced hours-to-days apart (`viral-playbook.md`).
- Zero DMs unless someone engaged first. Never vote, never ask for votes, never use more than the one account.

## Sources
- Reddit archived ranking code (Hot, 45000s), explained: https://socialboostdigital.com/blog/reddit-ranking-algorithm-2026
- Velocity, first-hour window, 2026 changes: https://www.singlegrain.com/digital-marketing-strategy/reddits-upvote-algorithm-how-to-optimize-for-visibility/ and https://www.conbersa.ai/learn/reddit-algorithm-explained
- Suppression types, self-check, appeal: https://www.redditapis.com/blogs/reddit-shadowban-2026 and https://multilogin.com/blog/is-your-reddit-account-shadowbanned/
- CQS: https://postpone.app/blog/understanding-reddits-contributor-quality-score and Reddit's r/modnews announcement (Sept 14, 2023)
- Self-promotion rules, enforcement ladder, rule 2: https://redship.io/blog/reddit-self-promotion-rules-2026
- Comment cooldown for new accounts: community reports in r/NewToReddit (https://www.reddit.com/r/NewToReddit/) summarised via web search 2026-10-05
- Early comments / rising: https://www.conbersa.ai/learn/reddit-thread-seeding-timing
- AI/search visibility: https://www.isocialweb.agency/en/bita/reddit-ai-source/ and https://saasintelligence.substack.com/p/reddits-ai-citation-share-just-grew
