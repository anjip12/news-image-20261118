#!/usr/bin/env python3
"""news-image-20261118 v3 — 'THE WORLD IN ONE DAY' front page.

Drawn from scratch with Pillow: navy masthead, six story panels, ALSO
strip, footer. v3 changes vs v2: bigger Nvidia bar chart in the lead
panel and a redrawn broken Crimea bridge illustration.
Output: entry.png (1024x1024, deterministic).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
NAVY = (20, 38, 63)
GOLD = (242, 201, 76)
RED = (178, 34, 34)
INK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (110, 110, 110)
DARK_BLUE = (28, 52, 84)
TEAL = (15, 118, 110)
OCHRE = (146, 96, 20)
SKY = (198, 224, 240)
SEA = (38, 84, 138)
STEEL = (70, 70, 70)
SPIRAL_BG = (16, 54, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def sans(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), size)


def bold(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def headline(d, x, y, text, size, max_w, color=INK, min_size=18):
    """Bold headline, at most two lines; shrink from `size` until it fits."""
    s = size
    while s > min_size:
        if len(wrap(d, text, bold(s), max_w)) <= 2:
            break
        s -= 2
    f = bold(s)
    lines = wrap(d, text, f, max_w)
    lh = int(round(s * 1.2))
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=color)
    return y + (len(lines) - 1) * lh + s


def body(d, x, y, text, size, max_w, leading, color=INK):
    f = sans(size)
    lines = wrap(d, text, f, max_w)
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=f, fill=color)
    return y + (len(lines) - 1) * leading + size


def card(d, x0, y0, x1, y1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=WHITE,
                        outline=INK, width=2)


def kicker(d, x, y, text, color):
    d.text((x, y), text, font=bold(22), fill=color)


def draw_markets(d):
    card(d, 24, 140, 636, 556)
    kicker(d, 44, 158, "MARKETS", RED)
    hy = headline(d, 44, 188, "NVIDIA BEATS BIG: $115.8BN QUARTER", 40, 572)
    body(d, 44, hy + 10,
         "Revenue doubles, up 103%, and guidance rises to $130bn \u2014 the "
         "first report since Jensen Huang quit.", 21, 572, 28)
    # Bigger bar chart: baseline y=520, bars 132 wide, step 185 from x=70,
    # heights scaled 140 * value / max.
    vals = [57, 96, 116]
    labs = ["$57bn", "$96bn", "$116bn"]
    subs = ["A YEAR AGO", "LAST QTR", "THIS QTR"]
    cols = [(150, 180, 215), (80, 130, 195), (20, 60, 120)]
    base_y = 520
    mx = max(vals)
    d.line([56, base_y, 588, base_y], fill=INK, width=3)
    for i, v in enumerate(vals):
        bx = 70 + i * 185
        hgt = round(140 * v / mx)
        top = base_y - hgt
        d.rectangle([bx, top, bx + 132, base_y], fill=cols[i])
        f = bold(22)
        lw = d.textlength(labs[i], font=f)
        d.text((bx + (132 - lw) / 2, top - 30), labs[i], font=f, fill=INK)
        fs = bold(15)
        sw = d.textlength(subs[i], font=fs)
        d.text((bx + (132 - sw) / 2, base_y + 8), subs[i], font=fs, fill=GREY)


def draw_asia(d):
    card(d, 652, 140, 1000, 344)
    kicker(d, 672, 158, "ASIA DIPLOMACY", DARK_BLUE)
    hy = headline(d, 672, 188, "APEC OPENS IN SHENZHEN", 30, 308)
    body(d, 672, hy + 8,
         "Xi urges open trade; Putin takes the stage. First Trump\u2013Xi\u2013Putin "
         "talks set for Thursday.", 19, 308, 25)


def draw_gulf(d):
    card(d, 652, 360, 1000, 556)
    kicker(d, 672, 378, "GULF TENSIONS", TEAL)
    hy = headline(d, 672, 408, "IRAN HITS KUWAIT AND BAHRAIN", 30, 308)
    body(d, 672, hy + 8,
         "Tehran fires drones at U.S. bases after American jets hit a missile "
         "site on Qeshm Island.", 19, 308, 25)


def draw_ukraine(img, d):
    card(d, 24, 572, 333, 920)
    kicker(d, 44, 590, "WAR IN UKRAINE", RED)
    hy = headline(d, 44, 620, "CRIMEA BRIDGE DOWN", 30, 269)
    ix0, iy0 = 44, hy + 10
    ix1 = 313
    iw, ih = ix1 - ix0, 118
    mid = ih // 2            # 59: horizon / sea surface
    deck = mid - 26          # 33: deck line
    layer = Image.new("RGB", (iw, ih), SKY)
    ld = ImageDraw.Draw(layer)
    ld.rectangle([0, mid, iw, ih], fill=SEA)
    # gold sun, top right
    ld.ellipse([iw - 44, 8, iw - 12, 40], fill=GOLD)
    # two pylons, from deck-44 to deck (tops clip at the box edge by design)
    for px in (52, iw - 52):
        ld.rectangle([px, deck - 44, px + 7, deck], fill=STEEL)
        # straight stay cables from pylon top to deck +/-38px
        ld.line([px + 3, deck - 44, px - 38, deck], fill=STEEL, width=3)
        ld.line([px + 3, deck - 44, px + 38, deck], fill=STEEL, width=3)
    # intact deck, left and right of the gap
    ld.rectangle([0, deck, 92, deck + 10], fill=STEEL)
    ld.rectangle([178, deck, iw, deck + 10], fill=STEEL)
    # fallen middle span: two slanted segments dropping into the strait
    ld.line([92, deck + 5, 128, mid + 14], fill=STEEL, width=10)
    ld.line([178, deck + 5, 146, mid + 16], fill=STEEL, width=10)
    # small white wave arcs on the sea surface
    for cx in (60, 135, 215):
        ld.arc([cx - 14, mid + 2, cx + 14, mid + 14], 180, 360,
               fill=WHITE, width=3)
    img.paste(layer, (ix0, iy0))
    body(d, 44, iy0 + ih + 8,
         "A road arch of the 19-km Kerch bridge collapses into the strait on "
         "the second day of strikes.", 19, 269, 24)


def draw_politics(d):
    card(d, 357, 572, 666, 920)
    kicker(d, 377, 590, "U.S. POLITICS", DARK_BLUE)
    hy = headline(d, 377, 620, "DEMOCRATS TAKE THE SENATE", 30, 269)
    bx, by = 377, hy + 10
    bw, bh = 269, 52
    dem_w = round(bw * 0.56)
    d.rectangle([bx, by, bx + dem_w, by + bh], fill=(31, 93, 176))
    d.rectangle([bx + dem_w, by, bx + bw, by + bh], fill=RED)
    f = bold(22)
    for txt, cx0, cx1 in (("56 DEM", bx, bx + dem_w),
                          ("44 GOP", bx + dem_w, bx + bw)):
        tw = d.textlength(txt, font=f)
        d.text((cx0 + (cx1 - cx0 - tw) / 2, by + (bh - 22) / 2),
               txt, font=f, fill=WHITE)
    ly = by + bh + 8
    d.text((bx, ly), "INCOMING SENATE \u00b7 100 SEATS", font=bold(15), fill=GREY)
    body(d, bx, ly + 25,
         "Mary Peltola wins Alaska, giving Democrats a 56\u201344 majority in "
         "the incoming Senate.", 19, 269, 24)


def draw_weather(img, d):
    card(d, 690, 572, 1000, 920)
    kicker(d, 710, 590, "WEATHER", OCHRE)
    hy = headline(d, 710, 620, "CYCLONE AKVAN BUILDS", 30, 269)
    ix0, iy0 = 710, hy + 10
    ix1 = 980
    iw, ih = ix1 - ix0, 118
    layer = Image.new("RGB", (iw, ih), SPIRAL_BG)
    ld = ImageDraw.Draw(layer)
    cx, cy = iw // 2, ih // 2
    for i in range(8):
        r = 46 - 8 * i
        if r <= 0:
            continue
        ld.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
               fill=WHITE, width=6)
    ld.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=GOLD)
    img.paste(layer, (ix0, iy0))
    body(d, 710, iy0 + ih + 8,
         "A severe cyclonic storm gathers in the Bay of Bengal, heading for "
         "India's Andhra coast.", 19, 269, 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.text((24, 12), "THE WORLD IN ONE DAY", font=bold(62), fill=WHITE)
    d.text((26, 74), "WEDNESDAY  \u00b7  18 NOVEMBER 2026", font=bold(33), fill=GOLD)
    d.rectangle([0, 116, W, 124], fill=RED)
    draw_markets(d)
    draw_asia(d)
    draw_gulf(d)
    draw_ukraine(img, d)
    draw_politics(d)
    draw_weather(img, d)
    # ALSO strip
    d.rectangle([0, 934, W, 972], fill=NAVY)
    d.text((24, 943), "ALSO:", font=bold(21), fill=GOLD)
    items = ["Quad in Manila", "Dhoni ends IPL career",
             "Amazon $7bn for India", "Ebola tops 11,000 cases"]
    f = sans(19)
    text = " \u00b7 ".join(items)
    while d.textlength(text, font=f) > 904 and len(items) > 1:
        items.pop()
        text = " \u00b7 ".join(items)
    d.text((96, 944), text, font=f, fill=WHITE)
    # footer
    d.text((24, 980), "Sources: Reuters, AP, CNN  \u00b7  Images drawn for this page",
           font=sans(17), fill=GREY)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    print(out)


if __name__ == "__main__":
    main()
