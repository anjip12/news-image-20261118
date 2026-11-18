"""Render the 18 November 2026 world-news front page (1024x1024 PNG).

Pure Pillow drawing: flat vector-style panels, no network, deterministic.
Run: python3 gen.py  -> writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (16, 38, 66)
TEAL = (14, 94, 96)
GOLD = (176, 124, 24)
SLATE = (84, 96, 110)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    f = font(FONT_B, 20)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 26


def headline(draw, x, y, text, size, max_w, fill=INK):
    f = font(FONT_B, size)
    return para(draw, (x, y), text, f, fill, max_w, size + 6)


def sub(draw, x, y, text, size, max_w, fill=(52, 52, 52)):
    f = font(FONT_R, size)
    return para(draw, (x, y), text, f, fill, max_w, size + 5)


def panel(draw, box, fill, outline=INK, width=3):
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=outline, width=width)


def rule(draw, x, y, w, color=RED, h=4):
    draw.rectangle([x, y, x + w, y + h], fill=color)


def draw_masthead(d):
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((32, 18), "THE WORLD IN ONE DAY", font=font(FONT_B, 58),
           fill=WHITE)
    d.text((32, 88), "WEDNESDAY  \u00b7  18 NOVEMBER 2026",
           font=font(FONT_B, 34), fill=(255, 214, 90))
    d.rectangle([0, 148, W, 154], fill=RED)


def draw_bridge_scene(d, x, y, w, h):
    """Broken road bridge over a strait: sea, deck, collapsed arch."""
    sea = (44, 96, 140)
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    d.rectangle([x, y + h - 78, x + w, y + h], fill=sea)
    # sun and smoke
    d.ellipse([x + w - 110, y + 14, x + w - 46, y + 78], fill=(255, 196, 66))
    for cx, cy, r in [(x + 150, y + 40, 26), (x + 185, y + 26, 34),
                      (x + 225, y + 42, 24)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # bridge deck, left span standing, right span dropped
    deck_y = y + h - 118
    d.rectangle([x, deck_y, x + 250, deck_y + 14], fill=(70, 70, 70))
    d.polygon([(x + 250, deck_y), (x + 330, deck_y + 62),
               (x + 330, deck_y + 76), (x + 250, deck_y + 14)],
              fill=(70, 70, 70))
    # fallen arch in the water
    d.arc([x + 300, deck_y - 10, x + 430, deck_y + 110], start=200,
          end=340, fill=(50, 50, 50), width=10)
    # support pillars
    for px in (x + 40, x + 200):
        d.rectangle([px, deck_y + 14, px + 16, y + h - 78], fill=(90, 90, 90))
    # waves
    for wx in range(x + 8, x + w - 20, 46):
        d.arc([wx, y + h - 46, wx + 34, y + h - 22], start=180,
              end=360, fill=WHITE, width=3)


def draw_quad_scene(d, x, y, w, h):
    """Four flag chips for the Quad: US, Japan, India, Australia."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    chips = [((178, 34, 34), "USA"), ((255, 255, 255), "JAPAN"),
             ((255, 153, 51), "INDIA"), ((0, 82, 165), "AUSTRALIA")]
    cw = (w - 40) // 4
    for i, (col, name) in enumerate(chips):
        cx = x + 12 + i * cw
        d.rounded_rectangle([cx, y + 4, cx + cw - 10, y + 34], radius=8,
                            fill=col, outline=INK, width=2)
        d.text((cx + 4, y + 38), name, font=font(FONT_B, 13), fill=INK)


def draw_drone_scene(d, x, y, w, h):
    """Radar dome under a night sky, drone silhouettes above."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 48))
    for sx, sy in [(x + 20, y + 18), (x + 90, y + 40), (x + 200, y + 14),
                   (x + 280, y + 44), (x + 340, y + 22)]:
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=WHITE)
    # radar dome and mast
    cx = x + w // 2
    d.pieslice([cx - 30, y + h - 36, cx + 30, y + h - 6],
               start=180, end=360, fill=(200, 200, 210))
    d.rectangle([cx - 3, y + 16, cx + 3, y + h - 36],
                fill=(160, 160, 170))
    d.arc([cx - 22, y + 6, cx + 22, y + 34], start=180,
          end=360, fill=(255, 214, 90), width=3)
    # drones
    for dx, dy in [(x + 36, y + 10), (x + 244, y + 20)]:
        d.ellipse([dx, dy, dx + 22, dy + 8], fill=(140, 140, 150))
        d.rectangle([dx - 6, dy + 2, dx + 28, dy + 5], fill=(140, 140, 150))


def draw_cyclone_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 64, 92))
    cx, cy = x + w // 2, y + h // 2
    for r, col in [(40, (255, 255, 255)), (30, (160, 210, 230)),
                   (20, (255, 255, 255)), (10, (255, 214, 90))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=col, width=6)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 214, 90))


def draw_cricket_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 112, 54))
    # pitch and stumps
    d.rectangle([x + w // 2 - 26, y + 20, x + w // 2 + 26, y + h - 20],
                fill=(214, 190, 140))
    for sx in (x + w // 2 - 14, x + w // 2, x + w // 2 + 14):
        d.rectangle([sx - 3, y + 26, sx + 3, y + 52], fill=(255, 214, 90))
    # bat and red ball
    d.polygon([(x + 60, y + 40), (x + 78, y + 30), (x + 108, y + 84),
               (x + 92, y + 94)], fill=(160, 110, 60))
    d.ellipse([x + w - 62, y + 30, x + w - 26, y + 66], fill=(178, 34, 34))
    d.text((x + 12, y + 10), "No. 7",
           font=font(FONT_B, 17), fill=WHITE)


def draw_solar_scene(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 244, 200))
    d.ellipse([x + w - 74, y + 10, x + w - 18, y + 66], fill=(255, 196, 66))
    for i in range(3):
        px = x + 16 + i * 96
        d.polygon([(px, y + h - 14), (px + 84, y + h - 14),
                   (px + 72, y + h - 52), (px + 12, y + h - 52)],
                  fill=(16, 62, 120), outline=WHITE)
        d.line([px + 42, y + h - 14, px + 42, y + h - 52], fill=WHITE,
               width=2)
    d.text((x + 12, y + 10), "$7 BILLION",
           font=font(FONT_B, 24), fill=(16, 62, 120))


def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)

    # --- hero: Crimea bridge, left 2/3 ---
    panel(d, (24, 172, 648, 560), (255, 255, 255))
    y = 188
    y = kicker(d, 40, y, "War in Ukraine", RED)
    y = headline(d, 40, y, "UKRAINE BRINGS DOWN THE CRIMEA BRIDGE", 38, 592)
    y = sub(d, 40, y + 4,
            "A road arch of the 19-km Kerch bridge collapses into the "
            "strait on the second day of strikes. Russia answers by "
            "hitting Kyiv\u2019s two Dnipro bridges.", 21, 592)
    draw_bridge_scene(d, 40, y + 10, 592, 544 - (y + 10))

    # --- right column: Quad, then Iran ---
    panel(d, (668, 172, 1000, 356), (255, 255, 255))
    y = 188
    y = kicker(d, 684, y, "Asia diplomacy", NAVY)
    y = headline(d, 684, y, "TRUMP IN MANILA FOR THE QUAD", 25, 300)
    draw_quad_scene(d, 684, y + 6, 300, 340 - (y + 6))

    panel(d, (668, 376, 1000, 560), (255, 255, 255))
    y = 392
    y = kicker(d, 684, y, "Gulf tensions", TEAL)
    y = headline(d, 684, y, "IRAN HITS U.S. RADAR IN BAHRAIN", 25, 300)
    draw_drone_scene(d, 684, y + 6, 300, 544 - (y + 6))

    # --- bottom row: three stories ---
    bw, gap = 312, 20
    panels = [
        (24, "Weather", "CYCLONE AKVAN BUILDS",
         "A severe cyclonic storm gathers in the Bay of Bengal; "
         "India on alert.", draw_cyclone_scene),
        (356, "Sport", "DHONI CALLS TIME ON THE IPL",
         "MS Dhoni ends his playing career and becomes Chennai "
         "Super Kings\u2019 mentor.", draw_cricket_scene),
        (688, "Business", "AMAZON BETS $7BN ON INDIA",
         "A $7 billion renewable-energy investment in India "
         "by 2030.", draw_solar_scene),
    ]
    for x, kick, head, txt, scene in panels:
        panel(d, (x, 580, x + bw, 876), (255, 255, 255))
        y = 596
        y = kicker(d, x + 16, y, kick, GOLD)
        y = headline(d, x + 16, y, head, 24, bw - 32)
        scene(d, x + 16, y + 6, bw - 32, 92)
        sub(d, x + 16, y + 106, txt, 18, bw - 32)

    # --- ticker: also in the news ---
    d.rectangle([0, 896, W, 964], fill=NAVY)
    d.text((24, 912), "ALSO:", font=font(FONT_B, 24), fill=(255, 214, 90))
    tick = ("India win a 10th SAFF title  \u00b7  "
            "UK and Australia sanction firms  \u00b7  "
            "Baidu warns of an AI bubble")
    tf = font(FONT_R, 17)
    trimmed = False
    while d.textlength(tick, font=tf) > W - 120 - 24 and " " in tick:
        tick = tick[:tick.rfind(" ")].rstrip()
        trimmed = True
    if trimmed:
        tick = tick + " \u2026"
    d.text((120, 916), tick, font=tf, fill=WHITE)
    d.text((24, 978), "Sources: Reuters, AP, CNN  \u00b7  Images drawn for this page",
           font=font(FONT_R, 16), fill=SLATE)
    return img


if __name__ == "__main__":
    img = compose()
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)
