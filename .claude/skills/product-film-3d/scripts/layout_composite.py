"""Place the REAL product into a generated scene at an exact size, angle and position.

Image models keep making the hero product huge, upright and pasted in front. Don't
describe placement in words. Composite the real product cut-out yourself, then let the
image model only blend it in (relight + add soft foreground pieces).

usage:
  python3 layout_composite.py --scene scene.png --product product_photo.jpg \
      --crop 420,300,700,960 --height 0.46 --angle 26 --cx 0.50 --cy 0.27 --out guide.png
  --crop     box around the product in the product photo (x0,y0,x1,y1); optional
  --cut-bottom  pixels to trim off the cut-out's bottom (props overlapping the base)
  --height   product height as a fraction of the scene height (pin size to the frame)
  --angle    lean in degrees; positive = top leans RIGHT (clockwise)
  --cx --cy  product centre as fractions of scene width / height
needs: pip install rembg onnxruntime pillow numpy  (model downloads from GitHub once)
"""
import argparse, numpy as np
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument('--scene', required=True); ap.add_argument('--product', required=True)
ap.add_argument('--crop'); ap.add_argument('--cut-bottom', type=int, default=0)
ap.add_argument('--height', type=float, default=0.4); ap.add_argument('--angle', type=float, default=0)
ap.add_argument('--cx', type=float, default=0.5); ap.add_argument('--cy', type=float, default=0.4)
ap.add_argument('--warm', type=float, default=1.0, help='1 = warm grade toward a honey-amber scene, 0 = none')
ap.add_argument('--out', default='layout_guide.png')
a = ap.parse_args()

from rembg import remove, new_session
src = Image.open(a.product).convert('RGB')
if a.crop: src = src.crop(tuple(int(v) for v in a.crop.split(',')))
cut = remove(src, session=new_session('isnet-general-use')).convert('RGBA')
if a.cut_bottom: cut = cut.crop((0, 0, cut.width, cut.height - a.cut_bottom))
cut = cut.crop(cut.getbbox())

# grade: lift blacks, soften contrast, optional warm shift, so it sits in an airy studio scene
arr = np.asarray(cut).astype(np.float32); rgb = arr[..., :3] / 255
rgb = 0.10 + 0.88 * rgb
if a.warm: rgb = rgb * (np.array([1.06, 0.97, 0.88]) * a.warm + (1 - a.warm))
arr[..., :3] = np.clip(rgb, 0, 1) * 255
cut = Image.fromarray(arr.astype(np.uint8))

scene = Image.open(a.scene).convert('RGBA'); W, H = scene.size
s = a.height * H / cut.height
cut = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)
cut = cut.rotate(-a.angle, resample=Image.BICUBIC, expand=True).filter(ImageFilter.GaussianBlur(0.6))
x, y = round(a.cx * W - cut.width / 2), round(a.cy * H - cut.height / 2)
scene.alpha_composite(cut, (x, y))
scene.convert('RGB').save(a.out); print('placed at', x, y, cut.size, '->', a.out)
