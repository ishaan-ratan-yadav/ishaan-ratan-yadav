# Unmet Demand and Open Opportunity Spaces for New ChatGPT Apps (as of October 2026)

> Research note: several primary sources (community.openai.com, developers.openai.com, virtualizationreview.com, modernretail.co, usecarly.com) were blocked by the network proxy, so some claims rely on search-result snippets of those pages rather than full reads. Those are flagged where relevant. No direct Reddit threads, Google Trends data, or Inc42/YourStory articles could be retrieved, so quantitative search-volume evidence is missing (see Gaps).

## Platform context the writer must know first (affects every opportunity)

### Takeaway
The platform changed a lot in 2026. The App Directory became the **Plugin Directory** on July 9, 2026, and **custom GPTs are being retired**: creation of new ones was planned to end September 25, 2026, and they are scheduled to stop running December 11, 2026. An indie developer should build an Apps SDK / MCP app packaged inside a Plugin, not a custom GPT. Monetization of digital goods inside ChatGPT is still not approved, and discoverability for third-party apps is weak.

### Cited Findings
- Apps SDK announced October 6, 2025 at DevDay. It is MCP-based and open source, and apps render interactive UI (maps, playlists, slides) inline in chat. Launch partners were Booking.com, Canva, Coursera, Figma, Expedia, Spotify, Zillow — [OpenAI](https://openai.com/index/introducing-apps-in-chatgpt/); [TechCrunch](https://techcrunch.com/2025/10/06/openai-launches-apps-inside-of-chatgpt); [dig.watch](https://dig.watch/updates/chatgpt-introduces-new-generation-of-interactive-apps)
- Apps are available to logged-in users outside the EU on Free, Go, Plus and Pro, which matters for reaching India's Go/Free base — [OpenAI](https://openai.com/index/introducing-apps-in-chatgpt/)
- The App Directory launched December 18, 2025. It renamed "connectors" to "apps" and opened public submissions. It initially had only three categories (Featured, Lifestyle, Productivity) — [Engadget](https://www.engadget.com/ai/openai-just-launched-an-app-store-inside-chatgpt-133049586.html); [datastudios](https://www.datastudios.org/post/chatgpt-app-directory-and-gpt-store-marketplace-launch-sdk-features-and-platform-evolution)
- As of July 2, 2026 there were 1,624 apps across 44 categories (community-maintained list) — [awesome-chatgpt-apps (GitHub)](https://github.com/rdmgator12/awesome-chatgpt-apps)
- On July 9, 2026 the App Directory was migrated to the Plugin Directory. A plugin can bundle skills (instructions, examples, code), apps (MCP connections) and app templates, and existing apps keep working underneath plugins — [Taskade](https://www.taskade.com/blog/chatgpt-plugins); [dragapp](https://www.dragapp.com/blog/what-happened-to-chatgpt-plugins/); [helloskip](https://helloskip.com/b/illco-ai/blog/openai-just-replaced-apps-with-plugins-and-chatgpt-now-runs-your-entire-workflow-mrf35te3)
- Plugin listings live at chatgpt.com/plugins/<slug> (for example, Steer Astro) — [ChatGPT Plugins: Steer Astro](https://chatgpt.com/plugins/steer-astro)
- On September 11, 2026 OpenAI announced in its release notes that it would retire custom GPTs in favor of plugins. Planned dates: migration banner September 17, end of GPT creation September 25, GPTs stop running December 11, 2026. GPT instructions convert to a Skill and knowledge files become reference files. Conversations, the selected model, Custom Actions and sharing settings do not transfer — [gsmdome](https://www.gsmdome.com/openai-to-retire-custom-gpts-on-december-11-2026-shifting-users-to-plugins-and-skills); [Virtualization Review (snippet only; page blocked)](https://virtualizationreview.com/articles/2026/09/28/openai-to-retire-custom-gpts-replace-them-with-plugins.aspx); [EdTech Innovation Hub](https://www.edtechinnovationhub.com/news/openai-to-retire-custom-gpts-in-december-as-creators-move-to-plugins). Note: one snippet says the December 11 date is stated "for affected Enterprise workspaces", while other sources say it applies across plans. The exact scope per plan is unconfirmed.
- Monetization: external checkout (a purchase on the developer's own domain) is the recommended, generally available path. In-chat Instant Checkout via the Agentic Commerce Protocol is a limited beta for approved partners selling physical goods. Snippets of OpenAI's docs say apps monetizing digital products/services cannot be submitted yet, and that OpenAI is "exploring additional monetization options over time, including digital goods" — [OpenAI Apps SDK Monetization docs (snippet; page blocked)](https://developers.openai.com/apps-sdk/build/monetization); [OpenAI Dev Community thread (snippet)](https://community.openai.com/t/chatgpt-app-monetization-apps-sdk/1372343); [arsum](https://arsum.com/blog/posts/chatgpt-apps-sdk-business-opportunity/)
- Bloomberg (March 30, 2026): "OpenAI's ChatGPT App Store Took Aim at Apple, But Results Lag So Far." Six months in, developers complained of a tedious approval process, a buggy coding system and no usage data — [Bloomberg (headline + snippet)](https://www.bloomberg.com/news/articles/2026-03-30/openai-s-chatgpt-app-store-took-aim-at-apple-but-results-lag-so-far)
- Alpic's chief of staff Dimitri Ewald said adoption and conversion are "pretty low" and "people don't even know that there are apps in the ChatGPT store". Apps like Sephora's don't launch from a generic cosmetics question, so users must already know the app exists and connect it — [Modern Retail (snippet; page blocked)](https://www.modernretail.co/technology/retailers-are-rushing-to-build-ai-apps-its-unclear-if-shoppers-will-use-them/)
- A developer forum snippet says OpenAI gives extra discoverability only to "proven apps", so testing mainly covers invocation once a user has already connected the app — [OpenAI Dev Community (snippet)](https://community.openai.com/t/chatgpt-apps-metada-for-discoverability/1371136)

### Inferences
- Custom GPTs are a dead end as a product strategy for anything launched now. The "custom GPT" half of the brief is obsolete. Existing GPT-store niches (astrology, resume, fitness GPTs) will lose many incumbents on December 11, 2026, and creators will rebuild as plugins. This is a short window where previously crowded GPT niches open up for well-built Apps SDK plugins.
- Because digital goods can't be sold in chat yet, indie monetization has to be external (freemium web app or subscription on your own domain, affiliate links, or lead generation). App concepts should be chosen so that ChatGPT acts as an acquisition funnel into a standalone product.
- Weak discoverability favors concepts that users seek out by name or share virally: shareable results, group-chat invites, and links. Concepts that only work if ChatGPT auto-routes a generic query are a poor bet.

### Gaps
- Could not read OpenAI's official monetization page or the release notes directly, because of the proxy block.
- No official per-category app counts from OpenAI. The only count found is the community GitHub list.

## Which categories are crowded vs. empty, and which big brands own them?

### Takeaway
B2B/SaaS categories (analytics, CRM, dev tools, design, documents) and branded transactional categories (travel, real estate, autos, food delivery, music) are crowded with big brands. Consumer **games, dating, personal tracking (fitness, habits, budgeting), and India-specific utilities** look thin in the directory. Education has big brands but is fragmented.

### Cited Findings
- Category snapshot (July 2, 2026, 1,624 apps, 44 categories) — [awesome-chatgpt-apps](https://github.com/rdmgator12/awesome-chatgpt-apps):
  - Analytics & Data, 70+ apps (Datadog, PostHog, Mixpanel, Amplitude)
  - CRM & Sales, 60+ (HubSpot, Salesforce, Apollo.io, Stripe)
  - Education & Learning, 60+ (Coursera, Khan Academy, Chegg, DataCamp)
  - Design & Creative, 45+ (Figma, Canva, Adobe Photoshop/Express)
  - Automotive, 40+ (CarMax, Cars.com, Edmunds, CARFAX)
  - Documents & Files, 35+ (Docusign, Box, Dropbox, Adobe Acrobat)
  - Development Tools, 30+ (Replit, Vercel, GitHub, Netlify)
  - Audio & Music, 15 (Spotify, Apple Music, Shazam)
  - Finance (Square featured as "App of the Week")
  - Health & Fitness and "Spirituality and Wellness" are listed, but no counts were visible
  - No Games or Dating category was visible in the fetched content
- India-specific apps in the directory: CarWale, Internshala, College Vidya, LeapScholar — [awesome-chatgpt-apps](https://github.com/rdmgator12/awesome-chatgpt-apps)
- Swiggy (Food, Instamart, Dineout) is available in ChatGPT, Claude and Gemini via MCP. It was announced January 27, 2026, and AI-tool orders are cash-on-delivery only — [Business Standard](https://www.business-standard.com/companies/news/swiggy-enables-grocery-food-delivery-via-chatgpt-and-other-ai-tools-126012701092_1.html); [Republic World](https://www.republicworld.com/tech/swiggy-users-can-now-order-food-groceries-inside-chatgpt)
- Launch-partner brands own travel (Booking.com, Expedia), real estate (Zillow), design (Canva, Figma), music (Spotify), learning (Coursera) and grocery (Instacart) — [OpenAI](https://openai.com/index/introducing-apps-in-chatgpt/); [Engadget](https://www.engadget.com/ai/openai-just-launched-an-app-store-inside-chatgpt-133049586.html)
- In the legacy GPT Store (159,000+ public GPTs), popular categories were personal assistants, learning to program, image generation, creative writing, gaming and entertainment. The top GPTs (January 2024) were Consensus, AI PDF, Grimoire, Canva, AskYourPDF, Logo Creator, WebPilot, ScholarAI, VideoGPT — [gptreview.io](https://www.gptreview.io/blog/the-most-popular-gpts-in-the-openai-gpt-store); [Wikipedia: GPT Store](https://en.wikipedia.org/wiki/GPT_Store)

### Inferences
- Avoid: travel booking, real estate, food delivery (Swiggy in India), music, design and documents. Brands with inventory or data moats already own these.
- Underserved (based on the absence of visible categories and brands): games and trivia, dating and social, personal tracking with persistence, regional and vernacular utilities, and exam-specific prep for Indian competitive exams.
- Gaming and entertainment were top GPT Store categories, but the app directory shows no visible games category. That suggests demand existed under GPTs and has not yet moved to Apps SDK supply.

### Gaps
- Could not confirm exact counts for Health & Fitness, Games, Lifestyle or Dating in the current Plugin Directory.
- Could not access the directory's live UI to check whether a Games category exists after the July 2026 Plugin migration.

## What do users repeatedly do manually with long prompts that a UI widget could do better?

### Takeaway
OpenAI's own usage research shows that "practical guidance" (tutoring, how-to, ideas), information seeking and writing make up about 80% of usage, and 70% of usage is non-work. Repeated manual prompt workflows (workout plans, meal plans, kundli analysis) are visible in the market for paid prompt packs and Notion templates. That market is indirect evidence that people want structure and persistence ChatGPT lacks.

### Cited Findings
- About 80% of conversations fall into practical guidance, seeking information and writing. About 49% are "Asking", 40% "Doing" (drafting, planning, programming) and 11% "Expressing" (reflection, exploration, play). About 70% are non-work. Data covers May 2024 to June 2025 — [OpenAI/NBER paper](https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf); [CNBC](https://www.cnbc.com/2025/09/17/openai-releases-first-of-kind-study-revealing-how-people-use-chatgpt.html)
- Practical guidance includes tutoring and teaching, how-to advice and creative ideas — [Entrepreneur](https://www.entrepreneur.com/business-news/how-people-are-using-chatgpt-openai-study/497193)
- Two-thirds of writing requests edit, translate, critique or modify existing text rather than generate new text — [OpenAI/NBER paper](https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf); [TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/openai-reveals-biggest-ever-study-of-how-people-are-using-chatgpt-here-are-3-things-weve-learned)
- A cottage industry sells "ChatGPT prompts for workout plans", meal-plan prompt packs and Notion gym/meal trackers on Gumroad. People pay for repeatable prompts plus external tracking — [Gumroad: workout prompts](https://chatgptaihubcom.gumroad.com/l/ChatGPT-Prompts-for-workout-plans); [Gumroad: meal](https://progresspro.gumroad.com/l/meal); [Gumroad: Gym tracker](https://vairusstrategy.gumroad.com/l/Gym-tracker); [Gumroad: AI Fitness Health Tracker](https://imryansteven.gumroad.com/l/AI-Powered-Fitness-Health-Tracker)
- Tom's Guide tested ChatGPT as an exercise coach and noted that users have to "build your own" tracking to follow progress — [Tom's Guide](https://www.tomsguide.com/ai/i-asked-chatgpt-to-become-my-exercise-coach-heres-what-happened)
- Prompt-template sites publish long "ChatGPT prompt for Kundli analysis" templates, evidence of a repeated manual astrology workflow — [promptjio](https://promptjio.com/astrology/chatgpt-prompt-for-kundli-analysis)

### Inferences (concrete app concepts)
- **"LiftLog": a workout plan and tracker widget.** It generates a program, then renders an inline set/rep logging table that persists across chats on your backend, with a progress chart. This replaces the Gumroad prompt-pack plus Notion-tracker combo.
- **"PlatePlan": a weekly meal-plan widget.** An editable 7-day grid, an auto-generated grocery checklist and macro totals. Optional export to the user's own grocery app; in India, a deep link to Instamart or Swiggy, which are already in ChatGPT.
- **"Redline Resume": a resume and job-fit editor.** Side-by-side diff against a job description, with a match score and accept/reject buttons per edit. This fits the "two-thirds of writing is editing" finding. Avoid job search listings, where brands like Internshala already exist.
- **"Flashdeck": spaced-repetition flashcards.** Turns any chat, PDF or notes into a card deck with an inline flip-card widget and SRS scheduling stored server-side. Fits "tutoring/teaching" as the top practical-guidance use.
- These are inferences from usage patterns and prompt-pack markets, not validated by search-volume data.

### Gaps
- No Google Trends or keyword-volume data was retrieved for "ChatGPT meal plan", "ChatGPT workout plan" and similar terms.
- No Reddit threads were retrieved. Search returned Gumroad products instead of r/ChatGPT complaint threads.

## What do users complain ChatGPT can't do natively?

### Takeaway
The most visible native gaps are **reliable reminders and recurring tracking** (Scheduled Tasks are capped, paid-only, and notify rather than act), **persistent structured state** (progress logs), and **multiplayer** interaction. Group chats now exist, but there is no evidence of rich group games or apps built for them.

### Cited Findings
- A developer forum thread is titled "Recurring task limitations are counterintuitive" — [OpenAI Dev Community](https://community.openai.com/t/recurring-task-limitations-are-counterintuitive/1391695)
- Scheduled Tasks are described as a "reminder-and-monitor tool, not an execution engine". They are capped at roughly once an hour, can't use voice, files or custom GPTs, auto-pause when ignored, and are paid-only — [usecarly (snippet; page blocked)](https://www.usecarly.com/blog/chatgpt-scheduled-tasks/)
- Reported caps on active tasks conflict: one source says 10 active tasks, another says five on a Plus seat — [chatai.guide](https://chatai.guide/features/chatgpt-tasks/); [notis.ai](https://www.notis.ai/blog/chatgpt-limitations-2026-workarounds/)
- SEO pages titled "Can ChatGPT Set Reminders? No—Here's What Works" and "Ask ChatGPT to Remind You Daily: Why It Doesn't Work" show that people search for this — [yougot.ai](https://www.yougot.ai/blog/ai-search/chatgpt-reminders/can-chatgpt-set-reminders); [yougot.ai](https://www.yougot.ai/blog/ai-search/chatgpt-reminders/ask-chatgpt-to-remind-me-daily)
- ChatGPT Group Chats support up to 20 participants and are available globally on Free, Go, Plus and Pro. OpenAI's example use case is planning a trip with friends — [VentureBeat](https://venturebeat.com/ai/chatgpt-group-chats-are-here-but-not-for-everyone-yet); [GSMArena](https://m.gsmarena.com/openai_chatgpt_group_chats_global_rollout-amp-70394.php); [Gulf News](https://gulfnews.com/technology/media/chatgpt-launches-group-chats-globally-letting-users-collaborate-with-ai-and-friends-1.500355781)
- Gizmodo called group chats "baffling", a sign of an unclear value proposition — [Gizmodo](https://gizmodo.com/openai-launches-baffling-group-chats-so-you-and-your-friends-can-hang-out-with-chatgpt-2000689280)

### Inferences (concrete app concepts)
- **"Streak": a habit and reminder app.** Persistent check-ins with WhatsApp, SMS or email nudges sent from the developer's backend, so it doesn't depend on the capped native Tasks. Logging happens inline in chat through a widget. This directly targets the "Can ChatGPT set reminders? No" search intent.
- **"Split & Plan": a group trip/expense app for group chats.** Shared itinerary voting, cost splitting and a packing list. It fills the group-chat use case OpenAI itself highlights, where no app owns the group-coordination layer. Avoid booking, where Booking.com and Expedia dominate. Link out to them instead.
- Whether Apps SDK widgets render and accept input in group chats was not confirmed (see Gaps). This is critical to validate before building multiplayer concepts.

### Gaps
- Could not confirm whether Apps SDK apps work inside Group Chats, or whether widgets support shared multi-user state.
- No direct Reddit or X complaint threads were retrieved.

## Emerging-market / India-specific opportunities

### Takeaway
India is ChatGPT's #2 market (100M weekly users). Free ChatGPT Go and ads on Free/Go (from August 2026) signal a very large, low-paying user base. Swiggy covers food and grocery, and a few education/auto brands are present. Astrology already has at least one plugin (Steer Astro) and standalone KundliGPT, so it is contested but not brand-dominated. Exam prep (JEE/NEET/UPSC) and vernacular utilities have no identified dominant ChatGPT app.

### Cited Findings
- India has 100 million weekly active ChatGPT users and is the second-largest market behind the US (Altman, ahead of the India AI Impact Summit) — [Unite.AI](https://www.unite.ai/india-becomes-chatgpts-second-largest-market-with-100-million-weekly-users/)
- OpenAI launched sub-$5 ChatGPT Go in India in August 2025. On October 27, 2025 it made Go free for one year for all users in India. It advertised heavily during IPL and WPL cricket — [TechCrunch](https://techcrunch.com/2025/10/27/openai-offers-free-chatgpt-go-for-one-year-to-all-users-in-india); [TechCrunch](https://techcrunch.com/2026/08/27/openai-to-start-showing-ads-on-chatgpts-free-and-go-tiers-in-india/)
- OpenAI began showing ads on Free and Go in India in August 2026. India is a testing ground where user numbers are high but payments lag — [TechCrunch](https://techcrunch.com/2026/08/27/openai-to-start-showing-ads-on-chatgpts-free-and-go-tiers-in-india/); [CNBC](https://www.cnbc.com/2026/08/28/openai-strategy-india-anthropic-ipo.html)
- Swiggy Food, Instamart and Dineout work in ChatGPT via MCP, with cash on delivery only for AI-tool orders — [Business Standard](https://www.business-standard.com/companies/news/swiggy-enables-grocery-food-delivery-via-chatgpt-and-other-ai-tools-126012701092_1.html); [india.com](https://www.india.com/news/india/swiggy-integrates-ai-tools-order-food-through-chatgpt-gemini-check-complete-process-here-instamart-dineout-8283457/)
- India-specific apps already in the directory: CarWale, Internshala, College Vidya, LeapScholar — [awesome-chatgpt-apps](https://github.com/rdmgator12/awesome-chatgpt-apps)
- Astrology competition: the Steer Astro plugin (Vedic birth charts, transits, dashas, Panchang in ChatGPT), KundliGPT (by NIT-Surat alumnus Raj Sutariya) and GPT-store GPTs such as "AstroSagga GPT" — [Steer Astro](https://chatgpt.com/plugins/steer-astro); [IndiaAI](https://indiaai.gov.in/article/gpt-tools-now-available-even-for-astrology); [kundligpt.com](https://kundligpt.com/features/ai-chat/); [AIPRM listing](https://app.aiprm.com/gpts/g-ufDu1ieo8/astrosagga-gpt-vedic-astrology-and-kundli-analysis)
- Exam-prep context: early reports found ChatGPT failed UPSC prelims (54/100) and scored 359/800 on NEET. These are older model results and show accuracy risk for exam content — [Gulf News](https://gulfnews.com/world/asia/india/ai-chatbot-chatgpt-unable-to-clear-upsc-exams-report-1.1677933491223); [IndiaAI](https://indiaai.gov.in/news/chatgpt-fails-to-clear-the-prestigious-civil-service-examination)

### Inferences (concrete app concepts)
- **"PYQ Arena": a JEE/NEET/UPSC previous-year-question practice widget.** Timed MCQ cards, topic-wise accuracy heatmaps and a spaced-repetition "mistake book". It is grounded in a verified question bank (to counter the accuracy risk shown above), with Hindi and regional-language toggles. No dominant ChatGPT app was found. Indian edtech incumbents (PW, Unacademy) were not seen in the directory snapshot, but this is unconfirmed.
- **"Kundli Match": a gun milan / marriage-compatibility widget.** A shareable compatibility card with a 36-guna score, for two people. Steer Astro covers individual charts, but a viral, shareable two-person matching flow is a differentiation angle. It is contested territory, so differentiate on shareability and Hindi output.
- **"Sarkari Saathi": a government-services form navigator.** Eligibility checker plus document checklist widgets for schemes, passport, PAN-Aadhaar and similar. This is inference only: no source in this research confirmed demand signals.
- **Cricket "Live Fantasy XI helper" or match-quiz:** cricket is clearly a mass channel (OpenAI advertised during IPL/WPL), but real-time sports data licensing is a cost risk. Inference only.
- Monetization in India should assume low willingness to pay. Ad-supported or B2B (coaching-institute white-label) models are likely better than subscriptions. Payments via UPI would have to be external, since in-chat digital-goods checkout isn't allowed.

### Gaps
- No Inc42, YourStory or Economic Times articles were retrieved on Indian ChatGPT usage patterns, exam-prep demand or UPI-in-ChatGPT.
- Could not confirm whether PhysicsWallah, Unacademy, Testbook, AstroTalk or Zomato have ChatGPT apps or plugins.
- No data on Hindi or regional-language share of Indian ChatGPT queries.

## Interactive / game-like apps inside chat (quizzes, personality tests, trivia, multiplayer)

### Takeaway
Gaming and entertainment were among the most popular GPT Store categories, and 11% of ChatGPT usage is "Expressing" (exploration, play). Yet no games category or game brands were visible in the app directory snapshot. Combined with 20-person Group Chats, this is a plausible white space. It is unvalidated: monetization and group-widget support are open questions.

### Cited Findings
- Gaming and entertainment were among the most popular GPT Store categories — [gptreview.io](https://www.gptreview.io/blog/the-most-popular-gpts-in-the-openai-gpt-store)
- 11% of messages are "Expressing" (personal reflection, exploration and play) — [OpenAI/NBER paper](https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf)
- Group Chats hold up to 20 participants on all consumer tiers — [VentureBeat](https://venturebeat.com/ai/chatgpt-group-chats-are-here-but-not-for-everyone-yet)
- No Games category was visible in the July 2026 directory snapshot — [awesome-chatgpt-apps](https://github.com/rdmgator12/awesome-chatgpt-apps)

### Inferences (concrete app concepts)
- **"Trivia Night": a host-mode quiz for group chats.** Generates themed rounds (Bollywood, IPL, office trivia) with a scoreboard widget. Viral via group invites.
- **"Which ___ Are You?": a personality-test engine.** An inline quiz widget that produces a shareable result card image. Shareable outputs are the main fix for the platform's discoverability problem.
- **Daily puzzle (a Wordle-style game with an AI twist):** a daily habit loop with a streak counter, stored server-side.
- Monetize externally (a premium web version or sponsored quiz packs), since digital goods can't be sold in chat.

### Gaps
- No examples found of successful game apps built on the Apps SDK, and no usage data.
- Unknown whether OpenAI's app review policy restricts games, or whether widgets support real-time multi-user state.

## Where do Apps SDK capabilities give a real advantage over plain chat?

### Takeaway
Widgets add real value where the output is **structured, stateful, editable or visual**: maps, carousels, grids, charts, flip cards, timers, scoreboards. Plain chat is good enough for one-shot advice. The launch examples (maps, playlists, slides) show OpenAI's intended pattern.

### Cited Findings
- Apps render interactive features such as maps, playlists and slides in chat, respond to natural language, and let developers build custom interfaces on MCP — [dig.watch](https://dig.watch/updates/chatgpt-introduces-new-generation-of-interactive-apps); [VentureBeat](https://venturebeat.com/ai/openai-announces-apps-sdk-allowing-chatgpt-to-launch-and-run-third-party); [OpenAI](https://openai.com/index/introducing-apps-in-chatgpt/)
- Tutorials show standard widget patterns, for example a pizza-ordering app with maps and carousels — [freeCodeCamp](https://www.freecodecamp.org/news/how-to-use-the-chatgpt-apps-sdk/); [RIIS](https://www.riis.com/blog/building-interactive-chatgpt-apps-with-openai%E2%80%99s-apps-sdk)
- Since July 2026, plugins can bundle skills plus apps, so a developer can ship prompt logic (the old "custom GPT" value) together with a UI widget — [Taskade](https://www.taskade.com/blog/chatgpt-plugins)

### Inferences
Each pattern below gets a clear advantage from a widget:
- An editable grid: meal plans, workout logs, study timetables.
- A flip or answer card with scoring: flashcards, PYQ practice, trivia.
- A diff view: resume edits.
- A shareable result card: personality tests, kundli matching.
- A map: local and regional services, though this risks overlap with Booking.com and Expedia for travel.
- A progress chart over time: any tracker. This needs the developer's own backend for persistence, which is also the main moat against ChatGPT adding the feature natively.

Weak fits are one-shot advice concepts (outfit rating, dating-profile review) that plain chat plus image upload already handles. They would need a shareable artifact or a persistent wardrobe/profile to justify an app.

### Gaps
- Could not read the Apps SDK docs directly to confirm the exact display modes (inline, fullscreen, picture-in-picture) and their constraints.
