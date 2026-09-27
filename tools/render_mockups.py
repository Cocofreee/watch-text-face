"""Render round-watch mockups of the face using the real bundled fonts.

Run:  python3 tools/render_mockups.py   (needs PIL in this interpreter)
Writes screenshots/*.png at 466x466 (OPPO Watch X3 resolution).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 466
CX = CY = 233
S = W / 450.0  # 450-space -> device px
RES = "watchface/src/main/res/font"
OUT = "screenshots"

HOUR = "Six"
MINUTE = "Twenty Eight"
DATE = "tue 22 sep"
DOT_R = 205  # orbit radius in device px (panda center distance from face center)


def font(name, size):
    return ImageFont.truetype(os.path.join(RES, name + ".ttf"), int(size * S))


def draw_centered(d, cx, y, text, fnt, fill):
    b = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y), text, font=fnt, fill=fill)


def wrap_minute(d, text, fnt, max_w):
    b = d.textbbox((0, 0), text, font=fnt)
    if b[2] - b[0] <= max_w:
        return [text]
    parts = text.split(" ")
    best, best_diff = None, None
    for k in range(1, len(parts)):
        top = " ".join(parts[:k])
        w = d.textbbox((0, 0), top, font=fnt)[2]
        diff = abs(w - max_w / 2)
        if best_diff is None or diff < best_diff:
            best, best_diff = k, diff
    return [" ".join(parts[:best]), " ".join(parts[best:])]


def draw_panda(d, dx, dy):
    """Design A (Scout) at 40px, like the WFF version: white head/ears with
    black outline, grey inner ears, eyes with glints, nose."""
    bx, by = dx - 20, dy - 20
    for ex, ey in ((bx + 1, by + 1), (bx + 29, by + 1)):
        d.ellipse([ex, ey, ex + 10, ey + 10], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
        d.ellipse([ex + 3, ey + 3, ex + 7, ey + 7], fill=(187, 187, 187))
    d.ellipse([bx + 5, by + 8, bx + 35, by + 34], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    for ex, ey in ((bx + 12, by + 16), (bx + 23, by + 16)):
        d.ellipse([ex, ey, ex + 5, ey + 7], fill=(0, 0, 0))
    for ex, ey in ((bx + 14, by + 17), (bx + 25, by + 17)):
        d.ellipse([ex, ey, ex + 2, ey + 2], fill=(255, 255, 255))
    d.ellipse([bx + 18, by + 26, bx + 22, by + 29], fill=(0, 0, 0))


RAINBOW = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0),
           (0, 255, 255), (0, 0, 255), (255, 0, 255)]


def draw_rainbow(d, cx, cy, radius, width=14):
    import math as _m
    steps = 90
    for k in range(steps):
        a0 = _m.radians(270 + 180 * k / steps)
        a1 = _m.radians(270 + 180 * (k + 1) / steps)
        col = RAINBOW[min(6, k * 7 // steps)]
        d.line([cx + radius * _m.sin(a0), cy - radius * _m.cos(a0),
                cx + radius * _m.sin(a1), cy - radius * _m.cos(a1)],
               fill=col, width=width)


def render(theme, fontname, ambient=False, second=28, hour="Six",
           minute="Twenty Eight", panda=True, rainbow=False):
    bg = (0, 0, 0) if (theme == "dark" or ambient) else (255, 255, 255)
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    if theme == "light" and not ambient:
        d.ellipse([CX - 233, CY - 233, CX + 233, CY + 233], fill=(255, 255, 255))
    if ambient:
        main, sub = (150, 150, 150), (100, 100, 100)
    elif theme == "dark":
        main, sub = (255, 255, 255), (187, 187, 187)
    else:
        main, sub = (0, 0, 0), (85, 85, 85)

    fh = font(fontname, 66)
    fm = font(fontname, 48)
    fd = font(fontname, 32)
    draw_centered(d, CX, 96 * S, hour, fh, main)
    lines = wrap_minute(d, minute, fm, 400)
    y = 188 * S
    for ln in lines:
        draw_centered(d, CX, y, ln, fm, main)
        b = d.textbbox((0, 0), ln, font=fm)
        y += (b[3] - b[1]) + 6
    draw_centered(d, CX, 312 * S, DATE, fd, sub)

    if rainbow and not ambient:
        draw_rainbow(d, CX, CY, 215)

    if not ambient:
        # panda seconds marker, 6 degrees per second clockwise from 12
        a = math.radians(second * 6)
        dx = CX + DOT_R * math.sin(a)
        dy = CY - DOT_R * math.cos(a)
        if panda:
            draw_panda(d, dx, dy)
        else:
            d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=main)

    # circular mask -> round watch look
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, W, H], fill=255)
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(img, mask=mask)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    render("dark", "bebas").save(f"{OUT}/shot-dark-bebas.png")
    render("light", "bebas").save(f"{OUT}/shot-light-bebas.png")
    render("dark", "unifraktur").save(f"{OUT}/shot-dark-unifraktur.png")
    render("dark", "medieval").save(f"{OUT}/shot-dark-medieval.png")
    render("dark", "bebas", ambient=True).save(f"{OUT}/shot-ambient.png")
    render("dark", "bebas", second=10, hour="Twelve", minute="O'Clock",
           rainbow=True).save(f"{OUT}/shot-rainbow.png")
    print("wrote", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
