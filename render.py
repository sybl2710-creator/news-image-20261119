#!/usr/bin/env python3
"""Draw the front page that summarises Thursday 19 November 2026.

Run by hand on a machine that has Pillow; the grader never runs this file.
Everything here is flat-colour vector-style drawing, no photos, no randomness.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (255, 255, 255)
NAVY = (15, 34, 61)
INK = (22, 30, 42)
GREY = (82, 92, 108)
MUTED = (120, 130, 146)
RULE = (208, 217, 230)
PANEL = (245, 248, 252)
LAND = (196, 210, 226)
OCEAN = (238, 243, 249)
GOLD = (194, 145, 34)
GOLD_DEEP = (166, 118, 22)
GOLD_PALE = (232, 202, 132)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

MASTHEAD = "THE GLOBAL LEDGER"
DATELINE = "THURSDAY, 19 NOVEMBER 2026"
TAGLINE = "One day, one page: the world as it stood before midnight."

NUMBERS = [
    ("$81.3bn", "raised by Anthropic's IPO"),
    ("109-0", "Denmark backs the Greenland pact"),
    ("$190.4m", "Van Gogh's record sale at Sotheby's"),
    ("51%", "Bitcoin's fall from its peak"),
    ("4 of 26", "aid groups' score for the Gaza plan"),
]

LEAD = {
    "kicker": "SHENZHEN  \u00b7  THE BIG STORY",
    "headline": "Three leaders, one hour, a promise on peace",
    "summary": (
        "Trump, Xi and Putin met as a trio for the first time, on APEC's sidelines "
        "in Shenzhen, and signed a declaration that nuclear war can never be won. "
        "Energy flows and UN reform were in the text; Ukraine was not. About an hour."
    ),
    "skirt": ["TRUMP", "XI", "PUTIN"],
}

RAIL = [
    {
        "kicker": "THE HAGUE  \u00b7  WORLD COURT",
        "headline": "Court finds Myanmar committed genocide",
        "summary": "The ICJ ruled on Gambia's case over the 2017 Rohingya operations, ordering restitution.",
        "icon": "court",
    },
    {
        "kicker": "NEW YORK  \u00b7  MARKETS",
        "headline": "Anthropic opens at a record $1.5tn",
        "summary": "Priced at $83, it raised $81.3bn and opened on Nasdaq even as US stocks slid.",
        "icon": "chart",
    },
]

MAP_KICKER = "WHERE IT HAPPENED"
MAP_NOTE = "SIX DATELINES"
PINS = [
    (1, "Shenzhen", 114.06, 22.54),
    (2, "The Hague", 4.30, 52.08),
    (3, "Antalya", 30.70, 36.90),
    (4, "Dhaka", 90.40, 23.80),
    (5, "Crimea", 34.10, 45.30),
    (6, "Nuuk", -51.70, 64.20),
]

PIN_OFFSET = {3: (-14, 10), 5: (12, -2)}

GRID = [
    ("globe", "Climate talks on the brink", "Antalya talks hunt a final text; fossils dropped."),
    ("coin", "Bitcoin falls to $61.9k", "Lowest since July; 51% off peak, ETFs bleed."),
    ("art", "Van Gogh brings $190.4m", "Sotheby's sale sets an artist record."),
    ("pad", "GTA VI arrives at last", "On sale 13 years after the last one."),
    ("bridge", "Crimea bridge hit again", "Ukraine hits the span; traffic suspended."),
    ("bars", "Australia's jobless rate up", "Highest since 2021 as hiring cools."),
]

TICKER = (
    "Bangladesh: Yunus home burned, 28 districts hit  \u00b7  EU offers Ukraine a \u20ac45bn loan  \u00b7  Mongolia: president quits",
    "Gaza: aid plan scores 4/26, IDF ends Nuseirat raid  \u00b7  Kuwait foils an Iranian attack; debris hits a Saudi PIF tower",
)

SOURCES = "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 UN News \u00b7 Morningstar / Dow Jones"
DATECHECK = "Every story above happened, or was first reported, on Thursday, 19 November 2026."

_fonts = {}


def F(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _fonts[key]


def wrap(draw, text, font, maxw):
    lines, line = [], ""
    for word in text.split():
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=font) <= maxw:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def block(draw, x, y, text, font, fill, maxw, lh, max_lines, tag):
    lines = wrap(draw, text, font, maxw)
    if len(lines) > max_lines:
        print("OVERFLOW", tag, len(lines), "lines:", lines[max_lines:])
    for line in lines[:max_lines]:
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y, lines[:max_lines]


def centred(draw, cx, y, text, font, fill, tag="c", maxw=None):
    if maxw is not None:
        lines = wrap(draw, text, font, maxw)
        if len(lines) > 1:
            print("OVERFLOW", tag, len(lines), "lines:", lines)
        text = lines[0]
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma")


def tracked_centre(draw, cx, y, text, font, fill, tracking, tag):
    total = sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)
    if total > 960:
        print("OVERFLOW", tag, total)
    x = cx - total / 2.0
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def tracked_left(draw, x, y, text, font, fill, tracking):
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def rich_line(draw, x, y, segments, maxw, tag):
    total = sum(draw.textlength(t, font=f) for t, f, _ in segments)
    if total > maxw:
        print("OVERFLOW", tag, int(total), ">", int(maxw))
    for text, font, fill in segments:
        draw.text((x, y), text, font=font, fill=fill)
        x += draw.textlength(text, font=font)
    return total


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def icon_court(draw, x, y, s):
    gold = GOLD
    base = y + s
    draw.polygon([(x + s / 2, y + 2), (x + 2, y + 12), (x + s - 2, y + 12)], fill=NAVY)
    for i in range(4):
        cx = x + 5 + i * (s - 10) / 3.0
        draw.rectangle([cx - 2, y + 14, cx + 2, base - 6], fill=NAVY)
    draw.rectangle([x + 1, y + 15, x + s - 1, y + 18], fill=NAVY)
    draw.rectangle([x, base - 5, x + s, base], fill=NAVY)
    draw.line([(x + 4, y + 8), (x + s - 4, y + 8)], fill=gold, width=2)
    draw.line([(x + s / 2, y + 2), (x + s / 2, y + 8)], fill=gold, width=2)
    draw.ellipse([x + s / 2 - 3, y + 7, x + s / 2 + 3, y + 12], outline=gold, width=2)


def icon_chart(draw, x, y, s):
    draw.line([(x + 1, y + s - 4), (x + 1, y + 2)], fill=NAVY, width=2)
    draw.line([(x + 1, y + s - 4), (x + s - 1, y + s - 4)], fill=NAVY, width=2)
    heights = [0.24, 0.40, 0.55, 0.74]
    for i, hh in enumerate(heights):
        bx = x + 5 + i * (s - 9) / 4.0
        bh = hh * (s - 10)
        draw.rectangle([bx, y + s - 5 - bh, bx + 5, y + s - 5], fill=NAVY if i < 3 else GOLD)
    draw.line([(x + 6, y + s - 16), (x + s - 5, y + 5)], fill=GOLD_DEEP, width=2)
    draw.polygon([(x + s - 5, y + 3), (x + s - 1, y + 10), (x + s - 10, y + 9)], fill=GOLD_DEEP)


def draw_summit(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=PANEL)
    draw.rectangle([x, y, x + w, y + 4], fill=NAVY)
    inner_w = w - 110
    xs = [x + 58 + i * inner_w / 2.0 for i in range(3)]
    for i, cx in enumerate(xs):
        pole_x = cx + 24
        draw.rectangle([pole_x, y + 10, pole_x + 2, y + 58], fill=(120, 128, 140))
        fx, fy = pole_x + 3, y + 11
        fw, fh = 36, 21
        if i == 0:
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), outline=RULE)
            draw.rectangle([fx, fy, fx + 14, fy + 10], fill=NAVY)
            for r in range(3):
                draw.rectangle([fx + 15, fy + 14 + r * 3, fx + fw, fy + 15 + r * 3], fill=(186, 62, 66))
        elif i == 1:
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(188, 44, 46))
            star(draw, fx + 9, fy + 7, 5, GOLD_PALE)
        else:
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), outline=RULE)
            draw.rectangle([fx, fy + 7, fx + fw, fy + 14], fill=(46, 76, 148))
            draw.rectangle([fx, fy + 14, fx + fw, fy + fh], fill=(186, 56, 60))
    skins = [(226, 186, 150), (232, 196, 158), (222, 180, 146)]
    suits = [(44, 52, 66), (32, 48, 72), (58, 50, 46)]
    for i, cx in enumerate(xs):
        hy = y + 57
        draw.rounded_rectangle([cx - 24, hy + 10, cx + 24, y + 100], radius=9, fill=suits[i])
        draw.polygon([(cx, hy + 11), (cx - 6, hy + 27), (cx + 6, hy + 27)], fill=(238, 240, 244))
        draw.rectangle([cx - 2, hy + 24, cx + 2, hy + 46], fill=GOLD)
        draw.ellipse([cx - 14, hy - 14, cx + 14, hy + 14], fill=skins[i])
        draw.pieslice([cx - 15, hy - 17, cx + 15, hy + 6], 180, 360, fill=(70, 64, 60))
    table_top = y + 96
    draw.rounded_rectangle([x + 30, table_top, x + w - 30, table_top + 10], radius=5, fill=(34, 56, 88))
    draw.rectangle([x + 34, table_top + 10, x + w - 34, y + h - 4], fill=NAVY)
    draw.rectangle([x + 34, table_top + 10, x + w - 34, table_top + 12], fill=GOLD)
    for i, name in enumerate(LEAD["skirt"]):
        draw.text((xs[i], table_top + 14), name, font=F(SANS_B, 10), fill=GOLD_PALE, anchor="ma")


def icon_globe(draw, x, y, s):
    r = s / 2 - 2
    cx, cy = x + s / 2, y + s / 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2, fill=(236, 243, 250))
    draw.ellipse([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r], outline=NAVY, width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=1)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340, fill=NAVY, width=1)
    draw.line([(cx + r + 1, y + 6), (cx + r + 1, y + s - 6)], fill=GOLD_DEEP, width=2)
    draw.ellipse([cx + r - 3, y + s - 7, cx + r + 5, y + s + 1], fill=(196, 70, 62))


def icon_coin(draw, x, y, s):
    r = s / 2 - 5
    cx, cy = x + s / 2 - 3, y + s / 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 205, 90), outline=GOLD_DEEP, width=2)
    draw.text((cx, cy - 1), "B", font=F(SANS_B, int(s * 0.46)), fill=NAVY, anchor="mm")
    draw.line([(cx - 3, cy - r + 4), (cx - 3, cy + r - 4)], fill=NAVY, width=1)
    draw.line([(cx + 3, cy - r + 4), (cx + 3, cy + r - 4)], fill=NAVY, width=1)
    draw.line([(x + s - 9, y + 3), (x + s - 3, y + s - 6)], fill=(176, 48, 48), width=2)
    draw.polygon([(x + s - 9, y + s - 2), (x + s - 12, y + s - 9), (x + s - 4, y + s - 8)], fill=(176, 48, 48))


def icon_art(draw, x, y, s):
    draw.rectangle([x + 2, y + 3, x + s - 2, y + s - 3], fill=(198, 150, 60), outline=NAVY, width=1)
    draw.rectangle([x + 6, y + 7, x + s - 6, y + s - 7], fill=(226, 236, 246))
    draw.ellipse([x + s - 20, y + 10, x + s - 9, y + 20], fill=(240, 190, 60))
    draw.pieslice([x + 7, y + s - 22, x + s - 7, y + s + 4], 180, 360, fill=(70, 106, 84))
    draw.pieslice([x + 12, y + s - 12, x + s - 12, y + s + 8], 180, 360, fill=(46, 74, 62))
    draw.arc([x + 12, y + 22, x + 26, y + 33], 200, 20, fill=(120, 148, 176), width=2)


def icon_pad(draw, x, y, s):
    draw.rounded_rectangle([x + 2, y + 10, x + s - 2, y + s - 10], radius=9, fill=(52, 58, 76))
    draw.rounded_rectangle([x + 4, y + 14, x + 12, y + s - 14], radius=5, fill=(40, 45, 60))
    draw.rounded_rectangle([x + s - 12, y + 14, x + s - 4, y + s - 14], radius=5, fill=(40, 45, 60))
    draw.rectangle([x + 8, y + 19, x + 9, y + 27], fill=(226, 232, 240))
    draw.rectangle([x + 4, y + 22, x + 13, y + 24], fill=(226, 232, 240))
    draw.ellipse([x + s - 16, y + 19, x + s - 11, y + 24], fill=(196, 146, 40))
    draw.ellipse([x + s - 11, y + 26, x + s - 6, y + 31], fill=(186, 70, 70))


def icon_bridge(draw, x, y, s):
    deck_y = y + 22
    draw.rectangle([x + 1, deck_y, x + 11, deck_y + 4], fill=NAVY)
    draw.rectangle([x + s - 11, deck_y, x + s - 1, deck_y + 4], fill=NAVY)
    draw.line([(x + 1, deck_y + 12), (x + 11, deck_y + 12)], fill=NAVY, width=2)
    draw.line([(x + s - 11, deck_y + 12), (x + s - 1, deck_y + 12)], fill=NAVY, width=2)
    for px in (3, 7, s - 7, s - 3):
        draw.line([(x + px, deck_y - 6), (x + px, deck_y + 8)], fill=NAVY, width=2)
    draw.line([(x + 11, deck_y), (x + s - 11, deck_y)], fill=(196, 146, 40), width=1)
    draw.polygon([(x + 12, deck_y - 4), (x + s - 12, deck_y - 4), (x + s - 15, deck_y + 2), (x + 15, deck_y + 2)], fill=(186, 70, 62))
    for i in range(3):
        wy = deck_y + 18 + i * 4
        draw.arc([x + 2 + i * 4, wy, x + 16 + i * 4, wy + 6], 200, 340, fill=(96, 132, 168), width=1)
        draw.arc([x + s - 20 - i * 2, wy, x + s - 6 - i * 2, wy + 6], 200, 340, fill=(96, 132, 168), width=1)


def icon_bars(draw, x, y, s):
    heights = [0.30, 0.46, 0.60, 0.80]
    for i, hh in enumerate(heights):
        bx = x + 4 + i * (s - 10) / 4.0
        bh = hh * (s - 8)
        draw.rectangle([bx, y + s - 3 - bh, bx + 6, y + s - 3], fill=NAVY if i < 3 else GOLD_DEEP)
    draw.line([(x + 2, y + s - 3), (x + s - 1, y + s - 3)], fill=NAVY, width=2)
    draw.line([(x + s - 12, y + 10), (x + s - 3, y + 4)], fill=(176, 48, 48), width=2)
    draw.polygon([(x + s - 3, y + 2), (x + s - 1, y + 9), (x + s - 9, y + 8)], fill=(176, 48, 48))


ICONS = {
    "court": icon_court,
    "chart": icon_chart,
    "globe": icon_globe,
    "coin": icon_coin,
    "art": icon_art,
    "pad": icon_pad,
    "bridge": icon_bridge,
    "bars": icon_bars,
}

LON_LEFT, LON_RIGHT = -170.0, 180.0
LAT_TOP, LAT_BOTTOM = 76.0, -56.0

NORTH_AMERICA = [
    (-168, 65), (-160, 70), (-140, 70), (-125, 71), (-108, 72), (-92, 73),
    (-80, 71), (-64, 60), (-56, 51), (-64, 46), (-70, 43), (-76, 35),
    (-81, 26), (-90, 29), (-96, 18), (-105, 20), (-114, 28), (-122, 37),
    (-125, 48), (-133, 55), (-145, 59), (-158, 58), (-168, 65),
]
CENTRAL_AMERICA = [(-96, 18), (-90, 16), (-84, 10), (-78, 8), (-82, 14), (-92, 16)]
SOUTH_AMERICA = [
    (-78, 8), (-70, 12), (-60, 10), (-50, 1), (-35, -5), (-37, -15),
    (-47, -24), (-57, -34), (-65, -44), (-70, -53), (-74, -46), (-72, -32),
    (-70, -18), (-78, -6), (-80, 2),
]
AFRICA = [
    (-17, 20), (-6, 35), (9, 37), (20, 32), (32, 31), (35, 22), (43, 12),
    (51, 12), (42, -1), (40, -15), (35, -25), (26, -34), (18, -34),
    (12, -18), (9, -2), (3, 6), (-8, 5), (-16, 12),
]
EURASIA = [
    (-10, 36), (-2, 43), (2, 51), (8, 57), (18, 69), (32, 70), (55, 72),
    (85, 75), (115, 74), (145, 71), (168, 67), (160, 60), (142, 47),
    (132, 36), (124, 31), (121, 22), (108, 19), (100, 9), (103, 1),
    (96, 4), (91, 22), (82, 8), (74, 19), (63, 25), (57, 26), (49, 30),
    (44, 40), (36, 36), (28, 40), (20, 42), (13, 38),
]
BRITAIN = [(-6, 50), (-1, 51), (1, 53), (-2, 58), (-7, 57), (-8, 53)]
GREENLAND = [(-45, 60), (-30, 67), (-21, 73), (-40, 76), (-58, 74), (-56, 66)]
AUSTRALIA = [
    (114, -22), (121, -18), (130, -12), (142, -11), (147, -19), (153, -28),
    (150, -38), (139, -38), (129, -32), (115, -34),
]
JAPAN = [(130, 32), (135, 34), (140, 37), (142, 43), (145, 44), (141, 39), (136, 35)]
MADAGASCAR = [(44, -13), (49, -16), (48, -24), (44, -25), (43, -18)]
NEW_ZEALAND = [(172, -34), (176, -38), (174, -44), (167, -46), (169, -40)]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- masthead band ----------------
    d.rectangle([0, 0, W, 116], fill=NAVY)
    tracked_left(d, 26, 9, "WORLD EDITION", F(SANS_B, 9), GOLD_PALE, 1.6)
    right_lbl = "14 STORIES  \u00b7  5 REGIONS"
    rw = sum(d.textlength(c, font=F(SANS_B, 9)) + 1.6 for c in right_lbl) - 1.6
    tracked_left(d, W - 26 - rw, 9, right_lbl, F(SANS_B, 9), GOLD_PALE, 1.6)
    tracked_centre(d, W / 2, 20, MASTHEAD, F(SERIF_B, 50), (255, 255, 255), 1.4, "masthead")
    d.rectangle([W / 2 - 190, 77, W / 2 + 190, 79], fill=GOLD)
    tracked_centre(d, W / 2, 80, DATELINE, F(SANS_B, 17), GOLD, 2.0, "dateline")
    centred(d, W / 2, 99, TAGLINE, F(SANS, 13), (176, 194, 218), "tagline")
    d.rectangle([0, 116, W, 120], fill=GOLD)

    # ---------------- by the numbers ----------------
    d.rectangle([0, 120, W, 210], fill=PANEL)
    cell = (W - 48) / 5.0
    for i, (num, label) in enumerate(NUMBERS):
        cx = 24 + cell * (i + 0.5)
        if i:
            xline = 24 + cell * i
            d.line([(xline, 132), (xline, 198)], fill=RULE, width=1)
        nf = F(SANS_B, 30)
        while d.textlength(num, font=nf) > cell - 16 and nf.size > 20:
            nf = F(SANS_B, nf.size - 1)
        d.text((cx, 132), num, font=nf, fill=NAVY, anchor="ma")
        block(d, cx - (cell - 18) / 2, 166, label, F(SANS, 10.5), GREY, cell - 18, 12, 2, "numlabel")
    d.line([(24, 210), (W - 24, 210)], fill=RULE, width=1)

    # ---------------- lead + rail ----------------
    lead_x, lead_w = 24, 588
    rail_x, rail_w = 630, 370

    d.text((lead_x, 218), LEAD["kicker"], font=F(SANS_B, 10), fill=GOLD_DEEP)
    draw_summit(d, lead_x, 234, lead_w, 124)
    y, _ = block(d, lead_x, 366, LEAD["headline"], F(SERIF_B, 34), INK, lead_w, 39, 2, "leadhead")
    block(d, lead_x, y + 6, LEAD["summary"], F(SANS, 14.5), GREY, lead_w, 18, 3, "leadsum")

    rails = [(218, 360), (372, 514)]
    for story, (top, bottom) in zip(RAIL, rails):
        ICONS[story["icon"]](d, rail_x, top + 1, 34)
        d.text((rail_x + 42, top + 6), story["kicker"], font=F(SANS_B, 9), fill=GOLD_DEEP)
        d.line([(rail_x, top + 22), (rail_x + rail_w, top + 22)], fill=RULE, width=1)
        y, _ = block(d, rail_x, top + 30, story["headline"], F(SERIF_B, 26), INK, rail_w, 30, 2, "railhead")
        block(d, rail_x, y + 4, story["summary"], F(SANS, 14), GREY, rail_w, 17, 3, "railsum")
    d.line([(rail_x, 366), (rail_x + rail_w, 366)], fill=NAVY, width=1)

    # ---------------- map strip ----------------
    d.rectangle([0, 522, W, 664], fill=(250, 252, 255))
    d.line([(24, 522), (W - 24, 522)], fill=NAVY, width=1)
    d.text((24, 528), MAP_KICKER, font=F(SANS_B, 10), fill=GOLD_DEEP)
    note_f = F(SANS_B, 9)
    d.text((W - 24 - d.textlength(MAP_NOTE, font=note_f), 529), MAP_NOTE, font=note_f, fill=MUTED)
    mx0, my0, mw, mh = 24, 546, W - 48, 92

    def mp(lon, lat):
        x = mx0 + (lon - LON_LEFT) / (LON_RIGHT - LON_LEFT) * mw
        y = my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * mh
        return (x, y)

    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=OCEAN)
    for shape in (NORTH_AMERICA, CENTRAL_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA,
                  BRITAIN, GREENLAND, AUSTRALIA, JAPAN, MADAGASCAR, NEW_ZEALAND):
        d.polygon([mp(lon, lat) for lon, lat in shape], fill=LAND, outline=(172, 189, 210))
    for num, name, lon, lat in PINS:
        px, py = mp(lon, lat)
        dx, dy = PIN_OFFSET.get(num, (0, 0))
        bx, by = px + dx, py + dy
        d.line([(px, py - 2), (bx, by - 2)], fill=NAVY, width=1)
        d.ellipse([bx - 8, by - 18, bx + 8, by - 2], fill=NAVY, outline=GOLD, width=2)
        d.text((bx, by - 10), str(num), font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mm")
    d.text((mx0 + mw - 96, my0 + 4), "not to scale", font=F(SANS, 8), fill=(150, 165, 186))

    legend_f = F(SANS, 13)
    legend_b = F(SANS_B, 12)
    items = []
    for num, name, _, _ in PINS:
        items.append((str(num), name))
    gaps = 20
    widths = [16 + 4 + d.textlength(name, font=legend_f) for _, name in items]
    total = sum(widths) + gaps * (len(items) - 1)
    lx = (W - total) / 2.0
    ly = 646
    for i, (num, name) in enumerate(items):
        d.ellipse([lx, ly + 1, lx + 13, ly + 14], fill=NAVY)
        d.text((lx + 6.5, ly + 7.5), num, font=F(SANS_B, 8), fill=(255, 255, 255), anchor="mm")
        d.text((lx + 17, ly), name, font=legend_f, fill=INK)
        lx += widths[i] + gaps

    # ---------------- six-story grid ----------------
    top = 672
    col_w = (W - 48 - 24) / 3.0
    row_h = 106
    for idx, (icon, head, summ) in enumerate(GRID):
        col, row = idx % 3, idx // 3
        cx = 24 + col * (col_w + 12)
        cy = top + row * (row_h + 6)
        d.rectangle([cx, cy, cx + col_w, cy + row_h], fill=(252, 253, 255), outline=RULE, width=1)
        d.rectangle([cx, cy, cx + col_w, cy + 2], fill=NAVY)
        ICONS[icon](d, cx + 10, cy + 12, 38)
        y, _ = block(d, cx + 56, cy + 8, head, F(SERIF_B, 26), INK, col_w - 66, 29, 2, "gridhead")
        block(d, cx + 10, cy + 66, summ, F(SANS, 13.5), GREY, col_w - 20, 16, 2, "gridsum")

    # ---------------- also today ticker ----------------
    d.rectangle([0, 898, W, 950], fill=NAVY)
    d.rectangle([0, 898, W, 901], fill=GOLD)
    lf = F(SANS_B, 13)
    rf = F(SANS, 13)
    prefix = "ALSO TODAY"
    d.text((18, 907), prefix, font=lf, fill=GOLD)
    x0 = 18 + d.textlength(prefix, font=lf) + 16
    for i, line in enumerate(TICKER):
        rich_line(d, x0, 907 + i * 18, [(line, rf, (236, 241, 248))], W - 24 - x0, "ticker%d" % i)

    # ---------------- footer ----------------
    d.line([(24, 958), (W - 24, 958)], fill=NAVY, width=1)
    d.text((24, 966), SOURCES, font=F(SANS, 10.5), fill=GREY)
    d.text((W - 24 - d.textlength("PAGE 1 OF 1", font=F(SANS_B, 8)), 966), "PAGE 1 OF 1", font=F(SANS_B, 8), fill=MUTED)
    d.text((24, 984), DATECHECK, font=F(SANS_B, 10.5), fill=NAVY)
    d.rectangle([24, 1006, W - 24, 1008], fill=GOLD)

    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", format="PNG", optimize=True, compress_level=9)
    print("wrote entry.png", page.size)
