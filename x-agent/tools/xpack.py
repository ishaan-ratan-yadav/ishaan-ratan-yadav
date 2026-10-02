#!/usr/bin/env python3
"""Build the Daily Pack for the Evolves Studio X agent.

Reads a pack JSON (written by the agent), validates every post against X's
free-account rules, and produces:
  * packs/<date>.html  - one-click launcher page (open in Chrome)
  * Telegram messages  - sent via the Bot API if config.json has a token,
                         otherwise printed as browser-openable send URLs

Nothing is ever posted to X. Every "Open in X" button is an intent link:
X opens the compose box pre-filled, and the human clicks Post.

Usage:
  python tools/xpack.py packs/2026-10-03.json            # build + send Telegram
  python tools/xpack.py packs/2026-10-03.json --no-send  # build only
  python tools/xpack.py --check "some post text"         # length/rule check
"""

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_CHARS = 280  # no X Premium -> hard 280 weighted-character limit
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")
INTENT = "https://x.com/intent/tweet"

# twitter-text v3: these code point ranges weigh 1, everything else (CJK, emoji, ...) weighs 2
_LIGHT_RANGES = ((0, 4351), (8192, 8205), (8208, 8223), (8242, 8247))


def weighted_length(text: str) -> int:
    """Approximate X's weighted character count (URLs always count 23)."""
    length = 0
    for url in URL_RE.findall(text):
        length += 23
        text = text.replace(url, "", 1)
    for ch in text:
        cp = ord(ch)
        length += 1 if any(lo <= cp <= hi for lo, hi in _LIGHT_RANGES) else 2
    return length


def check_post(text: str, *, main_post: bool = True) -> list[str]:
    """Return a list of rule problems for one post (empty list = OK)."""
    problems = []
    n = weighted_length(text)
    if n > MAX_CHARS:
        problems.append(f"too long: {n}/{MAX_CHARS} weighted chars")
    if main_post and URL_RE.search(text):
        problems.append("link in main post (put links in a self-reply instead)")
    tags = HASHTAG_RE.findall(text)
    if len(tags) > 1:
        problems.append(f"{len(tags)} hashtags (max 1)")
    first_line = text.strip().split("\n", 1)[0]
    if len(first_line) > 100:
        problems.append("hook (first line) longer than 100 chars")
    for tell in ("delve", "game-changer", "in today's fast-paced", "unleash", "elevate your", "—"):
        if tell.lower() in text.lower():
            label = "em dash" if tell == "—" else f"'{tell}'"
            problems.append(f"AI-sounding: {label}")
    return problems


def intent_url(text: str, in_reply_to: str | None = None) -> str:
    params = {"text": text}
    if in_reply_to:
        params["in_reply_to"] = in_reply_to
    return INTENT + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def status_id(url: str) -> str | None:
    m = re.search(r"/status/(\d+)", url or "")
    return m.group(1) if m else None


# ---------------------------------------------------------------- HTML page

CSS = """
:root{--bg:#f6f6f4;--card:#fff;--ink:#16161a;--muted:#6b6b76;--line:#e4e4e0;--accent:#5b4bff;--accent-ink:#fff;--warn:#b42318;--ok:#067647;--chip:#efeefe}
@media (prefers-color-scheme:dark){:root{--bg:#0f0f12;--card:#18181d;--ink:#ececf1;--muted:#9a9aa6;--line:#2a2a31;--accent:#8b7dff;--accent-ink:#0f0f12;--warn:#f97066;--ok:#47cd89;--chip:#24223a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:760px;margin:0 auto;padding:24px 16px 64px}h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;margin:32px 0 12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.sub{color:var(--muted);margin:0 0 16px}.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:0 0 14px}
.card.done{opacity:.45}.meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}.chip{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:12px}
.text{white-space:pre-wrap;font-size:16px;margin:8px 0;padding:12px;border-radius:10px;border:1px dashed var(--line)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
a.btn,button{appearance:none;border:0;border-radius:10px;padding:9px 14px;font:600 14px system-ui;cursor:pointer;text-decoration:none;display:inline-block}
a.btn{background:var(--accent);color:var(--accent-ink)}button{background:var(--chip);color:var(--ink)}
.count{font-size:12px;color:var(--muted)}.warn{color:var(--warn);font-size:13px}.ok{color:var(--ok);font-size:13px}
.why{color:var(--muted);font-size:13px}label{font-size:13px;color:var(--muted);display:flex;gap:6px;align-items:center}
ul{padding-left:18px;margin:6px 0}details{margin-top:8px}summary{cursor:pointer;color:var(--muted);font-size:13px}
img.media{max-width:100%;border-radius:10px;margin-top:8px}
"""

JS = """
function cp(id,btn){navigator.clipboard.writeText(document.getElementById(id).innerText).then(()=>{btn.textContent='Copied';setTimeout(()=>btn.textContent='Copy',1200)})}
function key(id){return 'xpack:'+document.body.dataset.date+':'+id}
function mark(cb){try{localStorage.setItem(key(cb.dataset.id),cb.checked?'1':'')}catch(e){}cb.closest('.card').classList.toggle('done',cb.checked)}
document.querySelectorAll('input[data-id]').forEach(cb=>{try{if(localStorage.getItem(key(cb.dataset.id))){cb.checked=true;cb.closest('.card').classList.add('done')}}catch(e){}})
"""

_uid = 0


def _textblock(text: str, label: str = "Copy") -> str:
    global _uid
    _uid += 1
    tid = f"t{_uid}"
    return (f'<div class="text" id="{tid}">{html.escape(text)}</div>'
            f'<div class="row"><button onclick="cp(\'{tid}\',this)">{label}</button>'
            f'<span class="count">{weighted_length(text)}/{MAX_CHARS}</span></div>')


def _problems_html(problems: list[str]) -> str:
    if not problems:
        return '<div class="ok">Passes checks</div>'
    return "".join(f'<div class="warn">⚠ {html.escape(p)}</div>' for p in problems)


def _done_box(item_id: str) -> str:
    return f'<label><input type="checkbox" data-id="{item_id}" onchange="mark(this)"> Posted</label>'


def render_post(p: dict) -> str:
    chips = [p.get("slot"), p.get("pillar"), p.get("format"), p.get("hook_type")]
    score = p.get("score")
    if score is not None:
        chips.append(f"score {score}")
    meta = "".join(f'<span class="chip">{html.escape(str(c))}</span>' for c in chips if c)
    out = [f'<div class="card"><div class="meta">{meta}</div>']
    if p.get("hypothesis"):
        out.append(f'<div class="why">Testing: {html.escape(p["hypothesis"])}</div>')
    thread = p.get("thread") or []
    out.append(_textblock(p["text"]))
    out.append(_problems_html(check_post(p["text"])))
    out.append(f'<div class="row"><a class="btn" href="{html.escape(intent_url(p["text"]))}" '
               f'target="_blank" rel="noopener">Open in X</a>{_done_box(p["id"])}</div>')
    if thread:
        out.append('<details open><summary>Thread: after posting, reply to your own post with each part, in order</summary>')
        for i, part in enumerate(thread, 2):
            out.append(f'<div class="why">Part {i}</div>{_textblock(part)}')
            out.append(_problems_html(check_post(part, main_post=False)))
        out.append("</details>")
    if p.get("self_reply_link"):
        out.append('<details open><summary>Self-reply with the link (post it right after the main post)</summary>')
        out.append(_textblock(p["self_reply_link"]) + "</details>")
    media = p.get("media")
    if media:
        if re.search(r"\.(png|jpe?g|gif|webp)$", media, re.I):
            out.append(f'<div class="why">Attach this media before posting:</div>'
                       f'<img class="media" src="{html.escape(media)}" alt="">'
                       f'<div class="why">{html.escape(media)}</div>')
        else:
            out.append(f'<div class="why">Media: {html.escape(media)}</div>')
    if p.get("alt_hooks"):
        out.append('<details><summary>Alternative hooks</summary><ul>')
        out.extend(f"<li>{html.escape(h)}</li>" for h in p["alt_hooks"])
        out.append("</ul></details>")
    out.append("</div>")
    return "".join(out)


def render_reply(r: dict, idx: int) -> str:
    tid = status_id(r.get("target_url", ""))
    out = [f'<div class="card"><div class="meta"><span class="chip">{html.escape(r.get("author", ""))}</span>']
    if r.get("posted_ago"):
        out.append(f'<span class="chip">{html.escape(r["posted_ago"])}</span>')
    out.append("</div>")
    if r.get("target_text"):
        out.append(f'<div class="why">“{html.escape(r["target_text"][:220])}”</div>')
    if r.get("why"):
        out.append(f'<div class="why">Why: {html.escape(r["why"])}</div>')
    out.append(f'<div class="row"><a href="{html.escape(r.get("target_url", "#"))}" target="_blank" rel="noopener">View original post</a></div>')
    for j, opt in enumerate(r.get("options", []), 1):
        out.append(_textblock(opt))
        out.append(_problems_html(check_post(opt, main_post=False)))
        if tid:
            out.append(f'<div class="row"><a class="btn" href="{html.escape(intent_url(opt, tid))}" '
                       f'target="_blank" rel="noopener">Reply with option {j}</a></div>')
    out.append(f'<div class="row">{_done_box(f"r{idx}")}</div></div>')
    return "".join(out)


def render_quote(q: dict, idx: int) -> str:
    text = q["text"].rstrip() + "\n" + q["target_url"]
    out = [f'<div class="card"><div class="meta"><span class="chip">quote</span>'
           f'<span class="chip">{html.escape(q.get("author", ""))}</span></div>']
    if q.get("why"):
        out.append(f'<div class="why">Why: {html.escape(q["why"])}</div>')
    out.append(_textblock(q["text"]))
    out.append(_problems_html(check_post(text, main_post=False)))
    out.append(f'<div class="row"><a class="btn" href="{html.escape(intent_url(text))}" target="_blank" '
               f'rel="noopener">Open quote in X</a>{_done_box(f"q{idx}")}</div></div>')
    return "".join(out)


def render_pack(pack: dict) -> str:
    date = pack["date"]
    brief = pack.get("brief", {})
    parts = [f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
             f'<meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>X Pack {html.escape(date)}</title><style>{CSS}</style></head>'
             f'<body data-date="{html.escape(date)}"><main>'
             f'<h1>Evolves Studio · X Pack · {html.escape(date)}</h1>'
             f'<p class="sub">Click “Open in X”, check the text, then press Post yourself. Tick “Posted” when done.</p>']
    if brief:
        parts.append('<h2>Today’s brief</h2><div class="card">')
        if brief.get("summary"):
            parts.append(f"<p>{html.escape(brief['summary'])}</p>")
        trends = brief.get("trends", [])
        if trends:
            parts.append("<ul>")
            for t in trends:
                parts.append(f"<li><b>{html.escape(t.get('name', ''))}</b>: {html.escape(t.get('angle', ''))}"
                             f"<span class='why'> ({html.escape(t.get('why', ''))})</span></li>")
            parts.append("</ul>")
        if brief.get("golden_hour"):
            parts.append(f"<p class='why'>{html.escape(brief['golden_hour'])}</p>")
        parts.append("</div>")
    if pack.get("render_requests"):
        parts.append("<h2>Render requests (make these, then post)</h2>")
        for rr in pack["render_requests"]:
            parts.append(f'<div class="card"><div class="meta"><span class="chip">{html.escape(rr.get("deadline", ""))}</span>'
                         f'<span class="chip">{html.escape(rr.get("length", ""))}</span></div>'
                         f'<p><b>{html.escape(rr.get("title", ""))}</b></p>'
                         f'<p>{html.escape(rr.get("shot", ""))}</p>'
                         f'<div class="why">Why: {html.escape(rr.get("why", ""))}</div></div>')
    if pack.get("posts"):
        parts.append("<h2>Posts</h2>")
        parts.extend(render_post(p) for p in pack["posts"])
    if pack.get("quotes"):
        parts.append("<h2>Quote posts</h2>")
        parts.extend(render_quote(q, i) for i, q in enumerate(pack["quotes"]))
    if pack.get("replies"):
        parts.append("<h2>Replies (post these fast, early replies get seen)</h2>")
        parts.extend(render_reply(r, i) for i, r in enumerate(pack["replies"]))
    parts.append(f"<script>{JS}</script></main></body></html>")
    return "".join(parts)


# ---------------------------------------------------------------- Telegram

def load_config() -> dict:
    cfg = ROOT / "config.json"
    return json.loads(cfg.read_text()) if cfg.exists() else {}


def telegram_messages(pack: dict, pack_path: Path) -> list[str]:
    msgs = []
    head = [f"<b>Evolves X Pack · {html.escape(pack['date'])}</b>"]
    brief = pack.get("brief", {})
    if brief.get("summary"):
        head.append(html.escape(brief["summary"]))
    for t in brief.get("trends", [])[:5]:
        head.append(f"• <b>{html.escape(t.get('name', ''))}</b>: {html.escape(t.get('angle', ''))}")
    for rr in pack.get("render_requests", []):
        head.append(f"🎬 Render: <b>{html.escape(rr.get('title', ''))}</b> by {html.escape(rr.get('deadline', ''))}")
    head.append(f"\nFull pack: {html.escape(str(pack_path))}")
    msgs.append("\n".join(head))
    for p in pack.get("posts", []):
        msgs.append(f"<b>{html.escape(p.get('slot', p['id']))}</b> · {html.escape(p.get('format', ''))}\n\n"
                    f"{html.escape(p['text'])}\n\n<a href=\"{html.escape(intent_url(p['text']))}\">▶ Open in X</a>")
    for q in pack.get("quotes", []):
        text = q["text"].rstrip() + "\n" + q["target_url"]
        msgs.append(f"<b>Quote</b> {html.escape(q.get('author', ''))}\n\n{html.escape(q['text'])}\n\n"
                    f"<a href=\"{html.escape(intent_url(text))}\">▶ Open quote in X</a>")
    for r in pack.get("replies", []):
        tid = status_id(r.get("target_url", ""))
        lines = [f"<b>Reply</b> {html.escape(r.get('author', ''))} · <a href=\"{html.escape(r.get('target_url', ''))}\">post</a>"]
        for j, opt in enumerate(r.get("options", []), 1):
            link = f" <a href=\"{html.escape(intent_url(opt, tid))}\">▶ reply {j}</a>" if tid else ""
            lines.append(f"{j}. {html.escape(opt)}{link}")
        msgs.append("\n".join(lines))
    return [m[:4000] for m in msgs]


def send_telegram(messages: list[str], cfg: dict) -> None:
    token, chat = cfg.get("telegram_bot_token"), cfg.get("telegram_chat_id")
    if not token or not chat:
        print("Telegram not configured (config.json). Skipping send.", file=sys.stderr)
        return
    for m in messages:
        data = urllib.parse.urlencode({"chat_id": chat, "text": m, "parse_mode": "HTML",
                                       "disable_web_page_preview": "true"}).encode()
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            with urllib.request.urlopen(url, data=data, timeout=20) as resp:
                resp.read()
        except Exception as exc:  # network may be blocked inside a sandbox
            print(f"Telegram send failed ({exc}). Open these URLs in Chrome instead:", file=sys.stderr)
            for mm in messages:
                q = urllib.parse.urlencode({"chat_id": chat, "text": mm, "parse_mode": "HTML",
                                            "disable_web_page_preview": "true"})
                print(f"{url}?{q}")
            return
    print(f"Sent {len(messages)} Telegram message(s).")


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack", nargs="?", help="path to pack JSON")
    ap.add_argument("--no-send", action="store_true", help="build the HTML only, skip Telegram")
    ap.add_argument("--check", metavar="TEXT", help="check one post's length and rules")
    args = ap.parse_args()

    if args.check is not None:
        probs = check_post(args.check)
        print(f"{weighted_length(args.check)}/{MAX_CHARS} weighted chars")
        print("\n".join(f"- {p}" for p in probs) or "OK")
        return 1 if probs else 0
    if not args.pack:
        ap.error("pack path required")

    pack_path = Path(args.pack).resolve()
    pack = json.loads(pack_path.read_text())
    bad = 0
    for p in pack.get("posts", []):
        for prob in check_post(p["text"]):
            bad += 1
            print(f"[{p['id']}] {prob}", file=sys.stderr)
    out = pack_path.with_suffix(".html")
    out.write_text(render_pack(pack))
    print(f"Wrote {out}")
    if not args.no_send:
        send_telegram(telegram_messages(pack, out), load_config())
    if bad:
        print(f"{bad} rule problem(s) in main posts: fix before posting.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
