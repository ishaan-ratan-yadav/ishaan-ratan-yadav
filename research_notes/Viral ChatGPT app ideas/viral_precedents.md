# Viral Precedents: ChatGPT GPTs, ChatGPT Apps, and Adjacent Consumer AI Products (2023 to Oct 2026)

> Method note: Most direct page fetches (gptstore.ai, gptsapp.io, community.openai.com, a16z.news, chatgptappsrank.com, forkoff.xyz) were blocked by the network egress proxy. Findings below come from web-search result summaries of the cited pages. Where a figure came only from a secondary or aggregator site, that is flagged. Treat exact numbers as "as reported by" the cited source.

## 0. Original Instagram reel context (instagram.com/reel/Dd-QUM2PypU)

### Takeaway
I could not find the reel or any mirror, transcript, or repost of it. Instagram is blocked from this network, and two web searches for the ID "Dd-QUM2PypU" returned nothing relevant.

### Cited Findings
- A search for "Dd-QUM2PypU" returned only generic Instagram-downloader pages and nothing tied to the ID — [search results incl. InstaFix issue](https://github.com/Wikidepia/InstaFix/issues/107)
- A search for the ID plus "viral ChatGPT app ideas" returned only generic "ChatGPT prompts for Reels" pages — [example result](https://www.lvprompts.com/2026/07/chatgpt-viral-prompt-instagram-reels-growth.html?m=1)

### Inferences
- The report writer should ask the user what the reel says (caption or creator handle) if it matters for framing. The rest of these notes do not depend on it.

### Gaps
- The reel's content, creator, and view count are unknown.

---

## 1. Top GPTs in the GPT Store by conversation count, and what made them top

### Takeaway
The GPT Store's top GPTs were broad, high-frequency utilities: image generation, writing, academic research, coding, and design (Canva). Identity and fortune GPTs (astrology birth chart) and AI-girlfriend GPTs were the main "fun" outliers. The leaders won by sitting on intents ChatGPT users already had, often with a brand or data moat (Consensus has 200M papers; Canva has a design engine), and by ranking early in store search. They did not win through social sharing. The store as a whole failed as a business for builders: the promised revenue share was never paid.

### Cited Findings
**Rankings and numbers**
- On the gptstore.ai ranking dated 2025-01-27, the top GPTs were Python, image generator, Write For Me, Canva, Scholar GPT, Write Anything, Astrology Birth Chart GPT, and Code Copilot — [gptstore.ai rank](https://gptstore.ai/gpts/rank) (page blocked; taken from the search snippet)
- Reported conversation counts: image generator 12.0M+, Consensus 8.0M+, Scholar GPT 6.0M+ (2024 data) — [gptstore.ai rank](https://gptstore.ai/gpts/rank) / [scriptbyai best GPTs](https://www.scriptbyai.com/best-gpts/) (search summary)
- Write For Me 9.0M+ conversations (writing, 4.3 rating). Consensus 8.0M+ (research, 4.3 rating) — [DigitalOcean / tech.co lists via search summary](https://www.digitalocean.com/resources/articles/gpts)
- In an earlier snapshot, Consensus ranked #2 with 5M conversations and Write For Me #3 with 4M — [OpenAI community "Top 500 GPTs by conversations"](https://community.openai.com/t/ranking-of-top-500-gpts-by-conversations/578607). Research-category page: Consensus 5M+ (4.3), Scholar GPT 2M+ (4.2) — [gptstore.ai research category](https://gptstore.ai/gpts/categories/research)
- Consensus pitch: "chat directly with the world's scientific literature… write articles backed by academic papers," with 200M+ papers and citations. Scholar GPT advertises 200M+ resources including Google Scholar, PubMed, and arXiv — [gptstore.ai research category](https://gptstore.ai/gpts/categories/research)
- A daily-updated "Top 1000 GPTs ranked by conversations" list exists, but it could not be fetched — [gptsapp.io](https://gptsapp.io/trending-gpts/top-1000-gpts-ranked)

**AI girlfriend, astrology, and companionship demand**
- Within two days of the store's launch (Jan 2024), a search for "girlfriend" returned at least eight girlfriend bots ("Korean Girlfriend," "Virtual Sweetheart," "Your AI girlfriend, Tsu"). This happened despite policy banning GPTs "dedicated to fostering romantic companionship" — [Quartz](https://qz.com/ai-girlfriend-bots-are-already-flooding-openai-s-gpt-st-1851159131); [Futurism](https://futurism.com/the-byte/openai-gpt-store-filling-up-ai-girlfriends)
- "AI girlfriend" gets about 99K global and 27K US monthly searches, as cited in GPT-Store coverage — [Medium (illyism)](https://medium.com/@illyism/openais-gpt-store-flooded-with-ai-girlfriends-days-after-launch-1a0e7ea9983e) (secondary)

**Store-level failure**
- The GPT Store launched Jan 2024 with about 3M custom GPTs and a promised builder revenue share that "never materialized… Zero developers got paid." OpenAI pivoted to ChatGPT Apps — [Aakash Gupta on X](https://x.com/aakashgupta/status/2038714642487533679?lang=en) (commentator claim; consistent with the [OpenAI dev forum thread on revenue-share status](https://community.openai.com/t/what-is-the-status-with-gpt-store-revenue-share/839172))
- Commentators blame the failure on no quality control or curation, which filled the store with duplicates, and on having no payment system, so the best builders stopped publishing — [Medium, "Why OpenAI's GPT Store failed to gain traction"](https://sallysliu.medium.com/why-openais-gpt-store-failed-to-gain-traction-7783972a5f90); [Medium, 6 months later](https://toproad.medium.com/openai-gpt-store-6-months-later-6a23f2deed20) (opinion)
- An academic study of the GPT landscape exists for deeper detail — [arXiv 2405.10547 "GPTs Window Shopping"](https://arxiv.org/html/2405.10547v1)

### Inferences
- In-store winners had (a) a generic, high-volume name that matched what users typed into store search ("image generator," "Write For Me," "Python"), (b) proprietary data or tools (Consensus, Canva), or (c) evergreen identity content (astrology). Discovery happened mostly inside the store, not on social media, which is why none of these became cultural moments.
- Conversation counts in the millions are small next to ChatGPT's hundreds of millions of WAU. Even the #1 GPT reached a tiny fraction of users. The store was a weak distribution channel.
- Demand for companionship and identity content is strong, but OpenAI's policy pushes it out.

### Gaps
- No reliable 2025–2026 GPT rankings with fresh numbers were reachable. The ranking sites were blocked, and OpenAI stopped emphasizing GPTs after Apps launched.
- I found no conversation counts for specific tarot or AI-girlfriend GPTs.

---

## 2. Viral ChatGPT moments driven by shareable output, and the mechanics behind them

### Takeaway
The biggest ChatGPT growth spikes came from first-party features whose output was a personalized artifact people wanted to post. Examples: Ghibli-style images (Mar 2025), action figure and starter pack (Apr 2025), memory-based roast and "what do you know about me" prompts, "Your Year with ChatGPT" Wrapped (Dec 2025), and the "caricature of me and my job" trend (Feb 2026). The recurring formula is **your face or your data → stylized, recognizable template → one-tap prompt anyone can copy → result posted with an implicit "do yours."** The mechanics at work were identity and self-reflection, a familiar visual format (Ghibli style, blister-pack toy, caricature), copyable prompts, humor, and social comparison. Sora (Oct 2025) shows the downside: huge launch virality, a collapse in retention, and shutdown within about 7 months.

### Cited Findings
**Ghibli / GPT-4o image generation (launched Mar 25, 2025)**
- ChatGPT gained 1M new users in one hour. ChatGPT's original launch took 5 days to reach 1M — [Fortune](https://fortune.com/2025/04/01/sam-altman-chatgpt-signups-soar-hayao-miyazaki-image-generation-feature); [Workmind](https://workmind.ai/chatgpt-gains-1-million-users-in-one-hour-amid-ghibli-art-trend/)
- Altman said GPUs were "melting" and posted "can yall please chill on generating images this is insane our team needs sleep" — [Fortune](https://fortune.com/2025/04/01/sam-altman-chatgpt-signups-soar-hayao-miyazaki-image-generation-feature)
- In the first week, 130M+ users generated 700M+ images (Brad Lightcap, OpenAI COO). India was a major growth driver — [The Decoder](https://the-decoder.com/chatgpts-image-generation-explodes-with-700m-creations-in-first-week/); [GIGAZINE](https://gigazine.net/gsc_news/en/20250404-chatgpt-users-generated-over-700m-images/); [BGR](https://www.bgr.com/tech/why-chatgpt-went-down-this-week/)
- At TED 2025 (Apr), Altman cited 500M WAU and said backstage the user base had "doubled in just a few weeks," alluding to about 10% of humanity — [Forbes](https://www.forbes.com/sites/martineparis/2025/04/12/chatgpt-hits-1-billion-users-openai-ceo-says-doubled-in-weeks/); [Fortune](https://dc.fortune.com/2025/04/14/sam-altman-openai-user-base-doubled-few-weeks-10-of-world-uses-system)
- Analysis says the model was "unusually good at reproducing a recognizable look from a short prompt," and the feature was available to free users too — [aiwiki Studio Ghibli moment](https://aiwiki.ai/wiki/studio_ghibli_moment)

**Action figure / "starter pack" (Apr 2025)**
- Users upload a selfie plus a prompt and get a toy of themselves in blister packaging, with accessories (iced coffee, laptop, running shoes) and their name and job title on the label. It spread across TikTok, X, Facebook, and especially LinkedIn. Brooke Shields posted one — [Fast Company](https://www.fastcompany.com/91318427/the-ai-starter-pack-trend-is-taking-over-linkedin-and-tiktok); [PetaPixel](https://petapixel.com/2025/04/09/chatgpt-can-turn-you-into-a-toy-action-figure/); [GV Wire](https://gvwire.com/2025/04/16/ai-action-figures-flood-social-media-accessories-included/)
- Artists responded with the #StarterPackNoAI counter-trend of hand-drawn versions — [NBC News](https://www.nbcnews.com/tech/social-media/ai-action-figures-social-media-artists-hand-drawn-rcna201056)

**Memory-based "roast me" and "what do you know about me" prompts (2025)**
- After memory launched, users asked ChatGPT to roast them "based on everything you know about me." A related prompt asks "From all of our interactions what is one thing that you can tell me about myself that I may not know about myself." The trends spread on TikTok and Instagram, and Sam Altman endorsed one — [Tom's Guide](https://www.tomsguide.com/ai/everyones-asking-chatgpt-to-roast-them-heres-how-to-try-it); [TechRadar](https://www.techradar.com/computing/artificial-intelligence/new-chatgpt-prompt-goes-viral-with-sam-altmans-approval); [Yahoo Lifestyle](https://www.yahoo.com/lifestyle/articles/used-chatgpts-viral-roast-prompt-070100100.html)
- In a variant TikTok trend, women asked ChatGPT to reveal their "most unhinged question of 2025" — [Yahoo](https://www.yahoo.com/lifestyle/articles/women-asking-chatgpt-reveal-most-120000439.html)

**"Your Year with ChatGPT" Wrapped (Dec 22, 2025)**
- A Spotify-Wrapped-style recap with awards, a poem, a pixel-art image, a chat-style "archetype," and 2026 predictions. It required memory and chat-history referencing plus a minimum activity threshold, and launched in the US, CA, UK, AU, and NZ — [TechCrunch](https://techcrunch.com/2025/12/22/chatgpt-launches-a-year-end-review-like-spotify-wrapped/); [MacRumors](https://www.macrumors.com/2025/12/22/chatgpt-year-end-summary-2025/); [Euronews](https://www.euronews.com/2025/12/23/chatgpt-rolls-out-spotify-wrapped-style-2025-recap-for-millions-of-users)
- Users posted their recaps widely on X, Reddit, and TikTok. People without access used a copycat "ChatGPT Wrapped prompt" — [Tenorshare](https://www.tenorshare.ai/chatgpt-tips/chatgpt-wrapped-prompt.html) (secondary)

**Caricature trend (Feb 2026)**
- Prompt: "Create a caricature of me and my job based on everything you know about me," plus a photo. It spread across Facebook, Instagram, TikTok, and professional circles (news anchors, doctors, teachers, real-estate agents). Forbes and others ran privacy warnings — [Forbes (Feb 6, 2026)](https://www.forbes.com/sites/lesliekatz/2026/02/06/chatgpt-trend-turns-people-into-caricatures---and-shows-how-well-ai-knows-us/); [Forbes privacy (Feb 9, 2026)](https://www.forbes.com/sites/kateoflahertyuk/2026/02/09/the-new-chatgpt-caricature-trend-comes-with-a-privacy-warning/); [The Tab](https://thetab.com/2026/02/04/its-everywhere-so-heres-how-to-do-that-viral-ai-caricature-trend-with-chatgpt); [TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/i-tried-the-new-chatgpt-caricature-trend-and-was-shocked-how-well-the-ai-chatbot-knows-me)
- Techweez credits "privacy fatigue" for the trend's popularity — [Techweez](https://techweez.com/2026/02/13/chatgpt-caricature-trend-privacy-concerns/) (opinion)

**Adjacent: Google Nano Banana figurine trend (Aug 2025)**
- Gemini 2.5 Flash Image launched Aug 26, 2025. Within days, Josh Woodward said Gemini had gained 10M+ new users and processed 200M+ image generations or edits, driven by the "3D figurine on acrylic base plus packaging" prompt — [AlmaBetter](https://www.almabetter.com/bytes/articles/how-nano-banana-helped-gemini-get-10-million-new-users-2); [Tom's Guide](https://www.tomsguide.com/ai/ai-image-video/nano-banana-just-broke-the-internet-with-these-viral-trends-here-are-5-ai-photo-prompts-to-try-now)
- A Gemini exec said Nano Banana caused "a big demographic shift" toward younger users — [Yahoo Tech](https://tech.yahoo.com/ai/gemini/articles/google-gemini-exec-says-nano-111112810.html)

**Sora app (launched Sep 30, 2025, shut down Apr 26, 2026)**
- It passed 1M downloads in under 5 days, faster than ChatGPT, and hit #1 on the US App Store with about 100K daily installs. It launched invite-only in the US and Canada — [Engadget](https://www.engadget.com/ai/openais-tiktok-of-ai-slop-hit-one-million-downloads-faster-than-chatgpt-181216271.html); [TipRanks](https://www.tipranks.com/news/openais-sora-hit-one-million-downloads-in-less-than-five-days)
- The core mechanic was "cameo": scan your face, then let consenting friends (or the public) put you in videos. Viral content included Jake Paul as a beauty influencer and Sam Altman stealing GPUs — [Influencer Marketing Hub](https://influencermarketinghub.com/openai-sora-1-million-downloads/); [Social Samosa](https://www.socialsamosa.com/samosa-snippets/the-sky-falls-what-led-to-the-downfall-of-openais-sora-11263604)
- Downloads peaked at about 3.33M in Nov 2025, fell 32% in Dec, fell another 45% in Jan, and were at about 1.13M by Feb 2026 (Appfigures) — [ContentGrip](https://www.contentgrip.com/sora-app-decline-openai/); [Social Samosa](https://www.socialsamosa.com/samosa-snippets/the-sky-falls-what-led-to-the-downfall-of-openais-sora-11263604)
- The shutdown was announced Mar 24, 2026. The app and web closed Apr 26, 2026, and the API was retired Sep 24, 2026 — [TechCrunch](https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/); [NBC News](https://www.nbcnews.com/tech/tech-news/openai-shuttering-sora-video-generating-service-rcna264989)
- Reported reasons: GPU costs, users falling from a peak of about 1M to under 500K, about $2.1M lifetime revenue, and copyright issues — [MindStudio](https://www.mindstudio.ai/blog/openai-shutting-down-sora-what-happened); [Medium](https://medium.com/@shubhamnv2/openai-sora-shutdown-15m-day-costs-2-1m-revenue-the-full-story-088380118243) (secondary; the $2.1M and $15M/day figures could not be verified against a primary source)
- One secondary write-up claims 1% 30-day retention — [Vocal](https://vocal.media/futurism/sora-app-from-viral-sensation-to-1-30-day-retention) (unverified)

### Inferences
- **Mechanics ranked by evidence:**
  1. **Personalized visual output in a known template.** Ghibli, action figure, caricature, Nano Banana figurine, and Lensa avatars all follow this pattern. People share an image of themselves faster than any text.
  2. **"How AI sees me" self-reflection.** Roast, "tell me something about myself," Wrapped, and caricature-from-memory each create a slightly embarrassing or flattering reveal that is fun to post and compare. Memory turns a generic prompt into a personal one.
  3. **Copyable prompts with zero setup.** Each trend spread as a prompt string or one-tap action. Every post is also the instructions.
  4. **Professional identity hooks.** Starter pack and caricature show name and job, which opened LinkedIn and work-group sharing ("show your job").
  5. **Humor and roast.** Being mocked is safe to share because the AI did it.
  6. **Novelty capability jumps.** Ghibli and Nano Banana were the first time a model could do a given style well. Trends fade when the novelty does.
- **The Sora lesson:** a "make content" app with no reason to return after the novelty (and with high compute cost) can win the launch charts and still die. Trends drive acquisition, not retention.
- **For a ChatGPT app:** the strongest designs combine (a) the user's photo or ChatGPT memory, (b) a branded, recognizable output template, (c) a one-line trigger prompt, and (d) an output sized for Stories or LinkedIn with subtle attribution.

### Gaps
- "Ask ChatGPT to draw your life," IQ-style results, and personality-test trends: I found no dedicated coverage with numbers.
- No numbers on how many Wrapped recaps were generated or shared, or on caricature-trend usage.
- No official OpenAI numbers on new users from the action-figure trend specifically.

---

## 3. ChatGPT Apps SDK apps (Oct 2025 to Oct 2026) that broke out

### Takeaway
I found no credible public evidence of any Apps SDK app, indie or brand, that broke out virally with disclosed metrics. Bloomberg (Mar 2026) reported that results "lag": about 300 integrations, apps buried in the interface, a buggy SDK, tedious approval, no usage data for developers, and brands holding back functionality. At DevDay 2026 (Sep 29) OpenAI reported 1.2B WAU but still announced no app-store-style billing or revenue share. The distribution is huge, but no one has shown it produces breakouts yet.

### Cited Findings
- Apps in ChatGPT and the Apps SDK (built on MCP) launched at DevDay, Oct 6, 2025. Launch partners were Booking.com, Canva, Coursera, Figma, Expedia, Spotify, and Zillow — [TechCrunch how-to](https://techcrunch.com/2025/10/24/how-to-use-the-new-chatgpt-app-integrations-including-spotify-figma-canva-and-others); [Tom's Guide](https://www.tomsguide.com/ai/you-can-now-use-apps-inside-chatgpt-including-spotify-canva-and-zillow-heres-how)
- Instacart was reported as the first ChatGPT app to support full checkout inside ChatGPT — [Jotform list via search summary](https://www.jotform.com/ai/best-chatgpt-apps/) (secondary)
- Bloomberg (Mar 30, 2026), six months in: the initiative was "off to a sluggish start." There were 300+ integrations, but they were "hidden away and limited in functionality by partner companies hesitant to hand off customer relationships and payments." Developers cited tedious approval, a buggy SDK, and little engagement data. OpenAI acknowledged the developer experience needed improvement — [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-30/openai-s-chatgpt-app-store-took-aim-at-apple-but-results-lag-so-far); [PYMNTS](https://www.pymnts.com/artificial-intelligence-2/2026/openai-aims-to-improve-developer-experience-around-third-party-chatgpt-apps/)
- A third-party tracker's mid-2026 snapshot (Jul 16, 2026) counted 65 apps it scored. Business (38) and productivity (35) dominated, with lifestyle at 16 — [ChatGPTAppsRank state of apps 2026](https://chatgptappsrank.com/state-of-chatgpt-apps-2026) (blocked; from the search snippet. This count is far below Bloomberg's 300+, so it is likely a curated subset)
- DevDay 2026 (Sep 29, 2026): OpenAI reported 1.2B+ weekly ChatGPT users. It announced "plugin extensions" (full apps native to ChatGPT and Codex), always-on "Dots" agents, and Sign in with ChatGPT with 16 launch partners. No billing or revenue-share system comparable to traditional app stores was announced — [The Decoder](https://the-decoder.com/chatgpt-now-reaches-1-2-billion-people-every-week-openai-says/); [CNBC recap](https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html); [The Neuron](https://www.theneuron.ai/news/openai-devday-2026-chatgpt-is-becoming-an-ai-operating-system/) (DevDay 2026 details are only a few days old and come from search summaries; verify specifics)
- OpenAI reported 900M WAU in Feb 2026, up from 400M a year earlier — [Aakash Gupta, Medium](https://aakashgupta.medium.com/the-chatgpt-app-store-has-900m-weekly-users-heres-how-to-build-for-it-99a7dcde81ef) (secondary)
- OpenAI separately said Apple Intelligence users showed little interest in the ChatGPT integration (Sep 2026). This is another case where an embedded surface underperformed — [9to5Mac](https://9to5mac.com/2026/09/23/openai-says-apple-intelligence-users-showed-little-interest-in-chatgpt-integration/)

### Inferences
- Through Oct 2026, the viral moments inside ChatGPT were all first-party features. No third-party app has had a Ghibli-style moment. A builder should not expect the directory to deliver users. The realistic path is a ChatGPT app with a shareable output that pulls people in from social media ("type @YourApp in ChatGPT").
- The incentive problem Bloomberg describes (brands don't want to lose the customer relationship) leaves room for indie, consumer, fun apps where ChatGPT is the whole product, not a funnel.
- Monetization is still unsolved: no billing or revenue share as of DevDay 2026. Revenue has to come from your own off-ChatGPT subscription, which adds friction.

### Gaps
- No public per-app usage numbers (installs, invocations, WAU) for any ChatGPT app.
- I could not verify whether any consumer or entertainment ChatGPT app (horoscope, games, photo) gained social traction.

---

## 4. Viral indie AI consumer apps outside ChatGPT: growth loops and how they translate

### Takeaway
The standalone AI consumer hits of 2022–2026 fall into two loops. (1) **Output-as-ad virality**: Lensa, Remini, Epik yearbook, PhotoAI. A personalized image of yourself is posted, and every post advertises the app. These spike hard and fade. (2) **Paid and creator distribution with a single "magic" interaction**: Cal AI, Umax, RIZZ, Cluely. Creators demo a one-step result (photo of food → calories, selfie → face rating, screenshot → reply) and the app monetizes immediately with a hard paywall. Companion apps (Character.ai) win on retention, not shareability. All of them pair a self-image or self-improvement hook (looks, body, dating, career) with a single input and an instant verdict.

### Cited Findings
**Lensa Magic Avatars (Prisma Labs, Nov–Dec 2022)**
- Downloads went from 219K (Oct 2022) to 19.3M (Dec 2022). December revenue was about $30.7M, and 2022 revenue about $39.2M, up from $6.5M in 2021 — [DevTechnosys Lensa stats](https://devtechnosys.com/data/lensa-ai-statistics.php); [Prioridata](https://prioridata.com/data/lensa-ai-statistics/) (aggregators citing Sensor Tower and data.ai-style estimates)
- When Marques Brownlee posted his avatars on Nov 26, 2022, worldwide downloads spiked 631% within days — [DevTechnosys](https://devtechnosys.com/data/lensa-ai-statistics.php) (aggregator)

**Epik AI yearbook (Snow Corp, Sep–Oct 2023)**
- After the yearbook feature launched Sep 18, 2023, Epik was #1 in App Store downloads in 56 countries, including the US and UK, as of Oct 10, with about $7M iOS sales per data.ai — [Korea JoongAng Daily](https://www.koreajoongangdaily.com/business/ai-yearbook-picture-craze-makes-it-rain-for-snow/11050682)

**Remini AI headshots (Bending Spoons, Jun–Jul 2023)**
- #1 overall on the US App Store on Jul 11, 2023, ahead of Threads. Reported 22M+ worldwide downloads in 30 days. #Remini had 1.4B+ TikTok views ("why pay for headshots when AI does them for free?") — [TechCrunch](https://techcrunch.com/2023/07/20/remini-tops-the-app-store-for-its-viral-ai-headshots-but-its-body-edits-go-too-far-some-say/); [PetaPixel](https://petapixel.com/2023/07/20/why-pay-a-photographer-generation-z-go-wild-for-ai-generated-headshots/)
- Global downloads rose 138% month over month in Jul 2023, making it the #1 AI photo app — [Sensor Tower](https://sensortower.com/blog/rapid-growth-and-competitive-dynamics-the-state-of-ai-photo-and-video-apps)
- About $3.73M consumer spend for Jun 9–15, up 1,055% week over week (data.ai) — [TechCrunch](https://techcrunch.com/2023/07/20/remini-tops-the-app-store-for-its-viral-ai-headshots-but-its-body-edits-go-too-far-some-say/)

**Cal AI (Zach Yadegari and Henry Langmack, teens; acquired by MyFitnessPal)**
- 15M+ downloads and $30M+ annual revenue in under two years. Yadegari said they "broke $50m in ARR." MyFitnessPal announced the acquisition Mar 2, 2026 (closed Dec 2025). The 7-person team was retained — [TechCrunch / Yahoo Finance](https://finance.yahoo.com/news/myfitnesspal-acquired-cal-ai-viral-140000003.html); [MyFitnessPal blog](https://news.myfitnesspal.com/myfitnesspal-expands-its-position-as-the-leading-player-in-digital-nutrition-tracking-with-cal-ai-acquisition/); [Zach Yadegari on X](https://x.com/zach_yadegari/status/2028473704359874652)
- Growth loop: the first ~$2M/month came "entirely from fitness influencers posting the app inside their daily-routine content," then non-fitness influencers, then paid TikTok/IG/FB performance ads, reaching about $5.7M/month — [Profitable Founder](https://www.profitablefounder.xyz/blog/cal-ai-founder-story); [Starter Story](https://www.starterstory.com/cal-ai-breakdown) (secondary, based on founder interviews)

**Blake Anderson's portfolio: RizzGPT, Umax (also a Cal AI co-founder)**
- Tiffany Zhong: "rizzgpt: 4m revenue, umax: 6m revenue, cal ai: 50m arr… he learned to code with chatgpt" — [X post](https://x.com/tzhongg/status/2028931446317232397?lang=en)
- Umax rates faces (jawline, cheekbones, masculinity) using OpenAI tech. It has 7M+ downloads and peaked at #36 in the US lifestyle chart — [Fortune](https://fortune.com/2024/07/01/looksmaxxing-apps-rate-teen-boys-faces-mental-health/)
- In Oct 2024, Forbes covered the bootstrapped apps at about $15M ARR combined — [Forbes](https://www.forbes.com/sites/josipamajic/2024/10/07/hacking-the-app-store-gen-zs-15m-arr-bootstrapped-success-story/)

**Cluely (Roy Lee, Apr 2025)**
- The launch tweet "Cluely is out. cheat on everything." got about 13.2M views. The blind-date launch video got 13M+ views on X. A campaign that hired about 50 interns to post TikTok and IG content pushed total reach past 1B views — [SF Standard](https://sfstandard.com/2025/07/18/cluely-startups-roy-lee-columbia-cheating-viral-tiktok/); [PostBeam](https://www.postbeam.ai/blog/how-cluely-grows)
- Claimed $6M ARR by June 2025. Lee later admitted to inflating the headline ARR, and he said viral buzz alone is insufficient — [Wikipedia: Roy Lee](https://en.wikipedia.org/wiki/Roy_Lee_(entrepreneur)); [Bitget news](https://www.bitget.com/news/detail/12560605049792) (treat the revenue figures as unreliable)

**PhotoAI and InteriorAI (Pieter Levels, solo)**
- PhotoAI is reported at about $102K–138K MRR (2025) and InteriorAI at about $39–40K MRR, both self-reported publicly by Levels — [Indie Hackers case study](https://www.indiehackers.com/post/photo-ai-by-pieter-levels-complete-deep-dive-case-study-0-to-132k-mrr-in-18-months-3a9a2b1579); [aituts](https://aituts.com/case-study/photo-ai-pieter-levels/)
- Levels launched 70+ products before these hits — [Julian on X](https://x.com/julianivaldy/status/1705224483441643596)

**Character.ai**
- 20M MAU in early 2024, peaking around 28M in mid-2024 before declining. Reported average time on the app ranges from about 75 min/day to about 2 hrs/day, with about 298 sessions per user per month (Sensor Tower) — [SQ Magazine](https://sqmagazine.co.uk/character-ai-statistics/); [a16z Top 100](https://a16z.com/100-gen-ai-apps/) (aggregators; figures vary by source)

**Context: a16z Top 100 Gen AI Consumer Apps, 6th edition (Mar 2026)**
- ChatGPT is 2.7x the #2 (Gemini) on web and 2.5x on mobile. ChatGPT WAU grew by 500M in a year to 900M. The list now includes AI-heavy incumbents (CapCut at 736M MAU, Canva, Notion, Grammarly) — [The Neuron summary](https://www.theneuron.ai/explainer-articles/a16z-just-ranked-the-100-most-popular-ai-apps-heres-the-full-list-and-what-it-tells-us-/); [a16z newsletter](https://www.a16z.news/p/top-100-gen-ai-consumer-apps-march)

### Inferences (translating these loops to a ChatGPT app)
- **Lensa, Remini, Epik → ChatGPT:** "upload a selfie, get a themed pack (yearbook, headshot, figurine, era)" is natively possible in ChatGPT, but first-party image generation competes with it for free. An app would need a proprietary template, consistency (multi-image packs, same face), or packaging such as a printable or a card frame to be worth invoking.
- **Cal AI → ChatGPT:** "snap → instant number" (calories, face score, outfit rating, room makeover) maps well onto an in-chat widget. But Cal AI scaled through paid creators and a paywall, and ChatGPT apps have no billing yet. The app would need an off-platform upsell.
- **Umax and RIZZ → ChatGPT:** score-and-verdict apps on insecure-but-shareable topics (looks, dating replies) drive repeat use and screenshots. They carry policy and ethical risk (Fortune covered harm to teen boys), and OpenAI's usage policies may restrict them.
- **Cluely → ChatGPT:** a provocative, founder-led content engine drives attention, but Cluely shows views can outrun real revenue.
- **Character.ai → ChatGPT:** companionship retains users but conflicts with OpenAI's romance-companion policy (see the GPT Store section).
- **Common DNA:** a one-input, instant-verdict experience about *you* (face, body, food, texts, career). The output is visual or screenshot-able, it monetizes on first use, and distribution comes from creators or the output itself rather than app-store search.

### Gaps
- No primary or Sensor Tower-verified 2025–2026 numbers for RizzGPT or Umax beyond founder and investor posts.
- I did not verify Interior AI's growth loop specifically (beyond Levels' building in public on X).
- Friend's actual retention and Character.ai's 2026 MAU are unverified.

---

## 5. Common traits of things that failed to spread (or failed to last) despite hype

### Takeaway
The failures cluster into four patterns. (1) **Platform without distribution or incentives**: GPT Store, and so far ChatGPT Apps. (2) **Hype or spectacle without a loved core loop**: Friend pendant, Humane AI Pin, Rabbit R1. (3) **Virality without retention or economics**: Sora app, many trend apps. (4) **Backlash**: privacy, artist, and creepiness concerns that turn sharing into stigma.

### Cited Findings
- **GPT Store:** about 3M GPTs, no paid revenue share, no curation, and builders struggled to drive usage. Most never cleared the engagement floor — [Aakash Gupta on X](https://x.com/aakashgupta/status/2038714642487533679?lang=en); [Medium analysis](https://sallysliu.medium.com/why-openais-gpt-store-failed-to-gain-traction-7783972a5f90)
- **ChatGPT Apps (to date):** apps hidden in the interface, partners holding back features, no usage data for developers — [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-30/openai-s-chatgpt-app-store-took-aim-at-apple-but-results-lag-so-far)
- **Sora:** downloads peaked at about 3.33M in Nov 2025, then fell steeply. Shut down within about 7 months. Cited reasons: GPU cost, falling users (about 1M → under 500K), minimal revenue, and copyright/deepfake issues. TechCrunch called it "the creepiest app on your phone" — [TechCrunch](https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/); [ContentGrip](https://www.contentgrip.com/sora-app-decline-openai/); [MindStudio](https://www.mindstudio.ai/blog/openai-shutting-down-sora-what-happened)
- **Friend ($129 AI pendant):** a $1M+ NYC subway takeover (about 11,000 posters) was widely vandalized ("AI is not your friend," "Stop profiting off of loneliness"). About 3,000 units sold and about 1,000 shipped, roughly $348K revenue. The founder later called the backlash intentional — [Wikipedia: Friend (product)](https://en.wikipedia.org/wiki/Friend_(product)); [Gothamist](https://gothamist.com/arts-entertainment/the-guy-behind-those-friend-ads-in-the-subways-is-tired-of-talking-to-new-yorkers); [Museum of Failure](https://museumoffailure.com/exhibition/friend-ai)
- **Humane AI Pin:** about 10K units sold against a projected 100K. Returns outpaced sales, leaving about 7K units in customers' hands. About $9M revenue and about $1M in returns. Discontinued Feb 28, 2025, with assets sold to HP for $116M after raising $230M — [Tom's Guide](https://www.tomsguide.com/ai/humane-flooded-with-dollar1-million-in-ai-pin-returns-as-ai-gadget-dumpster-fire-rages-on); [Digital Applied](https://www.digitalapplied.com/blog/ai-product-failures-2026-sora-humane-rabbit-lessons)
- **Rabbit R1:** about 100K units sold on CES hype, then mass returns when it couldn't deliver its demo promises — [Jason Deegan](https://jasondeegan.com/why-humanes-ai-pin-and-rabbit-r1-both-flopped-spectacularly/); [Digital Applied](https://www.digitalapplied.com/blog/ai-product-failures-2026-sora-humane-rabbit-lessons) (secondary)
- **Backlash patterns:** #StarterPackNoAI artist backlash — [NBC News](https://www.nbcnews.com/tech/social-media/ai-action-figures-social-media-artists-hand-drawn-rcna201056). Privacy warnings on the caricature trend — [Forbes](https://www.forbes.com/sites/kateoflahertyuk/2026/02/09/the-new-chatgpt-caricature-trend-comes-with-a-privacy-warning/). Remini criticized for body edits — [TechCrunch](https://techcrunch.com/2023/07/20/remini-tops-the-app-store-for-its-viral-ai-headshots-but-its-body-edits-go-too-far-some-say/). Looksmaxxing apps criticized for harming teen mental health — [Fortune](https://fortune.com/2024/07/01/looksmaxxing-apps-rate-teen-boys-faces-mental-health/)
- **Cluely:** the founder admitted inflating ARR and conceded virality alone is insufficient — [Bitget news](https://www.bitget.com/news/detail/12560605049792); [Wikipedia](https://en.wikipedia.org/wiki/Roy_Lee_(entrepreneur))

### Inferences
- **Failure traits to avoid:**
  1. The output is not about the user, so there is nothing personal to share (generic GPTs).
  2. The demo is better than daily use (Rabbit, Humane, Sora).
  3. No repeatable reason to return after the first shareable result (Sora, and the likely fate of most trend apps).
  4. Unit economics break at viral scale. Image and video compute is expensive, and free virality burns cash (Sora; ChatGPT's own "melting GPUs").
  5. Creepy or loneliness-exploiting positioning invites public backlash (Friend, Sora deepfakes).
  6. Relying on a platform's store for discovery when the platform has no curation or monetization (GPT Store, early ChatGPT Apps).
- **Successful counter-pattern:** fast personal verdict plus a shareable artifact for spread, a utility or recurring hook for retention (daily calorie log, daily horoscope, weekly roast), and monetization from day one.

### Gaps
- No quantitative retention data for trend-driven ChatGPT features (for example, how many Ghibli-era signups stayed).
- I found no rigorous dataset comparing hyped GPTs or ChatGPT apps that failed versus succeeded. Evidence is anecdotal or journalistic.
