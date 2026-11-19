#!/usr/bin/env python3
"""news-image-20261118 v3 -- "THE WORLD IN ONE DAY" newspaper front page.

Drawn with Pillow only. Fully deterministic: no randomness, no timestamps,
no network. Run: python3 gen.py  -> writes entry.png (1024x1024) next
to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (20, 38, 63)
GOLD = (242, 201, 76)
RED = (178, 34, 34)
INK = (0, 0, 0)
GRAY = (110, 110, 110)
DARKBLUE = (28, 52, 84)
TEAL = (15, 118, 110)
AMBER = (146, 96, 20)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap, measured with the real font."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if not cur or draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped body text; return y just past the last line."""
    for line in wrap_text(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(draw, x, y, text, size, max_w, fill=INK):
    """Bold headline, max 2 lines; shrink from `size` until it fits."""
    while size > 18:
        fnt = F(BOLD, size)
        lines = wrap_text(draw, text, fnt, max_w)
        if len(lines) <= 2 and all(
            draw.textlength(ln, font=fnt) <= max_w for ln in lines
        ):
            break
        size -= 1
    fnt = F(BOLD, size)
    lines = wrap_text(draw, text, fnt, max_w)
    lh = int(size * 1.2)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def card(draw, box):
    draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=INK, width=2)


def kicker(draw, x, y, text, color):
    draw.text((x, y), text, font=F(BOLD, 22), fill=color)


def masthead(draw):
    draw.rectangle([0, 0, W, 116], fill=NAVY)
    draw.text((24, 12), "THE WORLD IN ONE DAY", font=F(BOLD, 62), fill=WHITE)
    draw.text((26, 74), "WEDNESDAY  \u00b7  18 NOVEMBER 2026",
              font=F(BOLD, 33), fill=GOLD)
    draw.rectangle([0, 116, W, 124], fill=RED)


def panel_markets(draw):
    card(draw, [24, 140, 636, 556])
    kicker(draw, 44, 158, "MARKETS", RED)
    y = fit_headline(draw, 44, 186, "NVIDIA BEATS BIG: $115.8BN QUARTER",
                     40, 572)
    draw_wrapped(
        draw, 44, y + 8,
        "Revenue doubles, up 103%, and guidance rises to $130bn \u2014 the "
        "first report since Jensen Huang quit.",
        F(REG, 21), 572, 28,
    )
    vals = [57, 96, 116]
    labels = ["$57bn", "$96bn", "$116bn"]
    subs = ["A YEAR AGO", "LAST QTR", "THIS QTR"]
    colors = [(150, 180, 215), (80, 130, 195), (20, 60, 120)]
    base = 520
    top = max(vals)
    draw.line([44, base, 612, base], fill=INK, width=3)
    for i, v in enumerate(vals):
        x = 70 + i * 185
        h = int(round(140 * v / top))
        y0 = base - h
        draw.rectangle([x, y0, x + 132, base], fill=colors[i])
        lab = labels[i]
        lw = draw.textlength(lab, font=F(BOLD, 22))
        draw.text((x + (132 - lw) / 2, y0 - 28), lab, font=F(BOLD, 22),
                  fill=INK)
        sub = subs[i]
        sw = draw.textlength(sub, font=F(BOLD, 15))
        draw.text((x + (132 - sw) / 2, base + 8), sub, font=F(BOLD, 15),
                  fill=GRAY)


def panel_asia(draw):
    card(draw, [652, 140, 1000, 344])
    kicker(draw, 672, 158, "ASIA DIPLOMACY", DARKBLUE)
    y = fit_headline(draw, 672, 186, "APEC OPENS IN SHENZHEN", 30, 308)
    draw_wrapped(
        draw, 672, y + 8,
        "Xi urges open trade; Putin takes the stage. First Trump\u2013Xi\u2013Putin "
        "talks set for Thursday.",
        F(REG, 19), 308, 25,
    )


def panel_gulf(draw):
    card(draw, [652, 360, 1000, 556])
    kicker(draw, 672, 378, "GULF TENSIONS", TEAL)
    y = fit_headline(draw, 672, 406, "IRAN HITS KUWAIT AND BAHRAIN", 30, 308)
    draw_wrapped(
        draw, 672, y + 8,
        "Tehran fires drones at U.S. bases after American jets hit a missile "
        "site on Qeshm Island.",
        F(REG, 19), 308, 25,
    )


def panel_ukraine(draw):
    card(draw, [24, 572, 333, 920])
    kicker(draw, 44, 590, "WAR IN UKRAINE", RED)
    y = fit_headline(draw, 44, 618, "CRIMEA BRIDGE DOWN", 30, 269)
    x0, x1 = 44, 313
    y0 = y + 10
    y1 = y0 + 118
    mid = (y0 + y1) // 2
    deck = mid - 26
    gray = (70, 70, 70)
    draw.rectangle([x0, y0, x1, y1], fill=(198, 224, 240))
    draw.ellipse([x1 - 44, y0 + 8, x1 - 12, y0 + 32], fill=GOLD)
    draw.rectangle([x0, mid, x1, y1], fill=(38, 84, 138))
    ptop = max(deck - 44, y0)
    for px in (x0 + 52, x1 - 52):
        draw.rectangle([px - 3, ptop, px + 3, deck], fill=gray)
        draw.line([px, ptop, px - 38, deck], fill=gray, width=3)
        draw.line([px, ptop, px + 38, deck], fill=gray, width=3)
    draw.rectangle([x0, deck - 5, x0 + 92, deck + 5], fill=gray)
    draw.rectangle([x0 + 178, deck - 5, x1, deck + 5], fill=gray)
    draw.line([x0 + 92, deck, x0 + 128, mid + 14], fill=gray, width=10)
    draw.line([x0 + 178, deck, x0 + 146, mid + 16], fill=gray, width=10)
    for wx in (x0 + 40, x0 + 96, x0 + 176):
        draw.arc([wx, mid - 8, wx + 26, mid + 8], 180, 360,
                 fill=WHITE, width=3)
    draw_wrapped(
        draw, 44, y1 + 10,
        "A road arch of the 19-km Kerch bridge collapses into the strait on "
        "the second day of strikes.",
        F(REG, 19), 269, 24,
    )


def panel_politics(draw):
    card(draw, [357, 572, 666, 920])
    kicker(draw, 377, 590, "U.S. POLITICS", DARKBLUE)
    y = fit_headline(draw, 377, 618, "DEMOCRATS TAKE THE SENATE", 30, 269)
    bx, by = 377, y + 10
    bw, bh = 269, 52
    blue_w = int(round(bw * 0.56))
    draw.rectangle([bx, by, bx + blue_w, by + bh], fill=(31, 93, 176))
    draw.rectangle([bx + blue_w, by, bx + bw, by + bh], fill=RED)
    fnt = F(BOLD, 22)
    t1, t2 = "56 DEM", "44 GOP"
    ty = by + (bh - 22) // 2 - 2
    draw.text((bx + (blue_w - draw.textlength(t1, font=fnt)) / 2, ty),
              t1, font=fnt, fill=WHITE)
    draw.text((bx + blue_w + (bw - blue_w - draw.textlength(t2, font=fnt)) / 2,
               ty), t2, font=fnt, fill=WHITE)
    lab = "INCOMING SENATE \u00b7 100 SEATS"
    lw = draw.textlength(lab, font=F(BOLD, 15))
    draw.text((bx + (bw - lw) / 2, by + bh + 8), lab, font=F(BOLD, 15),
              fill=GRAY)
    draw_wrapped(
        draw, 377, by + bh + 8 + 24,
        "Mary Peltola wins Alaska, giving Democrats a 56\u201344 majority in "
        "the incoming Senate.",
        F(REG, 19), 269, 24,
    )


def panel_weather(draw):
    card(draw, [690, 572, 1000, 920])
    kicker(draw, 710, 590, "WEATHER", AMBER)
    y = fit_headline(draw, 710, 618, "CYCLONE AKVAN BUILDS", 30, 270)
    x0, x1 = 710, 980
    y0 = y + 10
    y1 = y0 + 118
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rectangle([x0, y0, x1, y1], fill=(16, 54, 84))
    r = 46
    while r > 0:
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                 fill=WHITE, width=6)
        r -= 8
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=GOLD)
    draw_wrapped(
        draw, 710, y1 + 8,
        "A severe cyclonic storm gathers in the Bay of Bengal, heading for "
        "India's Andhra coast.",
        F(REG, 19), 270, 24,
    )


def also_strip(draw):
    draw.rectangle([0, 934, W, 972], fill=NAVY)
    draw.text((24, 943), "ALSO:", font=F(BOLD, 21), fill=GOLD)
    items = ["Quad in Manila", "Dhoni ends IPL career",
             "Amazon $7bn for India", "Ebola tops 11,000 cases"]
    fnt = F(REG, 19)
    text = " \u00b7 ".join(items)
    while items and draw.textlength(text, font=fnt) > 904:
        items = items[:-1]
        text = " \u00b7 ".join(items)
    draw.text((96, 944), text, font=fnt, fill=WHITE)


def footer(draw):
    draw.text((24, 980),
              "Sources: Reuters, AP, CNN  \u00b7  Images drawn for this page",
              font=F(REG, 17), fill=GRAY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    panel_markets(draw)
    panel_asia(draw)
    panel_gulf(draw)
    panel_ukraine(draw)
    panel_politics(draw)
    panel_weather(draw)
    also_strip(draw)
    footer(draw)
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
