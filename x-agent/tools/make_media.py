#!/usr/bin/env python3
"""Render premium 3D post media for X (real WebGL 3D + editorial type), using the local Chrome.

Scenes (tools/media/scenes.js):
  ai-vs-3d     two bottles: a melting AI version vs the crisp 3D product
  logo-memory  chrome tangle ("decoration") vs one clean bevelled mark ("a logo")
  invoice      curled UNPAID invoice with floating gold coins (freelance / money posts)
  statement    abstract iridescent blob + glass sphere + chrome ring (any post)

Text: wrap words in *asterisks* for the italic accent style; use \\n for line breaks.

Examples:
  python tools/make_media.py ai-vs-3d --title "AI for the *vibe*.\\n3D for the *product*." -o media/p1.jpg
  python tools/make_media.py statement --kicker "Freelance" --title "Raise your *rates*." --seed 5 --size 16x9 -o media/x.jpg

Needs: pip install playwright (uses the installed Google Chrome, no browser download).
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIZES = {"4x5": (1080, 1350), "16x9": (1600, 900), "1x1": (1200, 1200)}


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scene", choices=["ai-vs-3d", "logo-memory", "invoice", "statement"])
    ap.add_argument("--title", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--kicker", default="Evolves Studio")
    ap.add_argument("--accent", default="#7C6CFF")
    ap.add_argument("--size", choices=SIZES, default="4x5", help="4x5 fills the most feed space on X mobile")
    ap.add_argument("--seed", type=int, default=3, help="statement scene: shape variation")
    ap.add_argument("--h1", type=float, help="headline size in %% of the short side (default 8.6 portrait)")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    w, h = SIZES[a.size]
    spec = {"scene": a.scene, "title": a.title.replace("\\n", "\n"), "sub": a.sub.replace("\\n", "\n"),
            "kicker": a.kicker, "accent": a.accent, "w": w, "h": h, "seed": a.seed}
    if a.h1:
        spec["h1"] = a.h1
    print("Wrote", render(spec, Path(a.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
