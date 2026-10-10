"""Panda climb-up then tumble-down concept (sec 0-15). Approximations only."""
import math, os
from PIL import Image, ImageDraw, ImageFont

W = H = 466
CX = CY = 233
S = W / 450.0
RES = "watchface/src/main/res/font"
OUT = "screenshots"
WHT, BLK = (255, 255, 255), (0, 0, 0)

def font(name, size):
    return ImageFont.truetype(os.path.join(RES, name + ".ttf"), int(size * S))

def draw_centered(d, cx, y, text, fnt, fill):
    b = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y), text, font=fnt, fill=fill)

def paint_walker(d, cx, cy, frame, ox=0, oy=0):
    """Paint front-facing panda centred at (cx+ox, cy+oy) on draw object d."""
    def X(v): return cx + ox + v
    def Y(v): return cy + oy + v
    bob = -4 if frame % 2 == 1 else 0
    cyb = cy + bob
    def Yb(v): return cyb + oy + v
    lo = 10 if frame % 2 == 0 else -10
    d.ellipse([X(-36+lo), Yb(28), X(-8+lo), Yb(58)], fill=BLK, outline=WHT, width=2)
    d.ellipse([X(8-lo), Yb(28), X(36-lo), Yb(58)], fill=BLK, outline=WHT, width=2)
    ao = 9 if frame % 2 == 0 else -9
    d.ellipse([X(-54), Yb(-4+ao), X(-30), Yb(28+ao)], fill=BLK, outline=WHT, width=2)
    d.ellipse([X(30), Yb(-4-ao), X(54), Yb(28-ao)], fill=BLK, outline=WHT, width=2)
    d.ellipse([X(-38), Yb(-12), X(38), Yb(44)], fill=WHT, outline=BLK, width=3)
    d.ellipse([X(-46), Yb(-62), X(-24), Yb(-40)], fill=BLK)
    d.ellipse([X(24), Yb(-62), X(46), Yb(-40)], fill=BLK)
    d.ellipse([X(-38), Yb(-48), X(38), Yb(10)], fill=WHT, outline=BLK, width=3)
    for ex in (-27, 9):
        d.ellipse([X(ex), Yb(-36), X(ex+18), Yb(-14)], fill=BLK)
    for ex in (-22, 14):
        d.ellipse([X(ex), Yb(-33), X(ex+5), Yb(-28)], fill=WHT)
    d.ellipse([X(-6), Yb(-10), X(6), Yb(-2)], fill=BLK)
    d.arc([X(-11), Yb(-5), X(11), Yb(9)], start=20, end=160, fill=BLK, width=2)

def panda_sprite(frame):
    spr = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    paint_walker(ImageDraw.Draw(spr), 80, 80, frame)
    return spr

def track_x(ty_dev):
    """Curve the vertical track to hug the round edge: further out at mid-height."""
    dy = (ty_dev - CY) / 233.0
    dy = max(-1.0, min(1.0, dy))
    edge = math.sqrt(max(0.0, 1.0 - dy*dy))  # 1 at middle, 0 at poles
    return CX + 105 + 25 * edge  # 338 near poles, ~363 at mid

def render(sec, mode, frame, angle, label):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    main, sub = (255, 255, 255), (187, 187, 187)
    fh, fm, fd = font("bebas", 66), font("bebas", 48), font("bebas", 32)
    draw_centered(d, CX, 96*S, "Six", fh, main)
    draw_centered(d, CX, 188*S, "Twenty", fm, main)
    draw_centered(d, CX, 188*S+52, "Eight", fm, main)
    draw_centered(d, CX, 312*S, "tue 22 sep", fd, sub)
    if mode == "walk":
        frac = sec / 7.5
        ty = (385 - frac*(385-140)) * S
        tx = track_x(ty)
        sprite = panda_sprite(frame)
        img.paste(sprite, (int(tx)-80, int(ty)-80), sprite)
        # alternate-limb label not needed
    else:
        frac = (sec - 7.5) / 7.5
        ty = (140 + frac*(385-140)) * S
        tx = track_x(ty)
        # motion trail above (rolling downward)
        for rad, col in ((52, (70,70,70)), (64, (42,42,42))):
            d.arc([tx-rad, ty-rad, tx+rad, ty+rad], start=250, end=290, fill=col, width=4)
        sprite = panda_sprite(frame).rotate(angle, resample=Image.BICUBIC, expand=False)
        img.paste(sprite, (int(tx)-80, int(ty)-80), sprite)
    d.text((12, H-24), label, fill=(120, 120, 120))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, W, H], fill=255)
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(img, mask=mask)
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    shots = [
        (0, "walk", 0, 0, "sec=00 walk up (bottom)"),
        (5, "walk", 1, 0, "sec=05 walk up (mid)"),
        (10, "ball", 0, -110, "sec=10 tucked, tumbling down"),
        (15, "ball", 1, -250, "sec=15 still tumbling down"),
    ]
    for sec, mode, fr, ang, label in shots:
        p = f"{OUT}/panda-climb-{sec:02d}.png"
        render(sec, mode, fr, ang, label).save(p)
        print("wrote", p)

if __name__ == "__main__":
    main()
