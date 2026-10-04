"""
Reddit lead agent for FreshLeads (no API key, runs on the Claude Max plan).

  python reddit_agent.py --scrape              pull fresh posts -> output/posts-DATE.json
  (Claude Code scores posts + drafts replies -> output/leads-DATE.json, see DAILY_RUN.md)
  python reddit_agent.py --digest FILE [--open] render leads JSON -> output/leads-DATE.html

Scraping uses Reddit's public RSS feeds: one multireddit feed per chunk of subreddits plus
site-wide search feeds for buying-intent phrases. ~10 requests per run, no login needed.
It never posts to Reddit. You post manually.
"""

import csv
import html
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
SEEN_FILE = ROOT / "seen.json"
LOG_FILE = ROOT / "leads_log.csv"
OUT_DIR = ROOT / "output"
ATOM = "{http://www.w3.org/2005/Atom}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
TODAY = datetime.now().strftime("%Y-%m-%d")
JUNK_SUB = re.compile(r"job|career|hiring|hiredev|slavelabour|beermoney|workonline")
JUNK_TITLE = re.compile(r"^\s*[\[(]\s*(for hire|offer|selling)", re.I)


# ---------- scraping ----------

def get_feed(session, path):
    """Fetch one RSS feed, backing off on 429 (anonymous feeds are rate limited)."""
    for wait in (0, 20, 60, 120):
        time.sleep(wait)
        try:
            r = session.get("https://www.reddit.com" + path, timeout=25)
        except requests.RequestException as ex:
            print(f"  ! network error: {ex}")
            continue
        if r.status_code == 200:
            return r.content
        if r.status_code != 429:
            print(f"  ! HTTP {r.status_code} for {path}")
            return None
        print("  rate limited, backing off ...")
    return None


def parse_feed(xml_bytes, source):
    posts = []
    for e in ET.fromstring(xml_bytes).iter(f"{ATOM}entry"):
        link = e.find(f"{ATOM}link").get("href")
        if "/comments/" not in link:
            continue
        content = e.findtext(f"{ATOM}content") or ""
        md = re.search(r'<div class="md">(.*)</div>', content, re.S)  # self-post body
        body = html.unescape(re.sub(r"<[^>]+>", " ", md.group(1) if md else ""))
        cat = e.find(f"{ATOM}category")
        published = e.findtext(f"{ATOM}published") or e.findtext(f"{ATOM}updated")
        posts.append({
            "id": (e.findtext(f"{ATOM}id") or link).replace("t3_", ""),
            "subreddit": cat.get("term") if cat is not None else "",
            "title": html.unescape(e.findtext(f"{ATOM}title") or ""),
            "body": re.sub(r"\s+", " ", body).strip()[:1500],
            "url": link,
            "author": (e.findtext(f"{ATOM}author/{ATOM}name") or "").replace("/u/", ""),
            "created": published,
            "age_hours": round((time.time() - datetime.fromisoformat(published).timestamp()) / 3600, 1),
            "source": source,
        })
    return posts


def feed_paths():
    rising = CONFIG.get("rising_subreddits", [])
    if rising:  # first, so these keep the "rising" label: early comments here get the most eyes
        yield "rising:" + "+".join(rising), f"/r/{'+'.join(rising)}/rising/.rss?limit=50"
    subs = CONFIG["subreddits"]
    for i in range(0, len(subs), 8):  # multireddit: many subs, one request
        chunk = subs[i:i + 8]
        yield "subs:" + "+".join(chunk), f"/r/{'+'.join(chunk)}/new/.rss?limit=100"
    for q in CONFIG["search_queries"]:  # buying intent anywhere on Reddit
        yield "search:" + q, f"/search.rss?q={quote(q)}&sort=new&t=week&limit=100"


def scrape():
    seen = set(json.loads(SEEN_FILE.read_text())) if SEEN_FILE.exists() else set()
    session = requests.Session()
    session.headers["User-Agent"] = UA
    me = CONFIG.get("my_reddit_username", "").lower()
    skip_subs = {s.lower() for s in CONFIG.get("exclude_subreddits", [])}
    max_age = CONFIG["max_post_age_hours"]
    keywords = [k.lower() for k in CONFIG["keywords"]]
    negatives = [k.lower() for k in CONFIG.get("negative_keywords", [])]

    found, titles = {}, set()
    for i, (source, path) in enumerate(feed_paths()):
        if i:
            time.sleep(7)
        xml_bytes = get_feed(session, path)
        if not xml_bytes:
            continue
        fresh = 0
        for p in parse_feed(xml_bytes, source):
            if (p["id"] in seen or p["id"] in found or p["age_hours"] > max_age
                    or p["author"].lower() == me or p["subreddit"].lower() in skip_subs):
                continue
            sub, title_key = p["subreddit"].lower(), re.sub(r"\W+", "", p["title"].lower())[:80]
            if title_key in titles or JUNK_SUB.search(sub) or JUNK_TITLE.search(p["title"]):
                continue  # cross-posts, job boards, people selling services
            text = (p["title"] + " " + p["body"]).lower()
            p["keyword_hits"] = [k for k in keywords if k in text]
            if any(n in text for n in negatives):
                continue
            if source.startswith("rising"):
                if p["age_hours"] > 10:  # only worth it while the post is still climbing
                    continue
            elif not p["keyword_hits"]:
                continue
            titles.add(title_key)
            found[p["id"]] = p
            fresh += 1
        print(f"  {source[:70]}: {fresh} new")

    posts = sorted(found.values(),
                   key=lambda p: (not p["source"].startswith("search"), -len(p["keyword_hits"]), p["age_hours"]))
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / f"posts-{TODAY}.json"
    if path.exists():  # second run same day: merge
        old = json.loads(path.read_text(encoding="utf-8"))
        posts = old + [p for p in posts if p["id"] not in {o["id"] for o in old}]
    path.write_text(json.dumps(posts, indent=1, ensure_ascii=False), encoding="utf-8")
    seen.update(found)
    SEEN_FILE.write_text(json.dumps(sorted(seen)[-20000:]))
    print(f"\n{len(found)} new posts -> {path}")


# ---------- inbox (replies, mentions, messages) ----------

INBOX_STATE = ROOT / "inbox_state.json"


def env(key):
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith(key + "="):
                return line.split("=", 1)[1].strip()
    return os.getenv(key, "")


def inbox():
    """Everything new in your Reddit inbox since the last check -> output/inbox-DATE.json."""
    feed = env("REDDIT_INBOX_FEED")
    if not feed:
        print("REDDIT_INBOX_FEED not set in .env (see README). Skipping inbox.")
        return
    state = json.loads(INBOX_STATE.read_text()) if INBOX_STATE.exists() else {"seen": []}
    seen = set(state["seen"])
    s = requests.Session()
    s.headers["User-Agent"] = UA
    m = re.search(r"/message/inbox/\.rss\?feed=\w+(?:&amp;|&)user=[\w-]+", feed)  # accepts a link or pasted XML
    if not m:
        print("REDDIT_INBOX_FEED doesn't look like an inbox RSS link. Skipping inbox.")
        return
    xml_bytes = get_feed(s, m.group(0).replace("&amp;", "&"))
    if not xml_bytes:
        return
    # what we replied to, so Claude knows the context of each conversation
    ours = {}
    for f in sorted(OUT_DIR.glob("leads-*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for l in (d.get("leads", []) if isinstance(d, dict) else d):
            ours[l["id"]] = {"their_post": l["title"], "their_post_body": l.get("body", "")[:600],
                             "our_reply": l.get("reply", "")}
    items = []
    for e_ in ET.fromstring(xml_bytes).iter(f"{ATOM}entry"):
        iid = e_.findtext(f"{ATOM}id") or ""
        if iid in seen:
            continue
        seen.add(iid)
        sender = (e_.findtext(f"{ATOM}author/{ATOM}name") or "").replace("/u/", "")
        if sender.lower() in {"automoderator", "reddit", "reddit_bot"} or sender.lower().endswith("bot"):
            print(f"  skipped bot message from {sender}")  # removals/notices, not people
            continue
        link_el = e_.find(f"{ATOM}link")
        link = link_el.get("href") if link_el is not None else ""
        content = html.unescape(re.sub(r"<[^>]+>", " ", e_.findtext(f"{ATOM}content") or ""))
        post_id = (re.search(r"/comments/(\w+)/", link) or [None, ""])[1]
        items.append({
            "id": iid,
            "kind": "message" if iid.startswith("t4_") else "comment reply / mention",
            "from": (e_.findtext(f"{ATOM}author/{ATOM}name") or "").replace("/u/", ""),
            "title": html.unescape(e_.findtext(f"{ATOM}title") or ""),
            "text": re.sub(r"\s+", " ", content).strip()[:1500],
            "url": link,
            "when": e_.findtext(f"{ATOM}updated"),
            "context": ours.get(post_id, {}),
        })
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / f"inbox-{TODAY}.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    path.write_text(json.dumps(old + items, indent=1, ensure_ascii=False), encoding="utf-8")
    state["seen"] = sorted(seen)[-5000:]
    INBOX_STATE.write_text(json.dumps(state))
    print(f"{len(items)} new inbox items -> {path}")


# ---------- digest ----------

def e(s):
    return html.escape(str(s or ""))


def card(i, l):
    dm = ""
    if l.get("dm"):
        user_url = f"https://www.reddit.com/message/compose/?to={e(l['author'])}"
        dm = (f'<details class="dm"><summary>DM opener (send after they reply to you)</summary>'
              f'<pre id="d{i}" contenteditable>{e(l["dm"])}</pre>'
              f'<button onclick="go(\'d{i}\',\'{user_url}\',this)">Copy DM + open chat</button></details>')
    promo = '<span class="tag">help only</span>' if l.get("no_promo") else ""
    return f"""
<div class="card" data-id="{e(l['id'])}" data-url="{e(l['url'])}" data-i="{i}">
  <div class="meta"><span class="num">{i + 1}</span><span class="badge">{l['ai_score']}/10</span>{promo}
    r/{e(l['subreddit'])} · {e(l.get('intent'))} · {l.get('age_hours', '?')}h old</div>
  <h3>{e(l['title'])}</h3>
  <p class="why">{e(l.get('why'))}</p>
  <details><summary>Original post</summary><p class="body">{e(l.get('body'))}</p></details>
  <pre id="r{i}" contenteditable title="Click to edit before copying">{e(l['reply'])}</pre>
  <div class="row">
    <button class="main" onclick="go('r{i}','{e(l['url'])}',this)">Copy reply + open thread <kbd>Enter</kbd></button>
    <button onclick="done({i},'replied')">Done <kbd>D</kbd></button>
    <button onclick="done({i},'skipped')">Skip <kbd>S</kbd></button>
    <select onchange="setS('{e(l['id'])}',this.value)">
      <option value="">status...</option><option>replied</option><option>DM sent</option>
      <option>talking</option><option>customer</option><option>skipped</option></select></div>
  {dm}
</div>"""


DAILY = ["Inbox replies first (top of this list), within a few hours",
         "3-5 rising-post comments (tagged RISING): be early, be the sharpest take in the thread",
         "Lead replies, spaced a few minutes apart",
         "Reply to every new comment on your own posts"]
WEEKLY = {  # weekday() -> growth task. Post days target US morning (8-10 AM Eastern)
    0: "Pick this week's 2 posts in the content kit, check those subs' rules and flair",
    1: "POST DAY: publish post #1 from the content kit, then answer every comment for 2 hours",
    2: "Crosspost yesterday's post to 1-2 related subs if it got 20+ upvotes. Answer late comments",
    3: "POST DAY: publish post #2 (engagement thread like the free email rewrite). Answer everything",
    4: "DM everyone who showed interest this week and send their free samples",
    5: "Turn your best-received comment of the week into a new post (ask Claude to expand it)",
    6: "Review leads_log.csv: which subs gave replies or customers? Ask Claude to drop the dead ones",
}


def routine_box(extra):
    tasks = DAILY + [WEEKLY[datetime.now().weekday()]] + list(extra or [])
    items = "".join(f'<label><input type="checkbox" data-t="{i}"> {e(t)}</label>' for i, t in enumerate(tasks))
    return f'<div class="card routine"><b>Today\'s routine</b>{items}</div>'


def digest(leads_file):
    data = json.loads(Path(leads_file).read_text(encoding="utf-8"))
    if isinstance(data, list):
        data = {"leads": data}
    leads = [l for l in data.get("leads", [])
             if l.get("ai_score", 0) >= CONFIG["min_relevance_score"] and l.get("reply")]
    leads.sort(key=lambda l: (-l["ai_score"], l.get("age_hours", 99)))
    leads = leads[:CONFIG["max_leads_per_run"]]
    # people who replied to / messaged us come first: they're the warmest leads
    priority = [{"id": m["id"], "url": m["url"], "subreddit": "inbox", "author": m["from"],
                 "title": f"u/{m['from']}: {m.get('title', '')}", "body": m.get("text", ""),
                 "ai_score": m.get("interest_score", 10), "intent": "REPLY TO THEM " + m.get("interest", ""),
                 "why": m.get("why", ""), "reply": m["draft"], "age_hours": "new", "dm": m.get("dm", "")}
                for m in data.get("inbox", []) if m.get("draft")]
    priority.sort(key=lambda l: -l["ai_score"])
    leads = priority + leads

    extra = ""
    if data.get("insights"):
        extra += "<h2>What prospects are saying</h2><ul>" + "".join(
            f"<li>{e(x)}</li>" for x in data["insights"]) + "</ul>"
    for j, vp in enumerate(data.get("value_posts", [])):
        extra += (f'<div class="card"><div class="meta">Value post idea · r/{e(vp.get("subreddit"))}</div>'
                  f'<h3>{e(vp.get("title"))}</h3><pre id="v{j}">{e(vp.get("body"))}</pre>'
                  f'<button onclick="cp(\'v{j}\',this)">Copy post</button></div>')

    stats = data.get("stats", {})
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>FreshLeads Reddit {TODAY}</title>
<style>
:root{{--bg:#f6f6f4;--card:#fff;--fg:#1a1a1a;--mute:#666;--line:#e3e3e0;--acc:#ff4500}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141414;--card:#1e1e1e;--fg:#eee;--mute:#999;--line:#333}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:24px 16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;margin:14px 0}}
.card.done{{opacity:.45}} .meta{{color:var(--mute);font-size:13px}} h3{{margin:6px 0}} a{{color:var(--acc)}}
.why{{color:var(--mute)}} pre{{white-space:pre-wrap;background:var(--bg);padding:12px;border-radius:8px;font:14px/1.5 system-ui}}
.body{{white-space:pre-wrap;font-size:14px}} .row{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
button,.btn,select{{cursor:pointer;padding:6px 12px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--fg);font:inherit;text-decoration:none}}
.badge{{background:var(--acc);color:#fff;border-radius:5px;padding:1px 7px;font-weight:600;margin-right:6px}}
.tag{{border:1px solid var(--acc);color:var(--acc);border-radius:5px;padding:0 6px;margin-right:6px;font-size:12px}}
.num{{font-weight:700;margin-right:8px;color:var(--fg)}} .card.cur{{border-color:var(--acc);box-shadow:0 0 0 2px var(--acc)}}
pre[contenteditable]{{outline:none;border:1px dashed transparent}} pre[contenteditable]:focus{{border-color:var(--acc)}}
button.main{{background:var(--acc);color:#fff;border-color:var(--acc);font-weight:600}}
kbd{{font:11px monospace;opacity:.7;margin-left:4px}}
.bar{{position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:2;border-bottom:1px solid var(--line)}}
.prog{{height:6px;background:var(--line);border-radius:3px;overflow:hidden;margin-top:6px}} .prog i{{display:block;height:100%;background:var(--acc);width:0}}
.links a{{margin-right:14px;font-size:14px}}
.routine label{{display:block;margin:6px 0;cursor:pointer}} .routine input{{margin-right:8px}}
</style></head><body>
<div class="bar"><b>FreshLeads · Reddit checklist {TODAY}</b> <span class="meta" id="count"></span> <b id="timer" style="margin-left:10px"></b>
<div class="prog"><i id="pbar"></i></div>
<div class="meta">Enter = copy reply + open thread → Ctrl+V → post → come back → D = done (jumps to next). S = skip. J/K = move.</div>
<div class="links"><a href="content_kit.html" target="_blank">Content kit (posts to publish)</a>
<a href="https://www.reddit.com/user/{e(CONFIG.get('my_reddit_username', ''))}" target="_blank">My profile</a></div></div>
{routine_box(data.get("growth_tasks"))}
<p class="meta">{stats.get('scanned', '?')} posts scanned · {len(leads)} items. Freshest first gets seen. New account: Reddit allows ~1 comment per 10 min, the timer shows when you can post again. Click any reply to edit it.</p>
{''.join(card(i, l) for i, l in enumerate(leads)) or '<p>No strong leads this run.</p>'}
{extra}
<script>
const cards=[...document.querySelectorAll('.card[data-id]')];let cur=0;
function copyText(t){{if(navigator.clipboard&&window.isSecureContext!==false){{navigator.clipboard.writeText(t).catch(()=>fb(t))}}else fb(t)}}
function fb(t){{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}
function cp(id,b){{copyText(document.getElementById(id).innerText);b.textContent='Copied'}}
function go(id,url,b){{copyText(document.getElementById(id).innerText);window.open(url,'_blank');if(b)b.firstChild.textContent='Copied + opened '}}
function st(){{try{{return JSON.parse(localStorage.getItem('fl_status')||'{{}}')}}catch(x){{return {{}}}}}}
function setS(id,v){{const s=st();s[id]=v;try{{localStorage.setItem('fl_status',JSON.stringify(s))}}catch(x){{}}paint()}}
function isDone(c){{const v=st()[c.dataset.id]||'';return !!v&&v!=='talking'}}
function focusCard(i){{if(!cards.length)return;cur=Math.max(0,Math.min(cards.length-1,i));cards.forEach(c=>c.classList.remove('cur'));
cards[cur].classList.add('cur');cards[cur].scrollIntoView({{behavior:'smooth',block:'center'}})}}
const GAP={CONFIG.get('comment_gap_minutes', 10)}*60000;
function tick(){{let t=0;try{{t=+localStorage.getItem('fl_last')||0}}catch(x){{}}const left=t+GAP-Date.now();const el=document.getElementById('timer');
if(left>0){{const m=Math.floor(left/60000),s=Math.floor(left%60000/1000);el.textContent='⏳ next comment in '+m+':'+String(s).padStart(2,'0');el.style.color='#e5a33b'}}
else{{el.textContent='✅ ready for next comment';el.style.color='#2ecc71'}}}}
setInterval(tick,1000);
function done(i,v){{if(v==='replied'){{try{{localStorage.setItem('fl_last',Date.now())}}catch(x){{}}tick()}}setS(cards[i].dataset.id,v);const n=cards.findIndex((c,k)=>k>i&&!isDone(c));
const m=n>=0?n:cards.findIndex(c=>!isDone(c));if(m>=0)focusCard(m)}}
function paint(){{const s=st();let d=0;cards.forEach(c=>{{const v=s[c.dataset.id]||'';c.querySelector('select').value=v;
const x=!!v&&v!=='talking';c.classList.toggle('done',x);if(x)d++}});
document.getElementById('count').textContent=' · '+d+'/'+cards.length+' done';
document.getElementById('pbar').style.width=(cards.length?100*d/cards.length:0)+'%'}}
document.addEventListener('keydown',ev=>{{if(ev.target.isContentEditable||/SELECT|INPUT|TEXTAREA/.test(ev.target.tagName))return;
const c=cards[cur];if(!c)return;const k=ev.key.toLowerCase();
if(k==='enter'){{go('r'+c.dataset.i,c.dataset.url,c.querySelector('button.main'));ev.preventDefault()}}
else if(k==='d')done(cur,'replied');else if(k==='s')done(cur,'skipped');
else if(k==='j')focusCard(cur+1);else if(k==='k')focusCard(cur-1)}});
cards.forEach((c,i)=>c.addEventListener('click',()=>{{cur=i;cards.forEach(x=>x.classList.remove('cur'));c.classList.add('cur')}}));
const RK='fl_routine_{TODAY}';function rs(){{try{{return JSON.parse(localStorage.getItem(RK)||'{{}}')}}catch(x){{return {{}}}}}}
document.querySelectorAll('.routine input').forEach(b=>{{b.checked=!!rs()[b.dataset.t];
b.onchange=()=>{{const s=rs();s[b.dataset.t]=b.checked;try{{localStorage.setItem(RK,JSON.stringify(s))}}catch(x){{}}}}}});
paint();const f=cards.findIndex(c=>!isDone(c));focusCard(f>=0?f:0);
</script></body></html>"""
    OUT_DIR.mkdir(exist_ok=True)
    path = OUT_DIR / f"leads-{TODAY}.html"
    path.write_text(page, encoding="utf-8")
    (OUT_DIR / "latest.html").write_text(page, encoding="utf-8")  # opened at PC startup

    new_log = not LOG_FILE.exists()
    logged = set() if new_log else {r[5] for r in csv.reader(LOG_FILE.open(encoding="utf-8")) if len(r) > 5}
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_log:
            w.writerow(["date", "score", "subreddit", "intent", "title", "url", "status"])
        for l in leads:
            if l["url"] not in logged:
                w.writerow([TODAY, l["ai_score"], l["subreddit"], l.get("intent", ""), l["title"], l["url"], ""])
    print(f"{len(leads)} leads -> {path}")
    if "--open" in sys.argv:
        open_in_chrome(OUT_DIR / "latest.html")


def open_in_chrome(path):
    for exe in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")):
        if os.path.exists(exe):
            subprocess.Popen([exe, str(path)])
            return
    os.startfile(path)  # fallback: default browser


if __name__ == "__main__":
    if "--scrape" in sys.argv:
        scrape()
    elif "--digest" in sys.argv:
        digest(sys.argv[sys.argv.index("--digest") + 1])
    elif "--inbox" in sys.argv:
        inbox()
    elif "--open-latest" in sys.argv:  # used by the Windows startup shortcut
        open_in_chrome(OUT_DIR / "latest.html")
    else:
        print(__doc__)
