"""Builds infographics (PNG, 1080x1350) + output/content_kit.html from posts.json."""
import html
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
ROOT = HERE.parent
IMG = ROOT / "output" / "img"
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
USER = CONFIG.get("my_reddit_username", "")
W, H = 1080, 1350
BG, CARD, FG, MUTE, ACC, RED = (12, 20, 16), (22, 34, 28), (240, 245, 240), (150, 170, 158), (46, 204, 113), (235, 87, 87)
F = "C:/Windows/Fonts/"


def font(bold, size):
    return ImageFont.truetype(F + ("segoeuib.ttf" if bold else "segoeui.ttf"), size)


def wrap(d, text, f, width):
    lines, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if d.textlength(t, font=f) <= width:
            line = t
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def text(d, xy, s, f, fill, width, gap=8):
    x, y = xy
    for ln in wrap(d, s, f, width):
        d.text((x, y), ln, font=f, fill=fill)
        y += f.size + gap
    return y


def canvas(kicker, title):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((70, 70), kicker.upper(), font=font(True, 28), fill=ACC)
    y = text(d, (70, 115), title, font(True, 60), FG, W - 140, 6)
    d.text((70, H - 70), f"u/{USER}", font=font(False, 26), fill=MUTE)
    return im, d, y + 30


def block(d, y, head, sub, color=ACC, h=None):
    hf, sf = font(True, 38), font(False, 30)
    lines = wrap(d, sub, sf, W - 240)
    h = h or 60 + hf.size + len(lines) * (sf.size + 8)
    d.rounded_rectangle((70, y, W - 70, y + h), 18, fill=CARD)
    d.rounded_rectangle((70, y, 82, y + h), 6, fill=color)
    d.text((115, y + 25), head, font=hf, fill=FG)
    yy = y + 35 + hf.size
    for ln in lines:
        d.text((115, yy), ln, font=sf, fill=MUTE)
        yy += sf.size + 8
    return y + h + 22


def three_line_email():
    im, d, y = canvas("Cold email anatomy", "The 3-line email D2C founders actually reply to")
    y = block(d, y, "1  The trigger", "Something dated and specific. \"Saw you just launched the new protein bar line.\"")
    y = block(d, y, "2  The proof", "One result for a brand like theirs. Numbers beat adjectives.")
    y = block(d, y, "3  The tiny ask", "Easy to say yes to. \"Want a 2 min Loom on your post-purchase emails?\"")
    y = block(d, y, "Cut these", "Your intro. Agency history. \"Hope you're well\". Calendar links in email 1. Anything over ~70 words.", RED)
    im.save(IMG / "three_line_email.png")


def where_email_lands():
    im, d, y = canvas("Where your pitch actually lands", "Stop emailing info@. Fix the inbox before the copy.")
    y = block(d, y, "info@  hello@  support@", "Support queue. Best case: \"please fill out our partnership form\".", RED)
    y = block(d, y, "marketing@  partnerships@", "Sponsorship triage. You get \"send a deck\", then silence.", (230, 170, 60))
    y = block(d, y, "Founder / head of ecom", "At brands under ~$20M this is where the yes happens. Verify it before you send.")
    text(d, (70, y + 10), "Fewer emails to the right inbox > more emails to the wrong one.", font(True, 34), FG, W - 140)
    im.save(IMG / "where_email_lands.png")


def twelve_triggers():
    im, d, y = canvas("Timing beats copy", "12 signals a D2C brand will reply this week")
    items = ["New product launch", "First retail doors", "Funding announced", "New growth/ecom hire",
             "Rebrand or redesign", "Moved to Shopify Plus", "New country launch", "Big pre-order win",
             "Meta ads spike", "Hiring marketers", "Founder on a podcast", "Bad review spike"]
    cw, ch, gap = (W - 140 - 20) // 2, 118, 18
    f = font(True, 32)
    for i, it in enumerate(items):
        x = 70 + (i % 2) * (cw + 20)
        yy = y + (i // 2) * (ch + gap)
        d.rounded_rectangle((x, yy, x + cw, yy + ch), 16, fill=CARD)
        d.text((x + 24, yy + 36), f"{i + 1:02d}", font=f, fill=ACC)
        d.text((x + 90, yy + 36), it, font=f, fill=FG)
    im.save(IMG / "twelve_triggers.png")


def free_founder_email():
    im, d, y = canvas("Free methods", "Find a D2C founder's real email in 5 minutes")
    steps = [("Store legal pages", "Privacy + refund policy often list the founder."),
             ("LinkedIn", "Confirm who the founder / head of ecom is today."),
             ("Podcasts + press", "Show notes and launch releases leak real emails."),
             ("Socials + Kickstarter", "Bios and creator pages."),
             ("Guess, then verify", "first@ only with an SMTP check. Unverified = skip.")]
    for i, (h_, s) in enumerate(steps):
        y = block(d, y, f"{i + 1}  {h_}", s, RED if i == 4 else ACC)
    im.save(IMG / "free_founder_email.png")


def kit_page(posts):
    def e(s):
        return html.escape(str(s or ""))
    cards = []
    for i, p in enumerate(posts):
        img = (f'<img src="img/{e(p["image"])}" alt=""><a class="btn" href="img/{e(p["image"])}" download>Download image</a>'
               if p.get("image") else "")
        subs = " ".join(f'<a class="btn" target="_blank" href="https://www.reddit.com/r/{e(s)}/submit?type=IMAGE">'
                        f'Post to r/{e(s)}</a>' if p.get("image") else
                        f'<a class="btn" target="_blank" href="https://www.reddit.com/r/{e(s)}/submit">Post to r/{e(s)}</a>'
                        for s in p["subs"])
        warn = '<span class="tag">after warm-up only</span>' if p.get("promo") else ""
        oc = " · tick <b>OC</b> if the sub offers it" if p.get("image") else ""
        flair = (f'<p class="meta">Flair: pick the first that exists → <b>{" › ".join(e(x) for x in p.get("flair", []))}</b>'
                 f'{oc}. Never NSFW/Spoiler.</p>')
        cards.append(f"""<div class="card" data-id="post{i}">
<div class="meta">Week {p['week']} · {e(p['archetype'])} {warn}</div>
<h3 id="t{i}">{e(p['title'])}</h3><button onclick="cp('t{i}',this)">Copy title</button>
<pre id="b{i}" contenteditable>{e(p['body'])}</pre><button onclick="cp('b{i}',this)">Copy body</button>
{flair}<div class="img">{img}</div><div class="row">{subs}</div>
<label><input type="checkbox" onchange="mark('post{i}',this.checked)"> Posted</label></div>""")
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FreshLeads Content Kit</title><style>
:root{{--bg:#f6f6f4;--card:#fff;--fg:#1a1a1a;--mute:#666;--line:#e3e3e0;--acc:#ff4500}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141414;--card:#1e1e1e;--fg:#eee;--mute:#999;--line:#333}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:24px 16px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;margin:16px 0}} .card.done{{opacity:.45}}
.meta{{color:var(--mute);font-size:13px}} pre{{white-space:pre-wrap;background:var(--bg);padding:12px;border-radius:8px;font:14px/1.5 system-ui}}
img{{max-width:100%;border-radius:8px;display:block;margin:10px 0}} .row{{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}}
button,.btn{{cursor:pointer;padding:6px 12px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--fg);font:inherit;text-decoration:none;display:inline-block}}
.tag{{border:1px solid var(--acc);color:var(--acc);border-radius:5px;padding:0 6px;font-size:12px}}
</style></head><body><h1>Content kit</h1>
<p class="meta">1-2 posts a week. Best time: Tue-Thu, 8-10 AM US Eastern. Check each sub's rules first (some ban images or self-promo).
Reply to every comment in the first 2 hours. That's what pushes a post up. Fill any [PLACEHOLDER] with your real numbers. Never invent stats.</p>
{''.join(cards)}
<script>
function cp(id,b){{const t=document.getElementById(id).innerText;navigator.clipboard.writeText(t);b.textContent='Copied'}}
function st(){{try{{return JSON.parse(localStorage.getItem('fl_posts')||'{{}}')}}catch(x){{return {{}}}}}}
function mark(id,v){{const s=st();s[id]=v;try{{localStorage.setItem('fl_posts',JSON.stringify(s))}}catch(x){{}}paint()}}
function paint(){{const s=st();document.querySelectorAll('.card').forEach(c=>{{const v=!!s[c.dataset.id];c.classList.toggle('done',v);c.querySelector('input').checked=v}})}}
paint();</script></body></html>"""
    (ROOT / "output" / "content_kit.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    three_line_email(); where_email_lands(); twelve_triggers(); free_founder_email()
    kit_page(json.loads((HERE / "posts.json").read_text(encoding="utf-8")))
    print("content kit built -> output/content_kit.html")
