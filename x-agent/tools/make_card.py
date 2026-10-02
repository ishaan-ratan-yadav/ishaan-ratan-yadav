#!/usr/bin/env python3
"""Render simple on-brand image cards for X posts (needs Pillow: pip install pillow).

Card styles:
  statement  - one bold line or two (hot takes, quotes, big claims)
  list       - title + numbered points (tips, lessons, breakdowns)
  versus     - two columns (before/after, client brief vs delivery, AI vs 3D)

Examples:
  python tools/make_card.py statement "Clients don't pay for renders.\nThey pay for attention." -o media/take.png
  python tools/make_card.py list "5 things that make a 3D ad feel expensive" "Slow camera" "Real light" "Micro detail" -o media/list.png
  python tools/make_card.py versus "Client brief" "What we delivered" "A spinning bottle" "A bottle that erupts into a city" -o media/vs.png

Brand colours and handle come from config.json ("brand" block) when present.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BRAND = {"bg": "#0E0E12", "fg": "#F4F4F6", "accent": "#7C6CFF", "muted": "#8A8A96",
                 "handle": "@EvolvesStudio", "size": [1600, 900]}
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # macOS
    "C:/Windows/Fonts/arialbd.ttf",                       # Windows
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def brand() -> dict:
    cfg = ROOT / "config.json"
    b = dict(DEFAULT_BRAND)
    if cfg.exists():
        b.update(json.loads(cfg.read_text()).get("brand", {}))
    return b


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap_px(text, f, max_w):
    """Greedy word wrap by measured pixel width."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = f"{line} {word}".strip()
            if not line or f.getlength(trial) <= max_w:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return "\n".join(lines)


def fit_text(draw, text, max_w, max_h, start=120, min_size=28):
    """Largest font size at which the wrapped text fits the box."""
    for size in range(start, min_size - 1, -4):
        f = font(size)
        body = wrap_px(text, f, max_w)
        box = draw.multiline_textbbox((0, 0), body, font=f, spacing=size // 4)
        if box[2] - box[0] <= max_w and box[3] - box[1] <= max_h:
            return body, f
    return body, f


def canvas(b):
    w, h = b["size"]
    img = Image.new("RGB", (w, h), b["bg"])
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 18, h], fill=b["accent"])
    d.text((80, h - 80), b["handle"], font=font(34), fill=b["muted"])
    return img, d, w, h


def statement(text, b):
    img, d, w, h = canvas(b)
    body, f = fit_text(d, text, w - 200, h - 260)
    d.multiline_text((100, 100), body, font=f, fill=b["fg"], spacing=f.size // 4)
    return img


def listing(title, points, b):
    img, d, w, h = canvas(b)
    tb, tf = fit_text(d, title, w - 200, 220, start=80)
    d.multiline_text((100, 80), tb, font=tf, fill=b["fg"], spacing=tf.size // 4)
    top = 80 + d.multiline_textbbox((0, 0), tb, font=tf)[3] + 60
    avail = h - top - 140
    size = max(30, min(56, avail // max(1, len(points)) - 18))
    pf = font(size)
    for i, p in enumerate(points, 1):
        y = top + (i - 1) * (size + 22)
        d.text((100, y), f"{i:02d}", font=pf, fill=b["accent"])
        d.text((100 + size * 2, y), p, font=pf, fill=b["fg"])
    return img


def versus(left_title, right_title, left, right, b):
    img, d, w, h = canvas(b)
    mid = w // 2
    d.line([mid, 90, mid, h - 140], fill=b["muted"], width=3)
    for x, title, body, colour in ((100, left_title, left, b["muted"]), (mid + 60, right_title, right, b["accent"])):
        d.text((x, 90), title.upper(), font=font(40), fill=colour)
        tb, tf = fit_text(d, body, mid - 160, h - 360, start=88)
        d.multiline_text((x, 180), tb, font=tf, fill=b["fg"], spacing=tf.size // 4)
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("style", choices=["statement", "list", "versus"])
    ap.add_argument("parts", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()
    b = brand()
    parts = [p.replace("\\n", "\n") for p in args.parts]
    if args.style == "statement":
        img = statement(parts[0], b)
    elif args.style == "list":
        img = listing(parts[0], parts[1:], b)
    else:
        if len(parts) != 4:
            ap.error("versus needs: left_title right_title left_text right_text")
        img = versus(*parts, b)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
