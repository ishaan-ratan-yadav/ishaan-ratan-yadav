#!/usr/bin/env python3
"""Build the Daily Pack for the FreshLeads Reddit growth agent.

Reads a pack JSON (written by the agent), checks every title, post, comment and
reply against Reddit's norms and our own rules, and produces:
  * packs/<date>.html  - click-through page: copy buttons, "open submit page",
                         "copy comment + open thread", done boxes, comment-gap timer
  * Telegram messages  - optional, via the Bot API if config.json has a token

Nothing is ever posted to Reddit. Every button copies text and/or opens a Reddit
page. Ishaan reads it, pastes, and clicks Post himself.

Usage:
  python tools/rpack.py packs/2026-10-05.json              # build + Telegram (if configured)
  python tools/rpack.py packs/2026-10-05.json --no-send    # build only
  python tools/rpack.py --check "comment text" [--sub agency] [--title]
"""

import argparse
import csv
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLE_MAX = 300          # Reddit hard limit
TITLE_SOFT = 150         # past this, feeds cut the title; the hook must be in the first ~90 chars
COMMENT_SOFT_WORDS = 150  # long comments sink in fast threads (aim 30-90 words for rising targets)
PROMO_MAX_SHARE = 0.10   # the 90/10 rule, measured across the whole pack
URL_ENC_MAX = 7000       # keep prefilled submit URLs well under browser/server limits

URL_RE = re.compile(r"https?://\S+|\bwww\.\S+", re.I)
BARE_DOMAIN_RE = re.compile(r"(?<![@\w.-])[a-z0-9-]+\.(?:io|com|co|ai|app|net|org|so|xyz|dev)\b", re.I)  # emails are not links
HASHTAG_RE = re.compile(r"(?<![\w&/#])#[A-Za-z][\w]+")
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF\uFE0F\u200d\u2B50\u2B06\u2B07\u2934\u2935]")
PROMO_RE = re.compile(r"fresh\s?leads|getfreshleads|sample leads|free leads|5 free|my (?:service|product|tool|startup|saas)"
                      r"|link (?:is )?in (?:my )?(?:bio|profile)|dm me for", re.I)
WEAK_OPENERS = ("hey", "hi ", "hi,", "hello", "so,", "so i", "just wanted", "quick question", "i have a question",
                "need help", "help needed", "help!", "thoughts?", "first post", "update:", "please help", "guys")
AI_TELLS = ("delve", "leverage", "robust", "seamless", "game-changer", "game changer", "unlock", "elevate", "navigate the",
            "landscape", "crucial", "pivotal", "foster", "streamline", "in today's", "it's worth noting", "great question",
            "totally get this", "happy to help", "as someone who", "here's the thing", "hope this helps", "in short,",
            "bottom line", "good luck on your journey", "let that sink in", "unleash", "supercharge", "testament to",
            "in conclusion", "furthermore", "moreover", "tapestry")
DASHES = ("\u2014", " \u2013 ")  # em dash anywhere, en dash used as a pause


# ---------------------------------------------------------------- config + memory

def load_config() -> dict:
    for name in ("config.json", "config.example.json"):
        p = ROOT / name
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(f"{name} is not valid JSON ({exc}). Using defaults.", file=sys.stderr)
    return {}


CFG = load_config()


def norm_sub(s: str) -> str:
    return re.sub(r"^/?r/", "", (s or "").strip()).strip("/").lower()


def load_intel() -> dict:
    """Parse the machine-readable table in memory/subreddit-intel.md.

    Columns: Sub | Promo | Links | Flair req | Min karma / age | Post types | Notes | Verified
    Promo: no / thread / ok / ?   Links: no / ok / ?   Flair req: yes / no / ?   Post types: text,image,link,gallery
    """
    path = ROOT / "memory" / "subreddit-intel.md"
    intel = {}
    if not path.exists():
        return intel
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("| r/"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        intel[norm_sub(cells[0])] = {
            "promo": cells[1].lower(), "links": cells[2].lower(), "flair": cells[3].lower(),
            "gate": cells[4], "types": cells[5].lower(), "notes": cells[6] if len(cells) > 6 else "",
        }
    for s in CFG.get("no_promo_subreddits", []):
        intel.setdefault(norm_sub(s), {"promo": "no", "links": "?", "flair": "?", "gate": "", "types": "?", "notes": ""})
        if intel[norm_sub(s)]["promo"] in ("?", ""):
            intel[norm_sub(s)]["promo"] = "no"
    return intel


INTEL = load_intel()


def thread_id(url: str) -> str | None:
    m = re.search(r"/comments/([a-z0-9]+)", url or "", re.I)
    return m.group(1).lower() if m else None


def load_seen_threads() -> dict:
    """Thread ids we (comment-log) or the lead agent already handled -> who."""
    seen = {}
    log = ROOT / "memory" / "comment-log.csv"
    if log.exists():
        for row in csv.DictReader(log.open(encoding="utf-8")):
            tid = thread_id(row.get("thread_url", ""))
            if tid and row.get("status", "") in ("posted", "commented", ""):
                seen[tid] = "we already commented here (memory/comment-log.csv)"
    lead_dir = Path(CFG.get("lead_agent_dir", "H:/claude/reddit  scrap"))
    try:
        files = sorted((lead_dir / "output").glob("leads-*.json"))[-10:]
    except OSError:
        files = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for lead in (data.get("leads", []) if isinstance(data, dict) else data):
            tid = thread_id(lead.get("url", ""))
            if tid:
                seen.setdefault(tid, f"lead agent drafted a reply here ({f.name})")
    lead_log = lead_dir / "leads_log.csv"
    try:
        if lead_log.exists():
            for row in csv.reader(lead_log.open(encoding="utf-8")):
                for cell in row:
                    tid = thread_id(cell)
                    if tid:
                        seen.setdefault(tid, "lead agent logged this thread (leads_log.csv)")
    except OSError:
        pass
    return seen


# ---------------------------------------------------------------- checks

def warmup_active(pack_date: str, phase: str | None) -> bool:
    if phase:
        return phase.lower().startswith("warm")
    until = CFG.get("warmup_until", "")
    try:
        d = date.fromisoformat(pack_date)
    except (TypeError, ValueError):
        d = date.today()
    try:
        return d < date.fromisoformat(until)
    except ValueError:
        return False


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text or ""))


def is_promo(text: str) -> bool:
    return bool(PROMO_RE.search(text or ""))


def has_link(text: str) -> bool:
    return bool(URL_RE.search(text or "") or BARE_DOMAIN_RE.search(text or ""))


def style_problems(text: str) -> list[str]:
    probs = []
    low = (text or "").lower()
    for d in DASHES:
        if d in text:
            probs.append("em/en dash: use a comma, period or 'and'")
            break
    if EMOJI_RE.search(text or ""):
        probs.append("emoji: remove it")
    if HASHTAG_RE.search(text or ""):
        probs.append("hashtag: Reddit has none, it reads as spam")
    hits = [t for t in AI_TELLS if t in low]
    if hits:
        probs.append("AI-sounding: " + ", ".join(f"'{h}'" for h in hits[:4]))
    if text.count("!") >= 2:
        probs.append("exclamation marks read as marketing: drop them")
    return probs


def check_text(text: str, *, sub: str = "", warmup: bool = False, kind: str = "comment",
               promo_declared: bool = False) -> tuple[list[str], list[str]]:
    """Return (blockers, warnings) for a body/comment/reply."""
    blockers, warns = [], style_problems(text)
    rules = INTEL.get(norm_sub(sub), {})
    promo = promo_declared or is_promo(text)
    link = has_link(text)
    if warmup and promo:
        blockers.append("product mention during warm-up (no promo until warmup_until)")
    if warmup and link:
        blockers.append("link during warm-up: links from a new account trip the spam filter")
    if rules.get("promo") == "no" and promo:
        blockers.append(f"r/{norm_sub(sub)} bans self-promotion (memory/subreddit-intel.md)")
    if rules.get("promo") == "thread" and promo and kind == "post":
        blockers.append(f"r/{norm_sub(sub)} allows promo only in its designated thread")
    if rules.get("links") == "no" and link:
        blockers.append(f"r/{norm_sub(sub)} bans links")
    words = word_count(text)
    if kind in ("comment", "reply") and words > COMMENT_SOFT_WORDS:
        warns.append(f"{words} words: long comments sink, aim for 30-90 (rising) or 40-120 (help)")
    if kind == "dm" and link:
        warns.append("link in a first DM looks like spam: send it only after they say yes")
    return blockers, warns


def check_title(title: str, sub: str = "", warmup: bool = False) -> tuple[list[str], list[str]]:
    blockers, warns = [], style_problems(title)
    n = len(title or "")
    if n == 0:
        blockers.append("empty title")
    if n > TITLE_MAX:
        blockers.append(f"title {n}/{TITLE_MAX} chars (Reddit's hard limit)")
    elif n > TITLE_SOFT:
        warns.append(f"title {n} chars: feeds cut long titles, keep the hook in the first ~90")
    low = (title or "").strip().lower()
    if low.startswith(WEAK_OPENERS):
        warns.append("weak opener: lead with the hook (number, result, tension), not a greeting")
    if has_link(title):
        blockers.append("link in title")
    caps = [w for w in re.findall(r"\b[A-Z]{4,}\b", title or "") if w not in ("SMTP", "HTML", "B2B", "DTC", "D2C", "CEO", "ROAS", "SaaS", "TLDR", "UGC", "AMA", "LLM", "IST")]
    if len(caps) > 1:
        warns.append("shouty caps read as clickbait")
    if warmup and is_promo(title):
        blockers.append("product name in title during warm-up")
    return blockers, warns


def check_post(p: dict, warmup: bool) -> tuple[list[str], list[str]]:
    sub = p.get("subreddit", "")
    b1, w1 = check_title(p.get("title", ""), sub, warmup)
    b2, w2 = check_text(p.get("body", ""), sub=sub, warmup=warmup, kind="post", promo_declared=p.get("promo", False))
    blockers, warns = b1 + b2, w1 + w2
    rules = INTEL.get(norm_sub(sub), {})
    if rules.get("flair") == "yes" and not p.get("flair"):
        warns.append(f"r/{norm_sub(sub)} requires flair: set 'flair' (AutoModerator removes unflaired posts)")
    ptype = (p.get("type") or "text").lower()
    types = rules.get("types", "?")
    if types not in ("?", "", "any") and ptype not in types:
        warns.append(f"r/{norm_sub(sub)} allows {types} posts, this is {ptype}")
    if "title-tag" in rules.get("notes", "").lower() and not p.get("title", "").lstrip().startswith("["):
        blockers.append(f"r/{norm_sub(sub)} requires a bracketed tag at the start of the title, e.g. [US] or [Global] (AutoModerator removes posts without it)")
    if p.get("first_comment"):
        b3, w3 = check_text(p["first_comment"], sub=sub, warmup=warmup, kind="comment")
        blockers += [f"first comment: {x}" for x in b3]
        warns += [f"first comment: {x}" for x in w3]
    if not norm_sub(sub):
        blockers.append("no subreddit")
    elif norm_sub(sub) not in INTEL and not norm_sub(sub).startswith("u_"):
        warns.append(f"r/{norm_sub(sub)} not in memory/subreddit-intel.md: read its rules page first")
    return blockers, warns


# ---------------------------------------------------------------- URLs

def submit_urls(p: dict) -> tuple[str, str]:
    sub = norm_sub(p.get("subreddit", ""))
    title = p.get("title", "")
    ptype = (p.get("type") or "text").lower()
    if sub.startswith("u_"):
        base_new = f"https://www.reddit.com/user/{sub[2:]}/submit/"
    else:
        base_new = f"https://www.reddit.com/r/{sub}/submit/"
    rtype = {"text": "TEXT", "image": "IMAGE", "gallery": "IMAGE", "link": "LINK"}.get(ptype, "TEXT")
    q_new = {"type": rtype, "title": title}
    if ptype == "link" and p.get("url"):
        q_new["url"] = p["url"]
    new = base_new + "?" + urllib.parse.urlencode(q_new, quote_via=urllib.parse.quote)
    q_old = {"title": title}
    if ptype == "text":
        q_old["selftext"] = "true"
        q_old["text"] = p.get("body", "")
    elif ptype == "link" and p.get("url"):
        q_old["url"] = p["url"]
    old = f"https://old.reddit.com/r/{sub}/submit?" + urllib.parse.urlencode(q_old, quote_via=urllib.parse.quote)
    if len(old) > URL_ENC_MAX:  # body too long to prefill: title only, paste the body
        q_old.pop("text", None)
        old = f"https://old.reddit.com/r/{sub}/submit?" + urllib.parse.urlencode(q_old, quote_via=urllib.parse.quote)
    return new, old


def dm_url(user: str, subject: str = "", message: str = "") -> str:
    q = {"to": user.replace("u/", "")}
    if subject:
        q["subject"] = subject
    if message and len(message) < 3000:
        q["message"] = message
    return "https://www.reddit.com/message/compose/?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)


# ---------------------------------------------------------------- HTML

CSS = """
:root{--bg:#f6f5f2;--card:#fff;--ink:#17171a;--muted:#686872;--line:#e3e2dd;--acc:#ff4500;--acc-ink:#fff;--ok:#067647;--warn:#b54708;--bad:#b42318;--chip:#f1efe9;--fresh:#12a150;--cur:#ff4500}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#101113;--card:#1a1b1e;--ink:#ececef;--muted:#9b9ba6;--line:#2c2d31;--acc:#ff5a1f;--acc-ink:#101113;--ok:#47cd89;--warn:#fdb022;--bad:#f97066;--chip:#24252a;--fresh:#3ddc84}}
:root[data-theme=dark]{--bg:#101113;--card:#1a1b1e;--ink:#ececef;--muted:#9b9ba6;--line:#2c2d31;--acc:#ff5a1f;--acc-ink:#101113;--ok:#47cd89;--warn:#fdb022;--bad:#f97066;--chip:#24252a;--fresh:#3ddc84}
*{box-sizing:border-box}html,body{background:var(--bg)}body{margin:0;color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:820px;margin:0 auto;padding:0 16px 80px}h1{font-size:20px;margin:0}h2{font-size:13px;margin:34px 0 10px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 0 10px;border-bottom:1px solid var(--line)}
.bar .top{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.prog{height:6px;background:var(--line);border-radius:3px;overflow:hidden;margin-top:8px}.prog i{display:block;height:100%;background:var(--acc);width:0}
.keys{color:var(--muted);font-size:12px;margin-top:6px}.phase{font-size:12px;font-weight:700;border-radius:999px;padding:2px 10px;background:var(--chip)}
.phase.warm{background:var(--warn);color:var(--bg)}#timer{font-weight:600;font-size:13px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:0 0 14px;scroll-margin-top:110px}
.card.done{opacity:.42}.card.cur{border-color:var(--cur);box-shadow:0 0 0 2px var(--cur)}
.meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 8px}.chip{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12px}
.chip.hot{background:var(--acc);color:var(--acc-ink);font-weight:700}.chip.fresh{background:var(--fresh);color:var(--bg);font-weight:700}
.num{font-weight:800;margin-right:2px}h3{margin:4px 0 6px;font-size:17px;line-height:1.35}
.text{white-space:pre-wrap;font-size:15px;margin:8px 0;padding:12px;border-radius:10px;border:1px dashed var(--line);outline:none}
.text:focus{border-color:var(--acc)}.ttl{font-weight:700;font-size:16px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
a.btn,button{appearance:none;border:1px solid var(--line);border-radius:10px;padding:8px 13px;font:600 13.5px system-ui;cursor:pointer;text-decoration:none;display:inline-block;background:var(--chip);color:var(--ink)}
.main{background:var(--acc)!important;color:var(--acc-ink)!important;border-color:var(--acc)!important}
.count{font-size:12px;color:var(--muted)}.warn{color:var(--warn);font-size:13px}.bad{color:var(--bad);font-size:13px;font-weight:600}.ok{color:var(--ok);font-size:13px}
.why{color:var(--muted);font-size:13.5px}.tip{background:var(--chip);border-radius:10px;padding:10px 12px;margin-top:8px;font-size:14px}
a{color:var(--acc)}ol,ul{padding-left:20px;margin:6px 0}li{margin:3px 0}label{font-size:13px;color:var(--muted);display:inline-flex;gap:6px;align-items:center;cursor:pointer}
details{margin-top:8px}summary{cursor:pointer;color:var(--muted);font-size:13px}img.media{max-width:100%;border-radius:10px;margin-top:8px;border:1px solid var(--line)}
.gap{font-size:12px;font-weight:600}.gap.wait{color:var(--warn)}.gap.ready{color:var(--ok)}kbd{font:11px ui-monospace,monospace;opacity:.7;margin-left:4px}
.opt{border-top:1px solid var(--line);margin-top:10px;padding-top:6px}
"""

JS = r"""
const D=document.body.dataset.date, GAP=(+document.body.dataset.gap||10)*60000;
const cards=[...document.querySelectorAll('.card[data-id]')];let cur=0;
const MEM={};
function store(k,v){try{if(v===undefined){const x=localStorage.getItem(k);return x===null?(MEM[k]??null):x}localStorage.setItem(k,v);MEM[k]=v}catch(e){if(v===undefined)return MEM[k]??null;MEM[k]=v}}
function copyText(t){if(navigator.clipboard&&window.isSecureContext!==false){navigator.clipboard.writeText(t).catch(()=>fb(t))}else fb(t)}
function fb(t){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove()}
function cp(id,b){copyText(document.getElementById(id).innerText);if(b){const o=b.dataset.l||b.textContent;b.dataset.l=o;b.textContent='Copied';setTimeout(()=>b.textContent=o,1200)}}
function go(id,url,b,sub){copyText(document.getElementById(id).innerText);window.open(url,'_blank','noopener');if(b){b.dataset.l=b.dataset.l||b.textContent;b.textContent='Copied + opened'}if(sub)stamp(sub)}
function openUrl(url){window.open(url,'_blank','noopener')}
function st(){try{return JSON.parse(store('rpack:'+D)||'{}')}catch(e){return {}}}
function setS(id,v){const s=st();s[id]=v;store('rpack:'+D,JSON.stringify(s));paint()}
function stamp(sub){if(!sub)return;let g={};try{g=JSON.parse(store('rpack:gap')||'{}')}catch(e){}g[sub]=Date.now();g._last=Date.now();g._sub=sub;store('rpack:gap',JSON.stringify(g));tick()}
function gapLeft(sub){let g={};try{g=JSON.parse(store('rpack:gap')||'{}')}catch(e){}const t=sub?(g[sub]||0):(g._last||0);return [t+GAP-Date.now(),g._sub]}
function fmt(ms){const m=Math.floor(ms/60000),s=Math.floor(ms%60000/1000);return m+':'+String(s).padStart(2,'0')}
function tick(){const [left,sub]=gapLeft(null);const el=document.getElementById('timer');
 if(el){if(left>0){el.textContent='next comment in r/'+sub+' in '+fmt(left);el.style.color='var(--warn)'}else{el.textContent='ready to comment';el.style.color='var(--ok)'}}
 document.querySelectorAll('.gap[data-sub]').forEach(x=>{const [l]=gapLeft(x.dataset.sub);if(l>0){x.textContent='r/'+x.dataset.sub+': wait '+fmt(l);x.className='gap wait'}else{x.textContent='r/'+x.dataset.sub+': ready';x.className='gap ready'}})}
setInterval(tick,1000);
function isDone(c){return !!st()[c.dataset.id]}
function focusCard(i){if(!cards.length)return;cur=Math.max(0,Math.min(cards.length-1,i));cards.forEach(c=>c.classList.remove('cur'));cards[cur].classList.add('cur');cards[cur].scrollIntoView({behavior:'smooth',block:'start'})}
function done(i,v){const c=cards[i];if(!c)return;if(v==='done'&&c.dataset.sub&&c.dataset.kind==='comment')stamp(c.dataset.sub);
 setS(c.dataset.id,v);const n=cards.findIndex((x,k)=>k>i&&!isDone(x));const m=n>=0?n:cards.findIndex(x=>!isDone(x));if(m>=0)focusCard(m)}
function paint(){const s=st();let d=0;cards.forEach(c=>{const v=s[c.dataset.id]||'';c.classList.toggle('done',!!v);const cb=c.querySelector('input.dn');if(cb)cb.checked=!!v;const lab=c.querySelector('.stat');if(lab)lab.textContent=v?('('+v+')'):'';if(v)d++});
 const ct=document.getElementById('count');if(ct)ct.textContent=d+'/'+cards.length+' done';const pb=document.getElementById('pbar');if(pb)pb.style.width=(cards.length?100*d/cards.length:0)+'%'}
function primary(c,n){const b=c.querySelectorAll('[data-primary]');const t=b[Math.min(n,b.length-1)];if(t)t.click()}
document.addEventListener('keydown',ev=>{if(ev.ctrlKey||ev.metaKey||ev.altKey)return;if(ev.target.isContentEditable||/SELECT|INPUT|TEXTAREA/.test(ev.target.tagName))return;
 const c=cards[cur];if(!c)return;const k=ev.key.toLowerCase();
 if(k==='enter'){primary(c,0);ev.preventDefault()}else if(/^[1-4]$/.test(k)){primary(c,+k-1)}
 else if(k==='d')done(cur,'done');else if(k==='s')done(cur,'skipped');else if(k==='j')focusCard(cur+1);else if(k==='k')focusCard(cur-1)});
cards.forEach((c,i)=>c.addEventListener('click',()=>{if(cur===i)return;cur=i;cards.forEach(x=>x.classList.remove('cur'));c.classList.add('cur')}));
document.querySelectorAll('input.dn').forEach(cb=>cb.addEventListener('change',()=>{const c=cb.closest('.card');setS(c.dataset.id,cb.checked?'done':'')}));
const RK='rpack:check:'+D;function rs(){try{return JSON.parse(store(RK)||'{}')}catch(e){return {}}}
document.querySelectorAll('input.ck').forEach(b=>{b.checked=!!rs()[b.dataset.t];b.onchange=()=>{const s=rs();s[b.dataset.t]=b.checked;store(RK,JSON.stringify(s))}});
function theme(){const r=document.documentElement;const t=r.dataset.theme==='dark'?'light':(r.dataset.theme==='light'?'':'dark');if(t)r.dataset.theme=t;else delete r.dataset.theme;store('rpack:theme',t||'')}
(function(){const t=store('rpack:theme');if(t)document.documentElement.dataset.theme=t})();
paint();tick();const f=cards.findIndex(c=>!isDone(c));if(cards.length){cur=f>=0?f:0;cards[cur].classList.add('cur')}
"""


class Page:
    def __init__(self):
        self.uid = 0
        self.blockers = 0
        self.warnings = 0

    def tid(self) -> str:
        self.uid += 1
        return f"t{self.uid}"

    def block(self, text: str, cls: str = "") -> tuple[str, str]:
        tid = self.tid()
        return tid, f'<div class="text {cls}" id="{tid}" contenteditable spellcheck="false">{html.escape(text)}</div>'

    def problems(self, blockers: list[str], warns: list[str]) -> str:
        self.blockers += len(blockers)
        self.warnings += len(warns)
        if not blockers and not warns:
            return '<div class="ok">Passes checks</div>'
        out = [f'<div class="bad">BLOCKER: {html.escape(b)}</div>' for b in blockers]
        out += [f'<div class="warn">Warning: {html.escape(w)}</div>' for w in warns]
        return "".join(out)


def e(s) -> str:
    return html.escape(str(s if s is not None else ""))


def done_box() -> str:
    return '<label><input type="checkbox" class="dn"> Done <span class="stat"></span></label>'


def render_rising(pg: Page, r: dict, i: int, warmup: bool, seen: dict) -> str:
    sub = norm_sub(r.get("subreddit", ""))
    url = r.get("url", "#")
    chips = [f'<span class="num">{i}</span>', f'<span class="chip hot">r/{e(sub)}</span>']
    for k in ("posted_ago", "kind"):
        if r.get(k):
            chips.append(f'<span class="chip">{e(r[k])}</span>')
    if r.get("score_seen") is not None or r.get("comments_seen") is not None:
        chips.append(f'<span class="chip">{e(r.get("score_seen", "?"))} pts · {e(r.get("comments_seen", "?"))} comments when seen</span>')
    if r.get("bridge"):
        chips.append('<span class="chip fresh">viral bridge</span>')
    out = [f'<div class="card" data-id="c{i}" data-sub="{e(sub)}" data-kind="comment">'
           f'<div class="meta">{"".join(chips)}<span class="gap" data-sub="{e(sub)}"></span></div>'
           f'<h3><a href="{e(url)}" target="_blank" rel="noopener">{e(r.get("title", "thread"))}</a></h3>']
    if r.get("why"):
        out.append(f'<div class="why">Why: {e(r["why"])}</div>')
    tid_ = thread_id(url)
    pre_warn = []
    if tid_ and tid_ in seen:
        pre_warn.append(f"already handled: {seen[tid_]}. Comment once per thread, max")
    for j, opt in enumerate(r.get("options", []), 1):
        tid, blk = pg.block(opt)
        b, w = check_text(opt, sub=sub, warmup=warmup, kind="comment")
        if j == 1:
            w = pre_warn + w
        words = word_count(opt)
        out.append(f'<div class="opt"><div class="why">Option {j} · {words} words</div>{blk}{pg.problems(b, w)}'
                   f'<div class="row"><button class="{"main" if j == 1 else ""}" data-primary '
                   f'onclick="go(\'{tid}\',\'{e(url)}\',this,\'{e(sub)}\')">Copy comment {j} + open thread<kbd>{j if j > 1 else "Enter"}</kbd></button>'
                   f'<button onclick="cp(\'{tid}\',this)">Copy</button></div></div>')
    if r.get("follow_up"):
        out.append(f'<div class="tip">If someone replies: {e(r["follow_up"])}</div>')
    out.append(f'<div class="row">{done_box()}</div></div>')
    return "".join(out)


def render_post(pg: Page, p: dict, i: int, warmup: bool) -> str:
    sub = norm_sub(p.get("subreddit", ""))
    chips = [f'<span class="num">{e(p.get("id", i))}</span>', f'<span class="chip hot">r/{e(sub)}</span>']
    for k in ("slot", "type", "pillar", "format", "hook_type", "bucket"):
        if p.get(k):
            chips.append(f'<span class="chip">{e(p[k])}</span>')
    if p.get("flair"):
        chips.append(f'<span class="chip">flair: {e(p["flair"])}</span>')
    if p.get("score") is not None:
        chips.append(f'<span class="chip">score {e(p["score"])}</span>')
    if p.get("promo"):
        chips.append('<span class="chip hot">PROMO</span>')
    new_url, old_url = submit_urls(p)
    out = [f'<div class="card" data-id="p{e(p.get("id", i))}" data-sub="{e(sub)}" data-kind="post"><div class="meta">{"".join(chips)}</div>']
    if p.get("hypothesis"):
        out.append(f'<div class="why">Testing: {e(p["hypothesis"])}</div>')
    intel = INTEL.get(sub)
    if intel and intel.get("notes"):
        out.append(f'<div class="why">r/{e(sub)} notes: {e(intel["notes"])}</div>')
    if intel and intel.get("gate") not in (None, "", "?", "-"):
        out.append(f'<div class="why">r/{e(sub)} gate: {e(intel["gate"])}. Check it before posting.</div>')
    t_id, t_blk = pg.block(p.get("title", ""), "ttl")
    b_id, b_blk = pg.block(p.get("body", ""))
    blockers, warns = check_post(p, warmup)
    out.append(f'<div class="why">Title · {len(p.get("title", ""))}/{TITLE_MAX}</div>{t_blk}')
    if p.get("body"):
        out.append(f'<div class="why">Body · {word_count(p["body"])} words</div>{b_blk}')
    out.append(pg.problems(blockers, warns))
    out.append(f'<div class="row"><button class="main" data-primary onclick="cp(\'{t_id}\',this);openUrl(\'{e(new_url)}\')">'
               f'Copy title + open submit page<kbd>Enter</kbd></button>'
               f'<button onclick="cp(\'{t_id}\',this)">Copy title</button>')
    if p.get("body"):
        out.append(f'<button onclick="cp(\'{b_id}\',this)">Copy body</button>')
    out.append(f'<a class="btn" href="{e(old_url)}" target="_blank" rel="noopener">old.reddit (prefilled)</a>{done_box()}</div>')
    flair_txt = f"Pick flair <b>{e(p['flair'])}</b>. " if p.get("flair") else ""
    out.append(f'<div class="tip">{flair_txt}On the submit page: check the sub is right, paste the title (and body), '
               f'attach media if listed, pick flair, then Post. Stay for the golden hour.</div>')
    media = p.get("media")
    if media:
        out.append(f'<div class="why">Media: {e(media)}</div>')
        for m in re.findall(r"(media/[^\s,;)]+\.(?:png|jpe?g|gif|webp))", media, re.I):
            out.append(f'<a href="../{e(m)}" target="_blank"><img class="media" src="../{e(m)}" alt=""></a>')
    if p.get("alt_text"):
        out.append('<details><summary>Image description (Reddit asks for it on upload)</summary>')
        tid, blk = pg.block(p["alt_text"])
        out.append(blk + f'<div class="row"><button onclick="cp(\'{tid}\',this)">Copy</button></div></details>')
    if p.get("first_comment"):
        tid, blk = pg.block(p["first_comment"])
        out.append('<details open><summary>First comment: post it yourself right after the post goes up</summary>'
                   f'{blk}<div class="row"><button onclick="cp(\'{tid}\',this)">Copy first comment</button></div></details>')
    if p.get("golden_hour_replies"):
        out.append('<details><summary>Golden hour: ready replies for the comments you will likely get</summary><ul>')
        out.extend(f"<li>{e(g)}</li>" for g in p["golden_hour_replies"])
        out.append("</ul></details>")
    if p.get("alt_titles"):
        out.append('<details><summary>Alternative titles</summary><ul>')
        out.extend(f"<li>{e(h)}</li>" for h in p["alt_titles"])
        out.append("</ul></details>")
    cross = p.get("crosspost")
    if cross:
        to = ", ".join(f"r/{norm_sub(s)}" for s in cross.get("to", []))
        out.append(f'<div class="tip">Crosspost plan: {e(to)} {e(cross.get("when", ""))}. One at a time, never the same day as the original if it is still rising.</div>')
    out.append("</div>")
    return "".join(out)


def render_inbox(pg: Page, m: dict, i: int, warmup: bool) -> str:
    sub = norm_sub(m.get("subreddit", ""))
    url = m.get("url", "#")
    out = [f'<div class="card" data-id="i{i}" data-sub="{e(sub)}" data-kind="comment"><div class="meta">'
           f'<span class="num">{i}</span><span class="chip hot">{e(m.get("interest", "reply"))}</span>'
           f'<span class="chip">u/{e(m.get("from", "?"))}</span><span class="chip">{e(m.get("kind", "comment reply"))}</span>'
           + (f'<span class="gap" data-sub="{e(sub)}"></span>' if sub else "") + '</div>']
    if m.get("their_text"):
        out.append(f'<div class="why">They said: “{e(m["their_text"][:400])}”</div>')
    if m.get("why"):
        out.append(f'<div class="why">Why: {e(m["why"])}</div>')
    tid, blk = pg.block(m.get("reply", ""))
    # someone asking what we do may be answered even in warm-up; product rules of the sub still apply
    asked = bool(m.get("asked_about_us"))
    b, w = check_text(m.get("reply", ""), sub=sub, warmup=warmup and not asked, kind="reply")
    out.append(blk + pg.problems(b, w))
    out.append(f'<div class="row"><button class="main" data-primary onclick="go(\'{tid}\',\'{e(url)}\',this,\'{e(sub)}\')">'
               f'Copy reply + open<kbd>Enter</kbd></button><button onclick="cp(\'{tid}\',this)">Copy</button>{done_box()}</div></div>')
    return "".join(out)


def render_dm(pg: Page, d: dict, i: int) -> str:
    user = d.get("to", "")
    out = [f'<div class="card" data-id="m{i}" data-kind="dm"><div class="meta"><span class="num">{i}</span>'
           f'<span class="chip hot">DM u/{e(user.replace("u/", ""))}</span>'
           + (f'<span class="chip">{e(d["stage"])}</span>' if d.get("stage") else "") + "</div>"]
    if d.get("context"):
        out.append(f'<div class="why">Context: {e(d["context"])}</div>')
    tid, blk = pg.block(d.get("text", ""))
    b, w = check_text(d.get("text", ""), kind="dm")
    out.append(blk + pg.problems(b, w))
    out.append(f'<div class="row"><button class="main" data-primary onclick="go(\'{tid}\',\'{e(dm_url(user, d.get("subject", "")))}\',this)">'
               f'Copy DM + open message page<kbd>Enter</kbd></button><button onclick="cp(\'{tid}\',this)">Copy</button>{done_box()}</div>')
    if d.get("follow_up"):
        out.append(f'<div class="tip">Follow-up: {e(d["follow_up"])}</div>')
    out.append("</div>")
    return "".join(out)


def promo_share(pack: dict) -> tuple[int, int]:
    total = promo = 0
    for p in pack.get("posts", []):
        total += 1
        promo += bool(p.get("promo") or is_promo(p.get("title", "") + " " + p.get("body", "")))
    for r in pack.get("rising", []):
        total += 1
        promo += any(is_promo(o) for o in r.get("options", []))
    for m in pack.get("inbox", []):
        total += 1
        promo += is_promo(m.get("reply", ""))
    return promo, total


def render_pack(pack: dict) -> tuple[str, Page]:
    pg = Page()
    d = pack.get("date", "")
    warmup = warmup_active(d, pack.get("phase"))
    seen = load_seen_threads()
    brief = pack.get("brief", {})
    gap = int(CFG.get("comment_gap_minutes", 10))
    promo, total = promo_share(pack)
    share = promo / total if total else 0
    sample = pack.get("sample_label")
    parts = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>Reddit Pack {e(d)}</title><style>{CSS}</style></head>'
             f'<body data-date="{e(d)}" data-gap="{gap}"><main><div class="bar"><div class="top">'
             f'<h1>FreshLeads · Reddit Pack · {e(d)}</h1>'
             f'<span class="phase {"warm" if warmup else ""}">{"WARM-UP: no product, no links" if warmup else "growth phase: 90/10 promo"}</span>'
             f'<span class="count" id="count"></span><span id="timer"></span><button onclick="theme()">Theme</button></div>'
             f'<div class="prog"><i id="pbar"></i></div>'
             f'<div class="keys">Enter = main action of the selected card (1-4 = comment option N) · D = done · S = skip · J/K = next/previous · click text to edit before copying. '
             f'You post every word yourself. New account: about 1 comment per {gap} min per sub, the timer tracks it.</div></div>']
    if sample:
        parts.append(f'<div class="tip"><b>{e(sample)}</b></div>')
    parts.append('<h2>Brief</h2><div class="card">')
    if brief.get("summary"):
        parts.append(f"<p>{e(brief['summary'])}</p>")
    if brief.get("karma"):
        k = brief["karma"]
        parts.append(f'<p class="why">Karma now: {e(k.get("now", "?"))} · goal this week: {e(k.get("goal", "?"))} · followers: {e(k.get("followers", "?"))}</p>')
    trends = brief.get("trends", [])
    if trends:
        parts.append("<ul>")
        for t in trends:
            src = f' <a href="{e(t["source"])}" target="_blank" rel="noopener">source</a>' if t.get("source") else ""
            parts.append(f"<li><b>{e(t.get('name', ''))}</b>: {e(t.get('angle', ''))}<span class='why'> ({e(t.get('why', ''))})</span>{src}</li>")
        parts.append("</ul>")
    parts.append(f'<p class="why">Promo share in this pack: {promo}/{total} items ({share:.0%}). Limit {PROMO_MAX_SHARE:.0%}{" (0 during warm-up)" if warmup else ""}.</p>')
    if warmup and promo:
        parts.append('<div class="bad">BLOCKER: product mentions in a warm-up pack. Remove them.</div>')
        pg.blockers += 1
    elif share > PROMO_MAX_SHARE:
        parts.append('<div class="warn">Warning: promo share above 10%. Cut promo or add pure-help items.</div>')
        pg.warnings += 1
    if brief.get("golden_hour"):
        parts.append(f"<p class='why'>{e(brief['golden_hour'])}</p>")
    parts.append("</div>")
    if brief.get("checklist"):
        parts.append('<h2>Today, in order</h2><div class="card">')
        parts.extend(f'<label style="display:flex;margin:6px 0"><input type="checkbox" class="ck" data-t="{n}"> {e(c)}</label>'
                     for n, c in enumerate(brief["checklist"]))
        parts.append("</div>")
    if pack.get("rising"):
        parts.append("<h2>Rising threads first: comment early, aim for top comment</h2>")
        parts.extend(render_rising(pg, r, n, warmup, seen) for n, r in enumerate(pack["rising"], 1))
    if pack.get("posts"):
        parts.append("<h2>Posts</h2>")
        parts.extend(render_post(pg, p, n, warmup) for n, p in enumerate(pack["posts"], 1))
    if pack.get("inbox"):
        parts.append("<h2>Inbox and golden-hour replies</h2>")
        parts.extend(render_inbox(pg, m, n, warmup) for n, m in enumerate(pack["inbox"], 1))
    if pack.get("dms"):
        parts.append("<h2>DM follow-ups (only people who asked or engaged)</h2>")
        parts.extend(render_dm(pg, dm, n) for n, dm in enumerate(pack["dms"], 1))
    if pack.get("profile_tasks"):
        parts.append('<h2>Profile and housekeeping</h2><div class="card"><ul>')
        parts.extend(f"<li>{e(t)}</li>" for t in pack["profile_tasks"])
        parts.append("</ul></div>")
    parts.append(f"<script>{JS}</script></main></body></html>")
    return "".join(parts), pg


# ---------------------------------------------------------------- Telegram

def telegram_messages(pack: dict, out: Path) -> list[str]:
    msgs = [f"<b>FreshLeads Reddit Pack · {html.escape(pack.get('date', ''))}</b>"]
    brief = pack.get("brief", {})
    if brief.get("summary"):
        msgs[0] += "\n" + html.escape(brief["summary"])
    msgs[0] += f"\n\nFull pack: {html.escape(str(out))}"
    for r in pack.get("rising", []):
        opt = (r.get("options") or [""])[0]
        msgs.append(f"<b>Comment</b> r/{html.escape(norm_sub(r.get('subreddit', '')))} · "
                    f"<a href=\"{html.escape(r.get('url', ''))}\">thread</a>\n\n{html.escape(opt)}")
    for p in pack.get("posts", []):
        new_url, _ = submit_urls(p)
        msgs.append(f"<b>{html.escape(p.get('slot', p.get('id', '')))}</b> r/{html.escape(norm_sub(p.get('subreddit', '')))}\n\n"
                    f"<b>{html.escape(p.get('title', ''))}</b>\n\n<a href=\"{html.escape(new_url)}\">Open submit page</a>")
    return [m[:4000] for m in msgs]


def send_telegram(messages: list[str]) -> None:
    token, chat = CFG.get("telegram_bot_token"), CFG.get("telegram_chat_id")
    if not token or not chat or "PASTE" in str(token):
        print("Telegram not configured (config.json). Skipping send.", file=sys.stderr)
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for m in messages:
        data = urllib.parse.urlencode({"chat_id": chat, "text": m, "parse_mode": "HTML",
                                       "disable_web_page_preview": "true"}).encode()
        try:
            with urllib.request.urlopen(url, data=data, timeout=20) as resp:
                resp.read()
        except Exception as exc:  # network may be blocked inside a sandbox
            print(f"Telegram send failed ({exc}). Skipping the rest; the HTML pack is ready.", file=sys.stderr)
            return
    print(f"Sent {len(messages)} Telegram message(s).")


# ---------------------------------------------------------------- CLI

def lint_pack(pack: dict) -> list[str]:
    """Plain-text list of problems, for the terminal."""
    warmup = warmup_active(pack.get("date", ""), pack.get("phase"))
    seen = load_seen_threads()
    lines = []
    for p in pack.get("posts", []):
        b, w = check_post(p, warmup)
        lines += [f"[{p.get('id')}] BLOCKER {x}" for x in b] + [f"[{p.get('id')}] {x}" for x in w]
    for n, r in enumerate(pack.get("rising", []), 1):
        tid_ = thread_id(r.get("url", ""))
        if tid_ in seen:
            lines.append(f"[C{n}] already handled: {seen[tid_]}")
        for j, o in enumerate(r.get("options", []), 1):
            b, w = check_text(o, sub=r.get("subreddit", ""), warmup=warmup)
            lines += [f"[C{n}.{j}] BLOCKER {x}" for x in b] + [f"[C{n}.{j}] {x}" for x in w]
    for n, m in enumerate(pack.get("inbox", []), 1):
        b, w = check_text(m.get("reply", ""), sub=m.get("subreddit", ""), warmup=warmup and not m.get("asked_about_us"), kind="reply")
        lines += [f"[I{n}] BLOCKER {x}" for x in b] + [f"[I{n}] {x}" for x in w]
    for n, d in enumerate(pack.get("dms", []), 1):
        b, w = check_text(d.get("text", ""), kind="dm")
        lines += [f"[M{n}] BLOCKER {x}" for x in b] + [f"[M{n}] {x}" for x in w]
    promo, total = promo_share(pack)
    if warmup and promo:
        lines.append(f"[pack] BLOCKER {promo} promo item(s) in a warm-up pack")
    elif total and promo / total > PROMO_MAX_SHARE:
        lines.append(f"[pack] promo share {promo}/{total} is above 10%")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack", nargs="?", help="path to pack JSON")
    ap.add_argument("--no-send", action="store_true", help="build the HTML only, skip Telegram")
    ap.add_argument("--check", metavar="TEXT", help="check one comment/body (or title with --title)")
    ap.add_argument("--title", action="store_true", help="with --check: treat TEXT as a post title")
    ap.add_argument("--sub", default="", help="with --check: apply this subreddit's rules from memory/subreddit-intel.md")
    ap.add_argument("--warmup", action="store_true", help="with --check: apply warm-up rules (default: by today's date)")
    args = ap.parse_args()

    if args.check is not None:
        warm = args.warmup or warmup_active(date.today().isoformat(), None)
        if args.title:
            b, w = check_title(args.check, args.sub, warm)
            print(f"{len(args.check)}/{TITLE_MAX} chars")
        else:
            b, w = check_text(args.check, sub=args.sub, warmup=warm)
            print(f"{word_count(args.check)} words")
        print("\n".join([f"- BLOCKER {x}" for x in b] + [f"- {x}" for x in w]) or "OK")
        return 1 if (b or w) else 0
    if not args.pack:
        ap.error("pack path required")

    pack_path = Path(args.pack).resolve()
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    for line in lint_pack(pack):
        print(line, file=sys.stderr)
    page, pg = render_pack(pack)
    out = pack_path.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out}  ({pg.blockers} blocker(s), {pg.warnings} warning(s))")
    if not args.no_send:
        send_telegram(telegram_messages(pack, out))
    if pg.blockers:
        print("Fix every BLOCKER before Ishaan posts anything.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
