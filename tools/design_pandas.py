"""4 panda design studies (40x40 box). Renders a contact sheet + individuals.

Run:  python3 tools/design_pandas.py   (needs PIL in system python)
The WFF versions in tools/generate_watchface.py mirror these coordinates.
"""
import os
from PIL import Image, ImageDraw

OUT = "screenshots/pandas"
WHT, BLK, GRY = (255, 255, 255), (0, 0, 0), (187, 187, 187)


def base(d, head=(5, 8, 35, 34), ears=((1, 1, 11, 11), (29, 1, 39, 11)),
         inner=True):
    for (x0, y0, x1, y1) in ears:
        d.ellipse([x0, y0, x1, y1], fill=WHT, outline=BLK, width=2)
        if inner:
            d.ellipse([x0 + 3, y0 + 3, x1 - 3, y1 - 3], fill=GRY)
    d.ellipse(head, fill=WHT, outline=BLK, width=2)


def nose(d, box=(18, 26, 22, 29)):
    d.ellipse(box, fill=BLK)


def design_a(d):  # Scout: classic + glints + inner ears
    base(d)
    for (x0, y0, x1, y1) in ((12, 16, 17, 23), (23, 16, 28, 23)):
        d.ellipse([x0, y0, x1, y1], fill=BLK)
    for (x0, y0, x1, y1) in ((14, 17, 16, 19), (25, 17, 27, 19)):
        d.ellipse([x0, y0, x1, y1], fill=WHT)
    nose(d)


def design_b(d):  # Chubby: wide head, blush, o mouth
    base(d, head=(3, 8, 37, 34))
    for (x0, y0, x1, y1) in ((13, 16, 17, 22), (23, 16, 27, 22)):
        d.ellipse([x0, y0, x1, y1], fill=BLK)
    for (x0, y0, x1, y1) in ((7, 24, 12, 28), (28, 24, 33, 28)):
        d.ellipse([x0, y0, x1, y1], fill=GRY)
    d.ellipse([18, 24, 22, 29], outline=BLK, width=2)


def design_c(d):  # Shades: sunglasses bar + shine
    base(d, inner=False)
    d.rectangle([8, 14, 32, 23], fill=BLK)
    d.rectangle([11, 16, 15, 18], fill=WHT)
    nose(d)


def design_d(d):  # Baby: small ears, huge eyes
    base(d, ears=((3, 2, 9, 8), (31, 2, 37, 8)))
    for (x0, y0, x1, y1) in ((11, 15, 18, 24), (22, 15, 29, 24)):
        d.ellipse([x0, y0, x1, y1], fill=BLK)
    for (x0, y0, x1, y1) in ((13, 16, 15, 18), (24, 16, 26, 18)):
        d.ellipse([x0, y0, x1, y1], fill=WHT)
    d.ellipse([19, 26, 21, 28], fill=BLK)


DESIGNS = [
    ("a-scout", "A — Scout (classic + glints)", design_a),
    ("b-chubby", "B — Chubby (blush + o mouth)", design_b),
    ("c-shades", "C — Shades (sunglasses)", design_c),
    ("d-baby", "D — Baby (big eyes)", design_d),
]


def render(fn, scale=4):
    img = Image.new("RGB", (40, 40), (0, 0, 0))
    fn(ImageDraw.Draw(img))
    return img.resize((40 * scale, 40 * scale), Image.NEAREST)


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, _, fn in DESIGNS:
        render(fn).save(f"{OUT}/panda-{slug}.png")
    sheet = Image.new("RGB", (2 * 200, 2 * 220), (18, 18, 18))
    sd = ImageDraw.Draw(sheet)
    for k, (slug, label, fn) in enumerate(DESIGNS):
        x, y = (k % 2) * 200, (k // 2) * 220
        sheet.paste(render(fn), (x + 20, y + 8))
        sd.text((x + 12, y + 176), label, fill=(255, 255, 255))
    sheet.save(f"{OUT}/panda-designs.png")
    print("wrote", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
