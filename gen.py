#!/usr/bin/env python3
"""Draw the front page for Wednesday 18 November 2026.

A single 1024x1024 PNG that sums up the day's world news: masthead,
one lead markets story, two diplomacy stories, three smaller stories
and an also-strip. Everything is drawn with Pillow shapes and text;
no network, no photographs, no downloaded assets. Running this file
twice writes byte-identical output.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (20, 38, 63)
NAVY2 = (28, 52, 84)
INK = (24, 24, 24)
RED = (178, 34, 34)
GOLD = (242, 201, 76)
TEAL = (15, 118, 110)
BROWN = (146, 96, 20)
BLUE = (31, 93, 176)
SKY = (198, 224, 240)
SEA = (38, 84, 138)
CARD = (255, 255, 255)
GREY = (96, 96, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = "DejaVuSans-Bold.ttf"
PLAIN = "DejaVuSans.ttf"

F_TITLE = load(BOLD, 62)
F_DATE = load(BOLD, 33)
F_KICK = load(BOLD, 22)
F_HEAD = load(BOLD, 40)
F_BODY = load(PLAIN, 21)
F_BODY_SM = load(PLAIN, 19)
F_ALSO = load(BOLD, 21)
F_ALSO_TXT = load(PLAIN, 19)
F_FOOT = load(PLAIN, 17)
F_NUM = load(BOLD, 22)
F_LAB = load(BOLD, 15)


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, leading, fill=INK):
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def card(draw, box):
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=INK, width=2)


def headline(draw, x, y, text, width, size=30, max_lines=2, fill=INK):
    """Fit a headline in at most max_lines, shrinking the font if needed."""
    size_now = size
    while size_now > 22:
        fnt = load(BOLD, size_now)
        if len(wrap(draw, text, fnt, width)) <= max_lines:
            break
        size_now -= 2
    fnt = load(BOLD, size_now)
    for line in wrap(draw, text, fnt, width)[:max_lines]:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += size_now + 6
    return y


def bars(draw, x0, base, values, labels, colors):
    top = max(values)
    for i, value in enumerate(values):
        height = int(108 * value / top)
        x = x0 + i * 185
        draw.rectangle([x, base - height, x + 118, base], fill=colors[i])
        tag = "$%dbn" % value
        tw = draw.textlength(tag, font=F_NUM)
        draw.text((x + (118 - tw) / 2, base - height - 30), tag, font=F_NUM, fill=INK)
        lw = draw.textlength(labels[i], font=F_LAB)
        draw.text((x + (118 - lw) / 2, base + 10), labels[i], font=F_LAB, fill=GREY)
    draw.line([x0 - 16, base, x0 + 3 * 185 - 30, base], fill=INK, width=3)


def bridge(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    draw.ellipse([x1 - 78, y0 + 12, x1 - 28, y0 + 62], fill=GOLD)
    mid = (y0 + y1) // 2
    draw.rectangle([x0, mid, x1, y1], fill=SEA)
    draw.line([x0, mid - 26, x0 + 92, mid - 26], fill=(70, 70, 70), width=10)
    draw.line([x0 + 150, mid - 26, x1, mid - 26], fill=(70, 70, 70), width=10)
    draw.line([x0 + 92, mid - 26, x0 + 122, mid + 6], fill=(70, 70, 70), width=10)
    draw.arc([x0 + 108, mid - 78, x0 + 208, mid + 22], start=200, end=340, fill=(70, 70, 70), width=8)
    draw.arc([x0 + 168, mid - 78, x1 - 8, mid + 22], start=200, end=340, fill=(70, 70, 70), width=8)
    for cx in range(x0 + 8, x1 - 8, 34):
        draw.arc([cx, mid + 16, cx + 30, mid + 44], start=180, end=360, fill=(255, 255, 255), width=3)


def spiral(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 54, 84))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in range(46, 8, -8):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=(255, 255, 255), width=6)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=GOLD)


def senate_bar(draw, x, y, w, h):
    blue_w = int(w * 0.56)
    draw.rectangle([x, y, x + blue_w, y + h], fill=BLUE)
    draw.rectangle([x + blue_w, y, x + w, y + h], fill=RED)
    draw.text((x + 12, y + h // 2 - 13), "56 DEM", font=F_NUM, fill=(255, 255, 255))
    draw.text((x + blue_w + 12, y + h // 2 - 13), "44 GOP", font=F_NUM, fill=(255, 255, 255))


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 116], fill=NAVY)
    draw.text((24, 12), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(255, 255, 255))
    draw.text((26, 74), "WEDNESDAY  \u00b7  18 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    draw.rectangle([0, 116, W, 124], fill=RED)

    # Lead: Nvidia.
    card(draw, (24, 140, 636, 556))
    draw.text((44, 158), "MARKETS", font=F_KICK, fill=RED)
    y = headline(draw, 44, 190, "NVIDIA BEATS BIG: $115.8BN QUARTER", 572, size=40, max_lines=2)
    y = para(draw, 44, y + 10, "Revenue doubles to $115.8bn, up 103%, and Nvidia guides $130bn next quarter \u2014 its first report since Jensen Huang quit. Shares jump after hours.", F_BODY, 572, 28)
    bars(draw, 70, 520, [57, 96, 116], ["A YEAR AGO", "LAST QTR", "THIS QTR"], [(150, 180, 215), (80, 130, 195), (20, 60, 120)])

    # Right top: APEC opens in Shenzhen.
    card(draw, (652, 140, 1000, 344))
    draw.text((672, 158), "ASIA DIPLOMACY", font=F_KICK, fill=NAVY2)
    y = headline(draw, 672, 190, "APEC OPENS IN SHENZHEN", 308, size=30, max_lines=2)
    para(draw, 672, y + 8, "Xi urges open trade; Putin takes the stage. First Trump\u2013Xi\u2013Putin talks set for Thursday.", F_BODY_SM, 308, 25)

    # Right bottom: Gulf escalation.
    card(draw, (652, 360, 1000, 556))
    draw.text((672, 378), "GULF TENSIONS", font=F_KICK, fill=TEAL)
    y = headline(draw, 672, 406, "IRAN HITS KUWAIT AND BAHRAIN", 308, size=30, max_lines=2)
    para(draw, 672, y + 6, "Tehran fires drones at U.S. bases after American jets hit a missile site on Qeshm Island.", F_BODY_SM, 308, 25)

    # Bottom left: Crimea bridge.
    card(draw, (24, 572, 333, 920))
    draw.text((44, 590), "WAR IN UKRAINE", font=F_KICK, fill=RED)
    y = headline(draw, 44, 622, "CRIMEA BRIDGE DOWN", 269, size=30, max_lines=2)
    bridge(draw, (44, y + 10, 313, y + 118))
    para(draw, 44, y + 130, "A road arch of the 19-km Kerch bridge collapses into the strait on the second day of strikes.", F_BODY_SM, 269, 24)

    # Bottom middle: U.S. Senate.
    card(draw, (357, 572, 666, 920))
    draw.text((377, 590), "U.S. POLITICS", font=F_KICK, fill=NAVY2)
    y = headline(draw, 377, 622, "DEMOCRATS TAKE THE SENATE", 269, size=30, max_lines=2)
    senate_bar(draw, 377, y + 12, 269, 52)
    draw.text((377, y + 72), "INCOMING SENATE \u00b7 100 SEATS", font=F_LAB, fill=GREY)
    para(draw, 377, y + 96, "Mary Peltola wins Alaska, giving Democrats a 56\u201344 majority in the incoming Senate.", F_BODY_SM, 269, 24)

    # Bottom right: Cyclone Akvan.
    card(draw, (690, 572, 1000, 920))
    draw.text((710, 590), "WEATHER", font=F_KICK, fill=BROWN)
    y = headline(draw, 710, 622, "CYCLONE AKVAN BUILDS", 270, size=30, max_lines=2)
    spiral(draw, (710, y + 10, 980, y + 118))
    para(draw, 710, y + 130, "A severe cyclonic storm gathers in the Bay of Bengal, heading for India's Andhra coast.", F_BODY_SM, 270, 24)

    # Also strip and footer.
    draw.rectangle([0, 934, W, 972], fill=NAVY)
    draw.text((24, 943), "ALSO:", font=F_ALSO, fill=GOLD)
    also = "Quad in Manila \u00b7 Dhoni ends IPL career \u00b7 Amazon $7bn for India \u00b7 Ebola tops 11,000 cases"
    if draw.textlength(also, font=F_ALSO_TXT) > 904:
        also = "Quad in Manila \u00b7 Dhoni ends IPL career \u00b7 Amazon $7bn for India"
    draw.text((96, 944), also, font=F_ALSO_TXT, fill=(255, 255, 255))
    draw.text((24, 980), "Sources: Reuters, AP, CNN  \u00b7  Images drawn for this page", font=F_FOOT, fill=GREY)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    draw_page().save(os.path.join(here, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
