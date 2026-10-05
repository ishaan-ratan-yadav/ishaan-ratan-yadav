#!/usr/bin/env python3
"""Render premium 3D images for Reddit image/gallery posts (real WebGL 3D + editorial type) in the local Chrome.

Scenes (tools/media/scenes.js):
  inbox        info@ tray overflowing with envelopes vs one founder envelope on a pedestal
  bars         3D bar comparison, e.g. reply rates (--data "Industry:2.5:2-3%,Ours:8:8%")
  five-buyers  a lead card with 5 buyer tokens and a RETIRED stamp (the 5-buyers-then-retired model)
  statement    abstract green/orange hero (any post)

Text: wrap words in *asterisks* for the italic accent style; use \\n for line breaks.
Tags: --tags "info@ · support queue:hot|founder · decides:hi" (classes: hi, hot, lo).

Sizes: 4x5 = 1080x1350 (feed-filling portrait, galleries) · wide = 1200x628 (link-style / landscape) · 1x1 = 1200x1200.
Rendered at 2x by default (2160x2700 for 4x5).

Branding: none by default (branded images in help-only subs read as ads). --brand adds the site in the footer
(growth phase, promo-OK subs only). --foot-left/--foot-right set the footer text by hand.

Examples:
  python tools/make_media.py inbox --kicker "Cold outreach to D2C" --title "Stop pitching *info@*." -o media/2026-10-05_P1_inbox.jpg
  python tools/make_media.py bars --data "Industry avg:2.5:2-3%,Our outreach:8:8%" --title "Same offer. *Different inbox.*" -o media/x.jpg
  python tools/make_media.py five-buyers --title "5 buyers.\\nThen *retired*." --size wide -o media/x.jpg

Needs: pip install playwright (uses the installed Google Chrome, no browser download). Always LOOK at the render
(Read the image) before it goes in a pack: nothing cropped, nothing touching the kicker or headline, text readable.
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SIZES = {"4x5": (1080, 1350), "wide": (1200, 628), "1x1": (1200, 1200)}
SCENES = ["inbox", "bars", "five-buyers", "statement"]


def render(spec: dict, out: Path, scale: float = 2.0) -> Path:
    from playwright.sync_api import sync_playwright

    html = (HERE / "media" / "engine.html").read_text(encoding="utf-8")
    scenes = (HERE / "media" / "scenes.js").read_text(encoding="utf-8")
    html = html.replace("__SPEC__", json.dumps(spec)).replace("__SCENES__", scenes)

    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            args=["--ignore-gpu-blocklist", "--enable-gpu", "--use-angle=d3d11", "--enable-unsafe-swiftshader"],
        )
        page = browser.new_page(viewport={"width": spec["w"], "height": spec["h"]}, device_scale_factor=scale)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.set_content(html, wait_until="networkidle")
        try:
            page.wait_for_function("window.READY === true", timeout=90_000)
        except Exception:
            browser.close()
            sys.exit("Render failed:\n" + "\n".join(errors or ["timed out waiting for the scene"]))
        kw = {"type": "jpeg", "quality": 93} if out.suffix.lower() in (".jpg", ".jpeg") else {"type": "png"}
        page.locator("#stage").screenshot(path=str(out), **kw)
        browser.close()
    return out


def parse_data(s: str) -> list[dict]:
    rows = []
    for part in filter(None, (x.strip() for x in (s or "").split(","))):
        bits = part.split(":")
        label, value = bits[0].strip(), float(bits[1]) if len(bits) > 1 else 0.0
        hero = label.endswith("!")
        rows.append({"label": label.rstrip("!"), "value": value, "display": bits[2].strip() if len(bits) > 2 else None, "hero": hero})
    return rows


def parse_tags(s: str) -> list[list[str]] | None:
    if not s:
        return None
    out = []
    for part in s.split("|"):
        text, _, cls = part.rpartition(":") if ":" in part else (part, "", "")
        out.append([text.strip() or part.strip(), cls.strip()])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scene", choices=SCENES)
    ap.add_argument("--title", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--kicker", default="Outbound to D2C brands")
    ap.add_argument("--accent", default="#2ECC71", help="FreshLeads green (default)")
    ap.add_argument("--hot", default="#FF4500", help="Reddit orange for the 'bad'/alert side")
    ap.add_argument("--size", choices=SIZES, default="4x5")
    ap.add_argument("--seed", type=int, default=3, help="shape/pile variation")
    ap.add_argument("--data", default="", help="bars scene: 'label:value[:display],...'; end a label with ! to mark the hero bar")
    ap.add_argument("--tags", default="", help="'text:class|text:class' pills over the scene (classes hi, hot, lo)")
    ap.add_argument("--brand", action="store_true", help="put getfreshleads.io in the footer (growth phase + promo-OK subs only)")
    ap.add_argument("--foot-left", default="")
    ap.add_argument("--foot-right", default="")
    ap.add_argument("--h1", type=float, help="headline size in %% of the short side (default 8.6 portrait, 9.2 wide)")
    ap.add_argument("--scale", type=float, default=2.0, help="device scale factor (2 = 2160x2700 for 4x5)")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    w, h = SIZES[a.size]
    foot_left, foot_right = a.foot_left, a.foot_right
    if a.brand:
        foot_left = foot_left or "getfreshleads.io"
        foot_right = foot_right or "verified D2C founder leads"
    spec = {"scene": a.scene, "title": a.title.replace("\\n", "\n"), "sub": a.sub.replace("\\n", "\n"),
            "kicker": a.kicker, "accent": a.accent, "hot": a.hot, "w": w, "h": h, "seed": a.seed,
            "data": parse_data(a.data), "tags": parse_tags(a.tags), "footLeft": foot_left, "footRight": foot_right}
    if a.h1:
        spec["h1"] = a.h1
    print("Wrote", render(spec, Path(a.out), a.scale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
