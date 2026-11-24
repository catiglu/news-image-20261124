#!/usr/bin/env python3
"""Deterministic world-news poster for the make.fun `news-image-20261124` bounty.

Renders a newspaper-style 1024x1024 PNG that sums up the world news of
Tuesday 24 November 2026. No network, no randomness, no timestamps: the same
script always produces a byte-identical image.

Run:  python make_image.py   # writes entry.png next to this file
"""
import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
PAPER = (246, 241, 231)        # warm newsprint
CARD = (255, 253, 247)         # card face
INK = (26, 26, 34)             # headline ink
SUB = (64, 60, 52)             # sub-headline grey (darkened for legibility)
RULE = (176, 166, 146)         # hairline rules
BORDER = (216, 208, 189)       # card border

FIELD_COLORS = {
    "WAR":      (163, 22, 33),
    "DISASTER": (193, 68, 14),
    "CRIME":    (91, 42, 134),
    "TECH":     (29, 78, 137),
    "AFRICA":   (15, 107, 92),
    "MIDEAST":  (122, 31, 43),
    "CLIMATE":  (46, 107, 52),
    "CULTURE":  (142, 42, 91),
}

# ------------------------------------------------------------------ fonts ---
FONT_DIR = r"C:\Windows\Fonts"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


# ------------------------------------------------------------------ data ----
# Headline facts cross-checked against BBC World, The Guardian, NYT World and
# Sky News RSS feeds for 23-24 November 2026.
LEAD = {
    "tag": "WAR · MEDITERRANEAN",
    "headline": "Ukrainian naval drones sink Russian warship off Libya",
    "sub": "Kyiv confirms strikes on two Russian vessels; a third sinks in Benghazi",
    "context": (
        "Maritime trackers report a large fire at the port; Russia says it is "
        "assessing the damage."),
}

CARDS = [
    ("DISASTER · ASIA", "Three dead, dozens missing as Indonesian candy factory burns",
     "search continues three days after the blaze"),
    ("CRIME · AMERICAS", "Mexican troops attacked after drug lord's arrest",
     "shoot-out follows capture on FBI's ten most-wanted list"),
    ("TECH · ASIA", "South Korea minister quits over AI exam cheating",
     "university exams engulfed in the scandal"),
    ("TECH · US", "US to blacklist AI chip firm Megaspeed",
     "after the Nvidia supply scandal"),
    ("AFRICA · DISASTER", "Nigeria boat capsizes: 24 dead",
     "vessel was carrying mourners to a funeral"),
    ("MIDEAST · IRAN", "Iran flogs singer over hijab performance",
     "lawyers say authorities went too far"),
    ("CLIMATE · WORLD", "COP31 ends without a deal",
     "analysts point to 'a divided world'"),
    ("CULTURE · US", "Miley Cyrus marries Maxx Morando",
     "ceremony in California"),
]

SOURCES = ("Sources: BBC World · The Guardian · NYT World · Sky News  |  "
           "23-24 November 2026")

W = H = 1024


# --------------------------------------------------------------- helpers ----
def wrap(draw, text, fnt, max_w):
    """Greedy word-wrap to max_w; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def chip(draw, x, y, label, color):
    """Small rounded tag chip; returns right edge x."""
    f = font("arialbd.ttf", 15)
    pad_x, pad_y = 8, 4
    tw = draw.textlength(label, font=f)
    th = f.size
    w = tw + 2 * pad_x
    h = th + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h / 2, fill=color)
    draw.text((x + pad_x, y + pad_y - 1), label, font=f, fill=(255, 255, 255))
    return x + w


# ----------------------------------------------------------------- render ---
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    y = 34
    f_kicker = font("arialbd.ttf", 17)
    draw_centered(d, W / 2, y, "T H E   W O R L D   I N   O N E   D A Y", f_kicker, SUB)
    y += 30
    f_date = font("georgiab.ttf", 52)
    draw_centered(d, W / 2, y, "24 November 2026", f_date, INK)
    y += 66
    f_day = font("arialbd.ttf", 20)
    draw_centered(d, W / 2, y, "T U E S D A Y", f_day, SUB)
    y += 34
    d.line([(48, y), (W - 48, y)], fill=INK, width=3)
    d.line([(48, y + 5), (W - 48, y + 5)], fill=INK, width=1)
    y += 22

    # ---- lead story ----
    lead_h = 170
    d.rounded_rectangle([48, y, W - 48, y + lead_h], radius=10, fill=CARD,
                        outline=BORDER, width=1)
    cx = chip(d, 68, y + 16, LEAD["tag"], FIELD_COLORS["WAR"])
    f_lead = font("georgiab.ttf", 32)
    lines = wrap(d, LEAD["headline"], f_lead, W - 48 - 68 - 40)
    ly = y + 46
    for ln in lines[:2]:
        d.text((68, ly), ln, font=f_lead, fill=INK)
        ly += 36
    f_sub = font("arial.ttf", 17)
    d.text((68, ly + 2), LEAD["sub"], font=f_sub, fill=SUB)
    f_ctx = font("ariali.ttf", 15)
    d.text((68, ly + 24), LEAD["context"], font=f_ctx, fill=SUB)
    y += lead_h + 18

    # ---- section header for the card grid ----
    margin = 48
    f_sec = font("arialbd.ttf", 16)
    d.text((margin, y), "THE DAY IN BRIEF", font=f_sec, fill=INK)
    sw = d.textlength("THE DAY IN BRIEF", font=f_sec)
    d.line([(margin + sw + 12, y + 9), (W - margin, y + 9)], fill=RULE, width=1)
    y += 28

    # ---- card grid: 2 cols x 4 rows ----
    gap = 16
    col_w = (W - 2 * margin - gap) / 2
    rows = 4
    card_h = (H - y - 96 - (rows - 1) * gap) / rows

    for i, (tag, head, sub) in enumerate(CARDS):
        r, c = divmod(i, 2)
        x0 = margin + c * (col_w + gap)
        y0 = y + r * (card_h + gap)
        d.rounded_rectangle([x0, y0, x0 + col_w, y0 + card_h], radius=10,
                            fill=CARD, outline=BORDER, width=1)
        field = tag.split(" ")[0]
        chip(d, x0 + 16, y0 + 12, tag, FIELD_COLORS.get(field, INK))
        f_head = font("georgiab.ttf", 22)
        hlines = wrap(d, head, f_head, col_w - 32)
        hy = y0 + 44
        for ln in hlines[:2]:
            d.text((x0 + 16, hy), ln, font=f_head, fill=INK)
            hy += 26
        f_sub2 = font("arial.ttf", 15)
        d.text((x0 + 16, hy + 2), sub, font=f_sub2, fill=SUB)

    # ---- also-in-the-news strip ----
    sy = y + rows * card_h + (rows - 1) * gap + 12
    f_lab = font("arialbd.ttf", 15)
    d.text((margin, sy), "ALSO:", font=f_lab, fill=INK)
    lw = d.textlength("ALSO:", font=f_lab)
    f_b = font("arial.ttf", 15)
    line1 = ("India pledges $1.6bn to Nepal in reset of ties  ·  "
             "South Korea's education minister resigns over exam-cheating scandal")
    line2 = ("FBI reportedly investigating apparent hack of its criminal database  ·  "
             "Italy mourns jeweller Paolo Bulgari, dead at 89")
    d.text((margin + lw + 8, sy), line1, font=f_b, fill=SUB)
    d.text((margin, sy + 21), line2, font=f_b, fill=SUB)

    # ---- footer ----
    f_src = font("arial.ttf", 14)
    draw_centered(d, W / 2, H - 34, SOURCES, f_src, SUB)

    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {size} bytes "
          f"({size / 1024:.1f} KiB)")
    assert img.size == (1024, 1024), "must be 1024x1024"
    assert size <= 1024 * 1024, "must be <= 1 MiB"


if __name__ == "__main__":
    main()
