# State of the ChatGPT Third-Party App / Plugin Platform (as of 2 Oct 2026)

> **Method caveat (read first):** WebFetch was blocked by the network egress proxy for every domain tried (openai.com, community.openai.com, wikipedia.org, axios.com, 9to5mac.com, learnetto.com). All findings below come from **search-engine result summaries/snippets**, not full-page reads. Citations point to the page the snippet came from. Facts that appeared in several independent results are noted as such; single-source claims, especially from SEO/aggregator blogs, are flagged. Before relying on any specific number, open the primary URL and check it.
>
> **Naming timeline (needed to read every source correctly):**
> - **2023 "ChatGPT plugins"**: deprecated. About 1,000 plugins at peak. **SUPERSEDED.**
> - **Jan 2024 GPT Store / custom GPTs**: still exists. Over 3M GPTs at launch. Revenue share never broadly launched.
> - **6 Oct 2025 "Apps in ChatGPT" + Apps SDK (MCP-based)**, announced at DevDay 2025. Submissions opened mid-Dec 2025; the **App Directory** opened at chatgpt.com/apps.
> - **26 Jan 2026 MCP Apps**: the interactive-UI extension became an official MCP standard. ChatGPT, Claude, VS Code and Goose support it.
> - **9 Jul 2026**: OpenAI **renamed "apps" to "plugins"**, and the **Plugin Directory replaced the App Directory**. A "plugin" now bundles skills + apps (MCP) + app templates. Apps still exist as the integration layer inside plugins. Docs appear to have moved to developers.openai.com/plugins/.
> - **29 Sep 2026 DevDay 2026**: **plugin extensions** (sidebar homes, interactive panels, file viewers, MCP Events automations), Plugin Creator, a redesigned submission flow, better ranking/recommendations, "Sign in with ChatGPT", Dots agents, and GPT-6.1 Sol.
>
> In late-2026 sources, "ChatGPT plugins" means the **new** MCP-based plugins, not the 2023 ones.

## 1. What is the Apps SDK / plugin platform: capabilities, limitations, review

### Takeaway
A ChatGPT "app" (inside a "plugin" since July 2026) is a remote **MCP server**: it exposes tools to the model and can also return sandboxed HTML/JS UI components. These render inline, in picture-in-picture or fullscreen, and keep their own state. At DevDay 2026 (29 Sep 2026) OpenAI added "plugin extensions": a plugin can now have a sidebar home, persistent interactive panels, custom file viewers and event-triggered automations, so it works much like a full app embedded in ChatGPT and Codex. Review requires a verified OpenAI Platform organization, a public HTTPS MCP endpoint, exact CSP domains and test cases. Reported turnaround is about 3–7 business days.

### Cited Findings
**Core architecture (Apps SDK, launched Oct 2025; still the base layer)**
- Apps are built on the Model Context Protocol (MCP), which lets ChatGPT connect to external tools and data. Users invoke an app by name or ChatGPT suggests it — [TechCrunch, 24 Oct 2025](https://techcrunch.com/2025/10/24/how-to-use-the-new-chatgpt-app-integrations-including-spotify-figma-canva-and-others); [OpenAI: Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/)
- Three display modes for the same widget: **inline** (in the message flow), **picture-in-picture/"pip"** (compact, overlays the chat) and **fullscreen**. A widget requests a mode with `window.openai.requestDisplayMode` — [OpenAI Apps SDK examples – PiP issue #87](https://github.com/openai/openai-apps-sdk-examples/issues/87); [DeepWiki window.openai API reference](https://deepwiki.com/openai/openai-apps-sdk-examples/4.2-window.openai-api-reference); [OpenAI Plugins reference docs](https://developers.openai.com/plugins/reference)
- State: `window.openai.widgetState` holds a snapshot of UI state that persists between renders. `setWidgetState(state)` stores a new snapshot, which propagates between views (e.g., inline to fullscreen) — [DeepWiki widget architecture](https://deepwiki.com/openai/openai-apps-sdk-examples/3.1-widget-architecture); [DeepWiki window.openai API reference](https://deepwiki.com/openai/openai-apps-sdk-examples/4.2-window.openai-api-reference)
- Environment signals widgets can read: theme, displayMode, maxHeight, safeArea, view, userAgent, locale — [DeepWiki window.openai API reference](https://deepwiki.com/openai/openai-apps-sdk-examples/4.2-window.openai-api-reference)
- Known rough edge: developers reported that calling setWidgetState() during requestDisplayMode() transitions caused progressive screen crashes on iOS — [OpenAI Developer Community thread](https://community.openai.com/t/setwidgetstate-during-requestdisplaymode-transitions-causes-progressive-screen-crash-on-ios/1374994)
- OpenAI has published practitioner guidance in "15 lessons learned building ChatGPT Apps" (content not retrieved) — [OpenAI developers blog](https://developers.openai.com/blog/15-lessons-building-chatgpt-apps)

**MCP Apps standard (cross-host UI)**
- MCP Apps went live on 26 Jan 2026 as the first official MCP extension. A tool can return an interactive HTML interface. Hosts at launch: Claude (web/desktop), Goose, VS Code Insiders and ChatGPT — [WorkOS, 27 Jan 2026](https://workos.com/blog/2026-01-27-mcp-apps); [Alpic AI](https://alpic.ai/blog/mcp-apps-goes-official-claude-chatgpt-support)
- MCP Apps render as isolated HTML/JS iframes that talk to the host over postMessage, which allows two-way interaction without a new prompt — [WorkOS](https://workos.com/blog/2026-01-27-mcp-apps)

**July 2026 restructure: apps became plugins**
- On 9 Jul 2026 OpenAI renamed ChatGPT apps to plugins and replaced the App Directory with the Plugin Directory. A plugin can bundle **skills** (reusable instructions, examples, code), **apps** (MCP connections) and **app templates**. Existing app connections were not affected — [OpenAI Help: Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex); [Taskade explainer](https://www.taskade.com/blog/chatgpt-plugins); [GitHub issue noting the rename](https://github.com/dnobj/mail-letter-irl/issues/476)
- The plugin directory is in ChatGPT web and desktop, and in ChatGPT Work and Codex — [OpenAI Help: Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex)
- First official business plugins (June 2026): "Creative Production" (Figma + Canva + Shutterstock + Picsart + Fal) and "Data Analytics" (Snowflake + Tableau). *Single aggregator source; unverified* — [Firecrawl blog](https://www.firecrawl.dev/blog/best-chatgpt-plugins)

**DevDay 2026 (29 Sep 2026): plugin extensions**
- Developers can build plugins that are "essentially entire applications that feel native to ChatGPT," distributed through OpenAI, e.g. "an editor, a dashboard, a whole workspace directly into ChatGPT and Codex" — [9to5Mac DevDay coverage](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/); [OpenAI DevDay 2026 Recap](https://openai.com/index/devday-2026-recap/)
- New surfaces: a dedicated **sidebar home**, **interactive panels** to use alongside chat, and **custom file viewers** for the developer's own file formats — [TechCrunch, 29 Sep 2026](https://techcrunch.com/2026/09/29/openai-expands-chatgpts-plugins-with-app-like-interfaces-and-automations/)
- **Automations:** OpenAI is adding support for the *proposed* **MCP Events** spec, so plugins can start automations when something happens in a connected app — [TechCrunch](https://techcrunch.com/2026/09/29/openai-expands-chatgpts-plugins-with-app-like-interfaces-and-automations/); [DEV Community](https://dev.to/techaiwire/chatgpt-plugin-extensions-add-app-panels-and-automations-2fhm)
- **ChatGPT Sites** (lightweight websites users build with ChatGPT) can host plugins, so a user can share an app with colleagues, who run it with their own connected data and permissions — [TechCrunch](https://techcrunch.com/2026/09/29/openai-expands-chatgpts-plugins-with-app-like-interfaces-and-automations/)
- Other DevDay items that affect plugin builders: **Dots** (always-on agents with their own computer/browser, "connected to over 4,000 apps in the ecosystem"); **Space** (a Drive-like workspace with native docs/slides/sheets apps); **Agents API** public beta; **GPT-6.1 Sol** — [9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/); [Axios](https://www.axios.com/2026/09/29/openai-dev-day-2026-dots-space-sol); [CNBC](https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html)

**Review and submission requirements**
- The submitter needs a **verified OpenAI Platform organization** (individual or business verification) and the Owner role, or "Apps Management Write" access — [OpenAI Help: Upload and submit your plugin](https://help.openai.com/en/articles/20001040-submitting-apps-to-the-chatgpt-app-directory); [BayramAnnakov submission_requirements.md](https://github.com/BayramAnnakov/chatgpt-app-skill/blob/main/chatgpt-app-builder/references/submission_requirements.md?plain=1)
- Technical requirements: the MCP server must be on a **public HTTPS domain** (no localhost/test endpoints), with **exact CSP domains**, streaming HTTP support and reasonable response times — [BayramAnnakov submission_requirements.md](https://github.com/BayramAnnakov/chatgpt-app-skill/blob/main/chatgpt-app-builder/references/submission_requirements.md?plain=1)
- Post-July 2026 flow: choose "With MCP" in the plugin submission portal, give the production `/mcp` URL, scan tools, verify the domain, define CSP, give reviewer credentials if auth is required, and add **5 positive + 3 negative test cases**. Plugins also include video walkthrough URLs and release notes in `plugin.json` — [sunpeak, "How to Submit a ChatGPT App as a Plugin (July 2026)"](https://sunpeak.ai/blogs/submit-chatgpt-app-as-plugin/); [OpenAI Help](https://help.openai.com/en/articles/20001040-submitting-apps-to-the-chatgpt-app-directory)
- DevDay 2026 added a **Plugin Creator** tool and a **redesigned submission flow with clearer feedback** — [TechCrunch](https://techcrunch.com/2026/09/29/openai-expands-chatgpts-plugins-with-app-like-interfaces-and-automations/); [InfoQ](https://www.infoq.com/news/2026/10/openai-devday-2026/)
- Reported approval time is **3–7 business days**. *Third-party claim, not an OpenAI SLA* — [Medium/TechTrends](https://medium.com/techtrends-digest/how-to-submit-your-app-to-chatgpt-and-actually-get-it-approved-f3b0d4b2b91f)
- Prohibited categories: apps may not sell, promote or facilitate adult content, sexual services, gambling, weapons or harmful materials — [OpenAI App submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)

### Inferences
- For an indie developer the unit of work is still "an MCP server + optional UI resources." Since MCP Apps is the shared standard, that one server should also run in Claude and other hosts (see §7). OpenAI-specific `window.openai` extras (display modes, widget state) are where portability may break.
- Plugin extensions (sidebar + panels + automations) move ChatGPT from "tool the model calls" toward "app the user opens," so persistent workspace-type products are now feasible. These were announced 3 days ago, so expect immature docs and bugs.
- An event-driven automation built on the *proposed* MCP Events spec is a fast-moving target. The spec may change.

### Gaps
- I could not read the current developers.openai.com/plugins docs in full, so I can't confirm the exact auth model (OAuth 2.1 with dynamic client registration was the Apps SDK pattern in 2025). The exact API names for the new sidebar/panel extension surfaces are also unconfirmed.
- No GA date found for plugin extensions (announced vs. available now vs. "soon").
- No official review SLA or published rejection rate.

## 2. Directory / store status: launch, rules, surfacing, regions

### Takeaway
Apps launched 6 Oct 2025 with partner apps. Third-party submissions opened around 17–18 Dec 2025, with the in-product App Directory at chatgpt.com/apps, and approved apps rolled out from early 2026. On 9 Jul 2026 the App Directory became the **Plugin Directory**. Discovery runs through the directory (browse featured/search), @-mention or naming the app in a prompt, and ChatGPT proactively suggesting apps in conversation. DevDay 2026 promised improved ranking and recommendations. Apps were not available in the EU at launch, and EU data residency is still not supported for apps.

### Cited Findings
- 6 Oct 2025 (DevDay 2025): apps rolled out to all logged-in ChatGPT users **outside the EU** on Free, Go, Plus and Pro — [TechCrunch](https://techcrunch.com/2025/10/24/how-to-use-the-new-chatgpt-app-integrations-including-spotify-figma-canva-and-others); [OpenAI: Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/)
- Submissions opened about 17–18 Dec 2025. Approved apps appear in an in-product **app directory**, found from the tools menu or at **chatgpt.com/apps**. Users can browse featured apps or search any published app. Approved apps rolled out gradually from **early 2026** — [OpenAI: Developers can now submit apps to ChatGPT](https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/); [OpenAI Devs on X](https://x.com/OpenAIDevs/status/2001419749016899868); [VentureBeat](https://venturebeat.com/technology/openai-now-accepting-chatgpt-app-submissions-from-third-party-devs-launches)
- Submissions include MCP connectivity details, testing guidelines, directory metadata and **country availability settings**. Status is tracked in the OpenAI Developer Platform — [OpenAI: Developers can now submit apps](https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/)
- Surfacing: (a) start a message with the app name ("Spotify, make a playlist…"); (b) ChatGPT **suggests apps in context**, e.g. Zillow when the user discusses buying a home — [TechCrunch](https://techcrunch.com/2025/10/24/how-to-use-the-new-chatgpt-app-integrations-including-spotify-figma-canva-and-others); [Storyboard18](https://www.storyboard18.com/how-it-works/openai-chatgpt-apps-chatgpt-apps-sdk-chatgpt-developers-canva-chatgpt-app-spotify-chatgpt-integration-expedia-chatgpt-app-coursera-chatgpt-zillow-chatgpt-figma-chatgpt-booking-com-chatgpt-op-82081.htm)
- OpenAI said apps that meet higher design and functionality standards / resonate with users "may be featured more prominently in the directory or recommended by ChatGPT" — [OpenAI: Developers can now submit apps](https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/) (via search summary)
- 9 Jul 2026: App Directory replaced by the **Plugin Directory**. Users add plugins there and authenticate the underlying app as before — [OpenAI Help: Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex)
- DevDay 2026: "improved ranking and recommendations in the directory and in conversations." "ChatGPT will soon be able to recommend relevant plugins during a conversation." OpenAI "will surface relevant plugins right in the conversations" — [InfoQ](https://www.infoq.com/news/2026/10/openai-devday-2026/); [DEV Community](https://dev.to/techaiwire/chatgpt-plugin-extensions-add-app-panels-and-automations-2fhm); [TechCrunch](https://techcrunch.com/2026/09/29/openai-expands-chatgpts-plugins-with-app-like-interfaces-and-automations/)
- Regions: "EU residency is not supported for apps; submissions must use global data residency project settings" — [BayramAnnakov submission_requirements.md](https://github.com/BayramAnnakov/chatgpt-app-skill/blob/main/chatgpt-app-builder/references/submission_requirements.md?plain=1)

### Inferences
- In-conversation recommendation is the distribution channel that matters. OpenAI says it is improving it, which makes tool naming/descriptions (how the model matches intent to your app) the main "ASO" lever.
- The "soon" wording about in-conversation recommendations at DevDay 2026 suggests proactive suggestion of *third-party* (not partner) apps may still be limited or rolling out.

### Gaps
- Could not confirm whether apps/plugins are now available to EU consumers in October 2026. The October 2025 EU exclusion is confirmed; the current status is not.
- No public criteria for "featured" placement, and no ranking algorithm details.
- No confirmation that Free-tier users get the full plugin directory after the July 2026 rename (the help article mentions web/desktop/Work/Codex).

## 3. Monetization: what actually exists and pays developers

### Takeaway
As of Oct 2026 there is **no OpenAI payout or revenue share for app/plugin developers** and **no in-ChatGPT way to sell digital goods**. Plugin guidelines allow commerce only for **physical goods**, plus letting existing customers use **entitlements they already own** (log in to your existing paid account). Selling subscriptions, credits or digital content, even indirectly through freemium upsells, is prohibited. Instant Checkout (ACP, built with Stripe) was **scaled back on 17 Mar 2026** after weak uptake; ChatGPT now sends shoppers to merchant-owned apps and sites. The GPT Store revenue program never broadly launched. The new **"Sign in with ChatGPT"** (DevDay 2026) does not pay developers, but it lets Plus/Pro users' subscriptions cover inference costs in partner apps.

### Cited Findings
**Apps/plugins commerce rules (current)**
- External checkout (the user completes the purchase on the developer's domain) is "the recommended and generally available approach" — [OpenAI Apps SDK: Monetization](https://developers.openai.com/apps-sdk/build/monetization)
- "Apps may conduct commerce only for physical goods; selling digital products or services, including subscriptions, digital content, tokens, or credits, is not allowed, whether offered directly or indirectly (for example, through freemium upsells)" — [OpenAI App submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines) (via search summary)
- Post-DevDay 2026 framing: plugins "may conduct commerce for physical goods and may let existing paid customers use entitlements they already own, but they may not sell digital products or services." No revenue share or paid-plugin model was announced at DevDay 2026 — [WorkOS: "Is this the AI era's App Store moment? Not yet"](https://workos.com/blog/ai-era-app-store-moment-openai-plugins) (via search summary)
- In-app checkout with the ChatGPT payment sheet was described as beta for select marketplace partners — [OpenAI Apps SDK: Monetization](https://developers.openai.com/apps-sdk/build/monetization)
- **Conflicting claim:** one blog says apps "support in-app purchases through Stripe and PayPal." This contradicts OpenAI's own guidelines above and is likely wrong — [snaplama 2026 guide](https://www.snaplama.com/blog/how-to-create-chatgpt-apps-and-monetize-them-complete-2026-guide) (low reliability)

**Agentic Commerce Protocol / Instant Checkout: SUPERSEDED / scaled back**
- (Prior state, 2025) OpenAI said it would support the Agentic Commerce Protocol, an open standard with Stripe, for instant checkout in ChatGPT — [OpenAI: Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/)
- Fee reports conflict: about 2% commission (attributed to Altman) vs. 4% on Instant Checkout sales from 26 Jan 2026 — [getchatads](https://www.getchatads.com/blog/chatgpt-checkout-affiliate-revenue/) vs. [ask-luca](https://ask-luca.com/blogs/chatgpt-4-fee-starting-jan-2026-what-smart-merchants-do-now) (both low-authority blogs)
- **17 Mar 2026:** OpenAI scaled back Instant Checkout. Users who find products are now sent to partner retailer apps (Instacart, Target, Expedia, DoorDash) to buy. OpenAI will focus on discovery and keep working with Stripe on ACP for **app-based** transactions — [TechRound](https://techround.co.uk/news/%E2%81%A0openai-scales-instant-checkout-feature-commerce/); [eMarketer](https://www.emarketer.com/content/how-payment-providers-should-react-openai-instant-checkout-walkback); [CNBC, 24 Mar 2026](https://www.cnbc.com/2026/03/24/openai-revamps-shopping-experience-in-chatgpt-after-instant-checkout.html); [MacRumors, 25 Mar 2026](https://www.macrumors.com/2026/03/25/chatgpt-revamps-shopping-features/); [PYMNTS](https://www.pymnts.com/artificial-intelligence-2/2026/openai-moves-commerce-focus-to-brand-owned-chatgpt-apps/)
- Reason: users researched products in ChatGPT but didn't complete purchases there. By Feb 2026 only about 30 Shopify merchants were live on Instant Checkout (Forrester's Emily Pfeiffer) — [TechRound](https://techround.co.uk/news/%E2%81%A0openai-scales-instant-checkout-feature-commerce/); [The Outpost](https://theoutpost.ai/news-story/open-ai-scales-back-chat-gpt-shopping-plans-as-instant-checkout-feature-fails-to-gain-traction-24385/)

**GPT Store revenue share: effectively never shipped broadly**
- The revenue program "never broadly launched." As of early 2026 it is reportedly a limited, invite-only pilot for a small group of US builders, with no new builders accepted — [digitalapplied GPT Store guide 2026](https://www.digitalapplied.com/blog/gpt-store-custom-gpts-business-guide-2026); [OpenAI Community thread on revenue share status](https://community.openai.com/t/what-is-the-status-with-gpt-store-revenue-share/839172)
- Payout figures ($100–500/month ceilings, about 25 conversations/week thresholds) circulate on SEO blogs and are **unverified**. Another source contradicts the "pilot only" framing by saying the program rolled out to most major markets. **Treat both as unreliable** — [thegptshop.online](https://www.thegptshop.online/blog/openai-gpt-store-revenue-sharing); [wildnetedge](https://www.wildnetedge.com/blogs/gpt-store-monetization-guide)

**"Sign in with ChatGPT" (DevDay 2026): an indirect economics lever**
- ChatGPT Plus and Pro subscribers can use their plan allowance inside third-party tools. 16 launch partners include OpenCode, Devin, Amp, Warp, Notion and Vercel. Users set weekly caps per app. When the cap is hit, usage stops; it does not switch to the partner's billing — [The New Stack](https://thenewstack.io/sign-in-with-chatgpt/); [explainx](https://www.explainx.ai/blog/openai-sign-in-with-chatgpt-devday-2026); [DEV Community](https://dev.to/axrisi/openai-devday-2026-every-announcement-with-prices-and-availability-1mbh)
- Effect for developers: "the user's subscription pays for the inference, so your margin stops depending on how much a heavy user prompts" — [DEV Community](https://dev.to/techaiwire/chatgpt-plugin-extensions-add-app-panels-and-automations-2fhm)

### Inferences
- For an indie developer, money comes from outside ChatGPT: the app is a funnel (acquisition and engagement) to the developer's own site or subscription, where the user signs up or pays. Inside ChatGPT the app can serve users who already hold an entitlement (log in to your existing paid account), but it cannot upsell them inside ChatGPT. Physical-goods affiliate/commerce flows via external checkout are allowed.
- The Instant Checkout retreat shows OpenAI moving to "discover in ChatGPT, transact in the brand's app/site." That favors developers who own a transaction surface.
- "Sign in with ChatGPT" mainly helps developers building standalone AI apps outside ChatGPT, not in-ChatGPT plugins. It is still a cost lever for an indie product that spans both.

### Gaps
- No evidence of any OpenAI developer payout, revenue share or paid-plugin listing for MCP apps/plugins as of Oct 2026.
- No confirmation whether "Sign in with ChatGPT" is open to all developers or only to the 16 launch partners.
- Did not verify whether ChatGPT ads (reported as coming in 2026) give app developers any promotion option.

## 4. Audience size: WAU, number of apps, usage stats

### Takeaway
ChatGPT reached about 800M weekly users at the Oct 2025 apps launch and about 900M by Feb 2026. Reports say it passed 1B by mid-2026, and at DevDay 2026 OpenAI cited **1.2B weekly users**. Over 50M paying subscribers were reported. No official count of directory apps/plugins was found. DevDay coverage mentions Dots connecting to "over 4,000 apps in the ecosystem," which is the best available proxy.

### Cited Findings
- About 800M+ weekly users at apps launch (Oct 2025) — [Storyboard18](https://www.storyboard18.com/how-it-works/openai-chatgpt-apps-chatgpt-apps-sdk-chatgpt-developers-canva-chatgpt-app-spotify-chatgpt-integration-expedia-chatgpt-app-coursera-chatgpt-zillow-chatgpt-figma-chatgpt-booking-com-chatgpt-op-82081.htm); [Yahoo Tech](https://tech.yahoo.com/ai/chatgpt/articles/connector-era-over-now-submit-093446755.html)
- 900M WAU in Feb 2026 (vs. 400M Feb 2025). Over 50M paying subscribers confirmed alongside it — [Superlines stats](https://www.superlines.io/articles/chatgpt-statistics/); [DemandSage](https://www.demandsage.com/chatgpt-statistics/) (aggregators citing OpenAI)
- WAU "surpassed 1 billion by July 31, 2026" (aggregator claim) — [Superlines stats](https://www.superlines.io/articles/chatgpt-statistics/); [Memeburn: "near 1 billion"](https://memeburn.com/chatgpt-weekly-active-users-near-1-billion/); another aggregator puts it at 900M as of Sept 2026: [TechnologyChecker.io](https://technologychecker.io/blog/chatgpt-statistics) (**conflict**)
- DevDay 2026: OpenAI "has over 1.2B weekly users and will surface relevant plugins right in the conversations" — [DEV Community](https://dev.to/techaiwire/chatgpt-plugin-extensions-add-app-panels-and-automations-2fhm); [WorkOS](https://workos.com/blog/ai-era-app-store-moment-openai-plugins)
- Dots "can be connected to over 4,000 apps in the ecosystem" — [9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/)
- Historical comparisons: about 1,000 plugins in the 2023 plugin store; over 3M GPTs at the GPT Store launch (Jan 2024) — [Firecrawl](https://www.firecrawl.dev/blog/best-chatgpt-plugins); [VentureBeat](https://venturebeat.com/ai/openai-launches-gpt-store-but-revenue-sharing-is-still-to-come)

### Inferences
- 1.2B WAU is the headline reach, but the share of users who actually invoke third-party plugins is unpublished and probably far smaller.
- "4,000 apps" may mix directory plugins with connectors and enterprise integrations, so it's a rough upper-bound proxy for directory competition.

### Gaps
- No official Plugin Directory listing count, no per-app usage, install or retention stats, and no breakdown of plugin usage by plan tier.
- The 1.2B figure came via secondary coverage; I could not confirm it on openai.com directly because fetch was blocked.

## 5. Launch partners and mechanics; notable indie apps

### Takeaway
The Oct 2025 launch partners were Booking.com, Canva, Coursera, Figma, Expedia, Spotify and Zillow. Each used the same pattern: invoked by name or suggested in context, returning an interactive card, map or list inline, with account linking for personalized actions. By 2026 the commerce partners (Instacart, Target, Expedia, DoorDash) became where shoppers are sent after the Instant Checkout retreat. No well-documented indie success story inside the new app/plugin directory was found.

### Cited Findings
- Launch partners: Canva, Spotify, Coursera, Expedia, Zillow, Figma, Booking.com — [Storyboard18](https://www.storyboard18.com/how-it-works/openai-chatgpt-apps-chatgpt-apps-sdk-chatgpt-developers-canva-chatgpt-app-spotify-chatgpt-integration-expedia-chatgpt-app-coursera-chatgpt-zillow-chatgpt-figma-chatgpt-booking-com-chatgpt-op-82081.htm); [OpenAI](https://openai.com/index/introducing-apps-in-chatgpt/)
- Mechanics: **Spotify** generates playlists; **Zillow** filters listings (e.g., 3 bed/3 bath) on an interactive map; **Booking.com/Expedia** show real-time hotel/flight data, price comparisons and interactive maps in chat; **Canva** creates designs/decks to spec (e.g., "a 16:9 slide deck about our Q4 roadmap") — [TechCrunch](https://techcrunch.com/2025/10/24/how-to-use-the-new-chatgpt-app-integrations-including-spotify-figma-canva-and-others); [Storyboard18](https://www.storyboard18.com/how-it-works/openai-chatgpt-apps-chatgpt-apps-sdk-chatgpt-developers-canva-chatgpt-app-spotify-chatgpt-integration-expedia-chatgpt-app-coursera-chatgpt-zillow-chatgpt-figma-chatgpt-booking-com-chatgpt-op-82081.htm); [shorttermrentalz](https://shorttermrentalz.com/news/chatgpt-launches-travel-apps-with-expedia-and-booking-com/)
- Post-March 2026 commerce routing goes to Instacart, Target, Expedia and DoorDash apps — [TechRound](https://techround.co.uk/news/%E2%81%A0openai-scales-instant-checkout-feature-commerce/)
- June 2026 business plugins bundle Figma, Canva, Shutterstock, Picsart, Fal (Creative Production) and Snowflake, Tableau (Data Analytics). *Single source* — [Firecrawl](https://www.firecrawl.dev/blog/best-chatgpt-plugins)
- Indie revenue examples that *do* surface (TypingMind about $50K/month, SiteGPT about $95K/month, early 2024) are **standalone products built on OpenAI's API, not in-ChatGPT apps**. They are not evidence of in-directory success — [search summary citing indie app roundups](https://mktclarity.com/blogs/news/indie-apps-top)

### Inferences
- Partner apps succeed because they already have big catalogs, inventory or accounts and use ChatGPT as a front door. An indie app needs a similarly crisp "noun the user names" (or a high-intent query category) to get invoked or recommended.

### Gaps
- No credible, sourced indie app/plugin with published user or revenue numbers inside the ChatGPT directory. The developer forum and HN were not reachable for fetch.
- Coursera and Figma mechanics were not detailed in retrieved snippets.

## 6. DevDay 2026 and other recent changes (Jul–Oct 2026)

### Takeaway
Recent changes, in order: the apps-to-plugins rename and Plugin Directory (9 Jul 2026), then DevDay 2026 (29 Sep 2026). DevDay brought plugin extensions (sidebar, panels, file viewers, MCP Events automations), Plugin Creator plus a new submission flow, better in-conversation recommendations, plugins hosted on ChatGPT Sites, Sign in with ChatGPT, Dots always-on agents (4,000+ apps), Space, the Agents API beta and GPT-6.1 Sol.

### Cited Findings
- DevDay 2026 was held 29 Sep 2026 in San Francisco with "more than 20 announcements" — [9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/); [CNBC](https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html); [OpenAI DevDay 2026 Recap](https://openai.com/index/devday-2026-recap/)
- Dots: always-on agents that work 24/7, have their own computer and browser, connect to 4,000+ apps, and reach users through ChatGPT, voice, Slack or Teams — [9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/)
- Space: a Google Drive-like workspace with ChatGPT-native docs/slides/spreadsheets apps — [9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/)
- GPT-6.1 Sol: better coding and computer use, at one-fifth the token price of "Astra". Agents API public beta with hosted execution, memory and computer use — [9to5Mac](https://9to5mac.com/2026/09/29/openai-teases-20-announcements-at-devday-watch-live/)
- Plugin extensions, Plugin Creator, submission redesign, MCP Events, Sites hosting: see §1 — [TechCrunch](https://techcrunch.com/2026/09/29/openai-expands-chatgpts-plugins-with-app-like-interfaces-and-automations/)
- Skeptical take: WorkOS argues it is "not yet" the AI era's App Store moment, citing no digital-goods sales and no revenue share — [WorkOS](https://workos.com/blog/ai-era-app-store-moment-openai-plugins)

### Inferences
- Dots plus 4,000 connected apps suggests plugins will increasingly be called **by agents in the background**, not only by users in chat. Builders should design tools that work headless as well as with UI.

### Gaps
- Exact availability and rollout dates for each DevDay 2026 plugin feature are unconfirmed. The community announcements page (community.openai.com/t/…/1402006) was blocked.

## 7. Same MCP server on other assistants (Claude, Gemini)

### Takeaway
Yes, with caveats. **Claude** supports MCP Apps (interactive UI) natively since 26 Jan 2026, with a directory at claude.ai/directory, so a standards-compliant MCP App can target both ChatGPT and Claude. **Gemini** (Gemini app / Gemini Spark) added third-party connected apps and custom MCP server URLs in mid-2026, but limited to US users 18+ on personal accounts. I found no evidence of an open third-party Gemini directory with interactive UI.

### Cited Findings
- MCP Apps "builds once to run in Claude and ChatGPT and any other host that implements the apps surface" — [WorkOS](https://workos.com/blog/2026-01-27-mcp-apps); [bytebot MCP Apps guide](https://bytebot.io/articles/mcp-apps)
- Claude: interactive connectors via MCP Apps launched 26 Jan 2026 with Asana, Canva, Figma, Slack, Box, Clay, Amplitude, Hex and Monday.com. Available on web/desktop for Pro, Max, Team and Enterprise. Users find them at **claude.ai/directory** (apps labeled "interactive") — [Claude blog: Interactive connectors and MCP Apps](https://claude.com/blog/interactive-tools-in-claude); [TechCrunch, 26 Jan 2026](https://www.techcrunch.com/2026/01/26/anthropic-launches-interactive-claude-apps-including-slack-and-other-workplace-tools/); [9to5Mac](https://9to5mac.com/2026/01/26/you-can-now-use-apps-like-slack-figma-and-canva-directly-inside-claude/)
- Gemini: Gemini Spark supports third-party apps including MCP (30 Jun 2026). Partners include Dropbox, Zillow, Canva, Instacart and OpenTable. Users can add a custom MCP server URL at gemini.google.com/apps — [9to5Google](https://9to5google.com/2026/06/30/gemini-spark-apps-more/); [Gemini Apps Help: custom apps](https://support.google.com/gemini/answer/17209137?hl=en)
- Gemini custom apps restrictions: 18+, **US only**, personal Google Account (not work/school) — [Gemini Apps Help](https://support.google.com/gemini/answer/17209137?hl=en)

### Inferences
- Building to the MCP Apps standard, rather than ChatGPT-only `window.openai` extras, maximizes reach across ChatGPT (1.2B weekly users), Claude (paid tiers only for interactive apps) and, to a lesser degree, Gemini (custom-URL, US-only). OpenAI-only features such as the new sidebar/panel extensions and display modes will need graceful fallbacks elsewhere.
- None of the three platforms has a confirmed developer payout model, so the funnel-to-own-billing approach applies across all of them.

### Gaps
- Whether Claude's directory accepts open third-party submissions (vs. curated partners), and its review process, were not confirmed.
- Whether Gemini renders MCP Apps UI (vs. tools only) is unconfirmed.
- Microsoft Copilot and other hosts were not researched.
