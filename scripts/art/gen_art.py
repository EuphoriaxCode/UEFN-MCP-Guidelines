"""Generates every texture for the Daily Reward UI (Roblox simulator / tycoon style).

Run:  python gen_art.py            -> writes PNGs into ../art/
All art uses: thick dark outline, vertical gradient, glossy top, hard drop shadow.
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from drawkit import (Canvas, OUTLINE, chunky, chunky_text, hexc, rot, sd_circle, sd_ellipse,
                     sd_poly, sd_rrect, sd_segment, smooth_union, star_pts)

OUT = os.path.join(os.path.dirname(__file__), "..", "art")
os.makedirs(OUT, exist_ok=True)
WHITE = hexc("#ffffff")


def out(img, name):
    p = os.path.join(OUT, name + ".png")
    img.save(p)
    print("wrote", name, img.size)


# ====================================================================== panels

def panel():
    cv = Canvas(1220, 820, ss=2)
    f = lambda x, y: sd_rrect(x, y, 610, 400, 588, 378, 66)
    chunky(cv, f, hexc("#63d4ff"), hexc("#2878de"), outline=10, shadow=16, gloss_alpha=0.30)
    # inner light rim
    d = f(cv.x, cv.y)
    rim = np.clip(cv.cov(np.abs(d + 16) - 3), 0, 1)
    cv.paint(rim, np.array([1, 1, 1, 0.35], np.float32))
    out(cv.image(), "T_DR_Panel")


def inner():
    cv = Canvas(1130, 590, ss=2)
    f = lambda x, y: sd_rrect(x, y, 565, 295, 556, 286, 46)
    d = f(cv.x, cv.y)
    cv.paint(cv.cov(d - 6), hexc("#1d4c8f"))
    cv.paint(cv.cov(d), cv.vgrad(hexc("#eef9ff"), hexc("#c9e8ff"), 10, 580))
    # inset top shadow
    d2 = f(cv.x, cv.y - 12)
    band = np.clip(cv.cov(d) - cv.cov(d2), 0, 1)
    cv.paint(band, np.array([0.05, 0.15, 0.35, 0.25], np.float32))
    out(cv.image(), "T_DR_Inner")


def title():
    cv = Canvas(940, 210, ss=3)
    # ribbon tails (behind)
    for side in (-1, 1):
        cx = 470 + side * 360
        pts = [(cx - 85, 70), (cx + 85, 70), (cx + 85, 170), (cx - 85, 170)]
        notch_x = cx + side * 85
        pts = [(cx - side * 60, 72), (notch_x, 72), (notch_x - side * 38, 121), (notch_x, 170), (cx - side * 60, 170)]
        f = (lambda P: (lambda x, y: sd_poly(x, y, P) - 6))(pts)
        chunky(cv, f, hexc("#ffb72e"), hexc("#e56b00"), outline=8, shadow=8, gloss=False)
    f = lambda x, y: sd_rrect(x, y, 470, 104, 385, 74, 30)
    chunky(cv, f, hexc("#fff06b"), hexc("#ffa516"), outline=9, shadow=10, gloss_alpha=0.45)
    chunky_text(cv, "DAILY REWARDS", 470, 104, 78, stroke=10, top=hexc("#ffffff"), bottom=hexc("#fff1c2"), tracking=2)
    out(cv.image(), "T_DR_Title")


# ====================================================================== cards

CARD = dict(
    locked=(hexc("#b3c4d6"), hexc("#8196ae")),
    today=(hexc("#fff27a"), hexc("#ffad1a")),
    claimed=(hexc("#93f07f"), hexc("#34b23a")),
)
MEGA = dict(
    locked=(hexc("#c3b2e0"), hexc("#8a76b2")),
    today=(hexc("#e29bff"), hexc("#7a2fd0")),
    claimed=(hexc("#93f07f"), hexc("#34b23a")),
)


def lock_icon(cv, cx, cy, s=1.0):
    # shackle
    d_ring = np.abs(sd_circle(cv.x, cv.y, cx, cy - 10 * s, 15 * s)) - 5 * s
    d_ring = np.where(cv.y > cy - 10 * s, 1e3, d_ring)
    body = lambda x, y: sd_rrect(x, y, cx, cy + 8 * s, 21 * s, 17 * s, 6 * s)
    cv.paint(cv.cov(d_ring - 4 * s), OUTLINE)
    cv.paint(cv.cov(d_ring), hexc("#d8dee8"))
    chunky(cv, body, hexc("#ffd64a"), hexc("#e39a00"), outline=4 * s, shadow=3 * s, gloss_alpha=0.4)
    cv.paint(cv.cov(sd_circle(cv.x, cv.y, cx, cy + 6 * s, 4 * s)), OUTLINE)


def card_frame(state, mega=False):
    if mega:
        W, H, hw, hh, r, lab_hh = 350, 540, 160, 255, 42, 30
    else:
        W, H, hw, hh, r, lab_hh = 250, 270, 112, 122, 30, 23
    cv = Canvas(W, H, ss=3)
    cx, cy = W / 2, H / 2 - 4
    top, bot = (MEGA if mega else CARD)[state]
    f = lambda x, y: sd_rrect(x, y, cx, cy, hw, hh, r)
    chunky(cv, f, top, bot, outline=8, shadow=9, gloss_alpha=0.33)
    # label strip
    ly = cy - hh + lab_hh + 12
    fl = lambda x, y: sd_rrect(x, y, cx - 6, ly, hw - 30, lab_hh, lab_hh * 0.6)
    cv.paint(cv.cov(fl(cv.x, cv.y)), np.array([0.02, 0.05, 0.15, 0.28], np.float32))
    if mega and state != "locked":
        # golden inner rim for the mega card
        d = f(cv.x, cv.y)
        cv.paint(np.clip(cv.cov(np.abs(d + 12) - 3.5), 0, 1), hexc("#ffe066", 0.9))
    if state == "locked":
        lock_icon(cv, W - 30, 34, 0.95 if not mega else 1.2)
    name = ("T_DR_Mega_" if mega else "T_DR_Card_") + state.capitalize()
    out(cv.image(), name)
    # white flash silhouette (same shape, no shadow)
    if state == "locked":
        fv = Canvas(W, H, ss=2)
        d = f(fv.x, fv.y)
        fv.paint(fv.cov(d - 8), WHITE)
        out(fv.image(), ("T_DR_Mega_Flash" if mega else "T_DR_Card_Flash"))


def day_labels():
    for n in range(1, 8):
        cv = Canvas(200, 60, ss=4)
        chunky_text(cv, f"DAY {n}", 100, 30, 38, stroke=6, tracking=1)
        out(cv.image(), f"T_DR_Day{n}")
    cv = Canvas(280, 76, ss=4)
    chunky_text(cv, "DAY 7", 140, 38, 50, stroke=7, top=hexc("#fff7cf"), bottom=hexc("#ffd84a"), tracking=2)
    out(cv.image(), "T_DR_Day7Big")


def tag_today():
    # draw the sticker upright on a bigger canvas, then rotate pill AND text together
    cv = Canvas(260, 140, ss=4)
    f = lambda x, y: sd_rrect(x, y, 130, 68, 88, 32, 22)
    chunky(cv, f, hexc("#ff6b6b"), hexc("#d81e3a"), outline=6, shadow=5, gloss_alpha=0.4)
    chunky_text(cv, "CLAIM ME!", 130, 67, 24, stroke=5, tracking=1)
    img = cv.image().rotate(6, resample=Image.BICUBIC, center=(130, 70))
    img = img.crop((22, 14, 238, 126))  # -> 216x112
    out(img, "T_DR_TagToday")


# ====================================================================== icons

def coin(cv, cx, cy, r, star=True):
    f = lambda x, y: sd_circle(x, y, cx, cy, r)
    d = f(cv.x, cv.y)
    cv.paint(cv.cov(sd_circle(cv.x, cv.y, cx, cy + 6, r) - 6), np.array([0, 0, 0, 0.3], np.float32))
    cv.paint(cv.cov(d - 6), OUTLINE)
    cv.paint(cv.cov(d), cv.rgrad(hexc("#fff59a"), hexc("#ffb000"), cx - r * 0.3, cy - r * 0.3, r * 1.5))
    ring = np.abs(sd_circle(cv.x, cv.y, cx, cy, r * 0.74)) - r * 0.05
    cv.paint(cv.cov(ring), hexc("#e38f00", 0.9))
    if star:
        sp = star_pts(cx, cy + r * 0.03, r * 0.48, r * 0.22)
        ds = sd_poly(cv.x, cv.y, sp) - r * 0.03
        cv.paint(cv.cov(ds - 3), hexc("#c97400"))
        cv.paint(cv.cov(ds), cv.vgrad(hexc("#fffbd0"), hexc("#ffd23a"), cy - r * 0.5, cy + r * 0.5))
    # gloss
    gl = sd_ellipse(cv.x, cv.y, cx - r * 0.25, cy - r * 0.45, r * 0.45, r * 0.18)
    cv.paint(cv.cov(gl), np.array([1, 1, 1, 0.55], np.float32))


def icon_coins():
    cv = Canvas(220, 220, ss=4)
    coin(cv, 78, 92, 46, star=False)
    coin(cv, 148, 88, 44, star=False)
    coin(cv, 112, 128, 62)
    out(cv.image(), "T_DR_IconCoins")


def bill(cv, cx, cy, ang, front=False):
    f = lambda x, y: sd_rrect(*rot(x, y, cx, cy, ang), cx, cy, 78, 44, 10)
    chunky(cv, f, hexc("#9cef7a"), hexc("#3fa63a"), outline=6, shadow=5, gloss_alpha=0.3)
    rx, ry = rot(cv.x, cv.y, cx, cy, ang)
    inner = np.abs(sd_rrect(rx, ry, cx, cy, 64, 31, 6)) - 2
    cv.paint(cv.cov(inner), hexc("#e8ffd9", 0.8))
    if front:
        dc = sd_circle(rx, ry, cx, cy, 22)
        cv.paint(cv.cov(dc - 3), hexc("#2c7d2a"))
        cv.paint(cv.cov(dc), hexc("#c9ffb0"))


def icon_cash():
    cv = Canvas(220, 220, ss=4)
    bill(cv, 112, 92, 16)
    bill(cv, 106, 118, -6)
    bill(cv, 112, 140, -18, front=True)
    # $ sign on the front bill
    sub = Canvas(220, 220, ss=4)
    chunky_text(sub, "$", 112, 140, 40, stroke=0, top=hexc("#2c7d2a"), bottom=hexc("#2c7d2a"), shadow=0)
    # rotate the $ layer by -18deg
    img = sub.image().rotate(18, center=(112, 140), resample=Image.BICUBIC)
    base = cv.image()
    base.alpha_composite(img)
    out(base, "T_DR_IconCash")


def icon_gems():
    cv = Canvas(220, 220, ss=4)
    P = [(66, 62), (154, 62), (192, 102), (110, 190), (28, 102)]
    f = lambda x, y: sd_poly(x, y, P) - 2
    chunky(cv, f, hexc("#8ffcff"), hexc("#1b7fe0"), outline=7, shadow=7, gloss=False, inner_shade=False)
    facets = [
        ([(66, 62), (154, 62), (140, 102), (80, 102)], hexc("#ffffff", 0.45)),
        ([(28, 102), (80, 102), (110, 190)], hexc("#0b4fb0", 0.35)),
        ([(140, 102), (192, 102), (110, 190)], hexc("#062f7a", 0.30)),
        ([(80, 102), (140, 102), (110, 190)], hexc("#7fe9ff", 0.25)),
        ([(28, 102), (66, 62), (80, 102)], hexc("#ffffff", 0.25)),
    ]
    for pts, col in facets:
        cv.paint(cv.cov(sd_poly(cv.x, cv.y, pts) + 1), col)
    for a, b in [((80, 102), (110, 190)), ((140, 102), (110, 190)), ((28, 102), (192, 102))]:
        cv.paint(cv.cov(sd_segment(cv.x, cv.y, *a, *b, 1.4)), hexc("#0b3d8f", 0.55))
    sp = star_pts(150, 70, 20, 5, n=4, rot_deg=0)
    cv.paint(cv.cov(sd_poly(cv.x, cv.y, sp)), WHITE)
    out(cv.image(), "T_DR_IconGems")


def icon_boost():
    cv = Canvas(220, 220, ss=4)
    f = lambda x, y: sd_circle(x, y, 110, 112, 78)
    chunky(cv, f, hexc("#c58bff"), hexc("#5a17c4"), outline=7, shadow=7, gloss_alpha=0.32)
    bolt = [(122, 40), (68, 122), (104, 122), (92, 186), (152, 96), (116, 96), (134, 40)]
    fb = lambda x, y: sd_poly(x, y, bolt) - 2
    chunky(cv, fb, hexc("#fff59a"), hexc("#ffb300"), outline=6, shadow=0, gloss_alpha=0.35, inner_shade=False)
    out(cv.image(), "T_DR_IconBoost")


def icon_gift():
    cv = Canvas(220, 220, ss=4)
    chunky(cv, lambda x, y: sd_rrect(x, y, 110, 142, 70, 52, 12), hexc("#ff7b7b"), hexc("#d42a3a"), outline=7, shadow=7)
    chunky(cv, lambda x, y: sd_rrect(x, y, 110, 86, 82, 22, 10), hexc("#ff8f8f"), hexc("#e0303f"), outline=7, shadow=5)
    for rect in [(110, 142, 13, 52), (110, 86, 14, 22)]:
        d = sd_rrect(cv.x, cv.y, *rect, 3)
        cv.paint(cv.cov(d), cv.vgrad(hexc("#fff27a"), hexc("#ffb300"), 64, 194))
    for side in (-1, 1):
        fl = (lambda s: (lambda x, y: sd_ellipse(*rot(x, y, 110 + s * 26, 54, s * 28), 110 + s * 26, 54, 28, 16)))(side)
        chunky(cv, fl, hexc("#fff27a"), hexc("#ffb300"), outline=6, shadow=0, gloss=False)
    chunky(cv, lambda x, y: sd_circle(x, y, 110, 60, 13), hexc("#fff27a"), hexc("#ffb300"), outline=6, shadow=0, gloss=False)
    chunky_text(cv, "?", 110, 146, 54, stroke=6)
    out(cv.image(), "T_DR_IconGift")


def chest(cv, cx, cy, s, body=("#c27a40", "#7a4519"), lid=("#d98d4f", "#8f531f"), trim=("#fff07a", "#e09a00"), gems=False):
    S = lambda v: v * s
    chunky(cv, lambda x, y: sd_rrect(x, y, cx, cy + S(28), S(84), S(48), S(10)), hexc(body[0]), hexc(body[1]), outline=S(7), shadow=S(7))
    chunky(cv, lambda x, y: sd_rrect(x, y, cx, cy - S(22), S(86), S(34), S(30)), hexc(lid[0]), hexc(lid[1]), outline=S(7), shadow=S(4))
    tg = lambda d: cv.vgrad(hexc(trim[0]), hexc(trim[1]), cy - S(56), cy + S(76))
    for bx in (-58, 58):
        d = sd_rrect(cv.x, cv.y, cx + S(bx), cy + S(4), S(9), S(70), S(3))
        cv.paint(cv.cov(d - S(3)), OUTLINE)
        cv.paint(cv.cov(d), tg(d))
    d = sd_rrect(cv.x, cv.y, cx, cy + S(10), S(86), S(6), S(3))
    cv.paint(cv.cov(d - S(3)), OUTLINE)
    cv.paint(cv.cov(d), tg(d))
    chunky(cv, lambda x, y: sd_rrect(x, y, cx, cy + S(16), S(16), S(20), S(5)), hexc(trim[0]), hexc(trim[1]), outline=S(4), shadow=0)
    cv.paint(cv.cov(sd_circle(cv.x, cv.y, cx, cy + S(13), S(4.5))), OUTLINE)
    if gems:
        for gx, col in ((-30, ("#8ffcff", "#1b7fe0")), (30, ("#ff9bf2", "#c21fa8"))):
            P = [(cx + S(gx - 10), cy - S(34)), (cx + S(gx + 10), cy - S(34)), (cx + S(gx + 14), cy - S(26)), (cx + S(gx), cy - S(10)), (cx + S(gx - 14), cy - S(26))]
            chunky(cv, (lambda P: lambda x, y: sd_poly(x, y, P))(P), hexc(col[0]), hexc(col[1]), outline=S(3.5), shadow=0, gloss=False, inner_shade=False)


def icon_chest():
    cv = Canvas(220, 220, ss=4)
    chest(cv, 110, 108, 1.0)
    out(cv.image(), "T_DR_IconChest")


def icon_mega():
    cv = Canvas(300, 300, ss=3)
    # sparkle burst behind
    for i, (sx, sy, r) in enumerate([(60, 70, 22), (245, 85, 18), (250, 215, 14), (48, 210, 12)]):
        sp = star_pts(sx, sy, r, r * 0.25, n=4, rot_deg=0)
        cv.paint(cv.cov(sd_poly(cv.x, cv.y, sp) - 3), OUTLINE)
        cv.paint(cv.cov(sd_poly(cv.x, cv.y, sp)), hexc("#fff59a"))
    chest(cv, 150, 150, 1.35, body=("#9b5cff", "#4a149e"), lid=("#b47bff", "#5a1fb8"), trim=("#fff59a", "#ffb000"), gems=True)
    out(cv.image(), "T_DR_IconMega")


# ====================================================================== small UI bits

def check():
    cv = Canvas(180, 180, ss=4)
    chunky(cv, lambda x, y: sd_circle(x, y, 90, 88, 72), hexc("#7cf06a"), hexc("#21a33a"), outline=8, shadow=8, gloss_alpha=0.35)
    pts = [(55, 92), (80, 118), (127, 64)]
    d = np.minimum(sd_segment(cv.x, cv.y, *pts[0], *pts[1], 11), sd_segment(cv.x, cv.y, *pts[1], *pts[2], 11))
    cv.paint(cv.cov(d - 5), OUTLINE)
    cv.paint(cv.cov(d), WHITE)
    out(cv.image(), "T_DR_Check")


def close_btn():
    cv = Canvas(130, 130, ss=4)
    chunky(cv, lambda x, y: sd_circle(x, y, 65, 62, 52), hexc("#ff7676"), hexc("#d01f2f"), outline=8, shadow=8, gloss_alpha=0.38)
    d = np.minimum(sd_segment(cv.x, cv.y, 45, 42, 85, 82, 9), sd_segment(cv.x, cv.y, 85, 42, 45, 82, 9))
    cv.paint(cv.cov(d - 5), OUTLINE)
    cv.paint(cv.cov(d), WHITE)
    out(cv.image(), "T_DR_Close")


def fire(cv, cx, cy, s):
    P = [(0, -40), (14, -18), (24, -26), (30, -2), (28, 18), (14, 32), (-14, 32), (-28, 18), (-30, -4), (-20, -16), (-14, -4), (-8, -24)]
    P = [(cx + px * s, cy + py * s) for px, py in P]
    f = lambda x, y: sd_poly(x, y, P) - 3 * s
    chunky(cv, f, hexc("#ffd84a"), hexc("#ff4d00"), outline=5 * s, shadow=4 * s, gloss=False)
    Q = [(cx + px * s * 0.5, cy + 10 * s + py * s * 0.5) for px, py in [(0, -36), (16, -6), (14, 20), (-14, 20), (-16, -6)]]
    cv.paint(cv.cov(sd_poly(cv.x, cv.y, Q) - 2 * s), hexc("#fff6a8"))


def clock(cv, cx, cy, r):
    chunky(cv, lambda x, y: sd_circle(x, y, cx, cy, r), hexc("#ffffff"), hexc("#d8e4f5"), outline=5, shadow=4, gloss=False)
    d = np.minimum(sd_segment(cv.x, cv.y, cx, cy, cx, cy - r * 0.62, 3.5), sd_segment(cv.x, cv.y, cx, cy, cx + r * 0.45, cy + r * 0.1, 3.5))
    cv.paint(cv.cov(d), OUTLINE)
    cv.paint(cv.cov(sd_circle(cv.x, cv.y, cx, cy, 4.5)), hexc("#ff4d4d"))


def pills():
    # streak pill
    cv = Canvas(400, 120, ss=3)
    chunky(cv, lambda x, y: sd_rrect(x, y, 200, 56, 186, 46, 46), hexc("#ffbf47"), hexc("#ff6a00"), outline=8, shadow=8, gloss_alpha=0.38)
    fire(cv, 60, 58, 1.05)
    chunky_text(cv, "STREAK", 182, 58, 29, stroke=5)
    # digit well
    cv.paint(cv.cov(sd_rrect(cv.x, cv.y, 316, 56, 62, 32, 24)), np.array([0.25, 0.05, 0, 0.30], np.float32))
    out(cv.image(), "T_DR_StreakPill")
    # timer pill
    cv = Canvas(460, 120, ss=3)
    chunky(cv, lambda x, y: sd_rrect(x, y, 230, 56, 216, 46, 46), hexc("#5a6fb0"), hexc("#28336a"), outline=8, shadow=8, gloss_alpha=0.3)
    clock(cv, 58, 56, 28)
    chunky_text(cv, "NEXT", 142, 58, 28, stroke=5)
    cv.paint(cv.cov(sd_rrect(cv.x, cv.y, 316, 56, 118, 32, 24)), np.array([0, 0, 0.1, 0.35], np.float32))
    out(cv.image(), "T_DR_TimerPill")


def buttons():
    cv = Canvas(480, 160, ss=3)
    chunky(cv, lambda x, y: sd_rrect(x, y, 240, 72, 220, 58, 40), hexc("#8ef567"), hexc("#25a82e"), outline=9, shadow=12, gloss_alpha=0.42)
    chunky_text(cv, "CLAIM!", 240, 72, 66, stroke=9, tracking=3)
    out(cv.image(), "T_DR_BtnClaim")
    cv = Canvas(480, 160, ss=3)
    chunky(cv, lambda x, y: sd_rrect(x, y, 240, 72, 220, 58, 40), hexc("#c4cfdd"), hexc("#7d8aa0"), outline=9, shadow=12, gloss_alpha=0.32)
    chunky_text(cv, "COME BACK", 240, 56, 34, stroke=6, tracking=1)
    chunky_text(cv, "TOMORROW!", 240, 96, 34, stroke=6, tracking=1)
    out(cv.image(), "T_DR_BtnWait")


def popup_banner():
    cv = Canvas(720, 160, ss=3)
    for side in (-1, 1):
        cx = 360 + side * 250
        notch_x = cx + side * 70
        P = [(cx - side * 50, 52), (notch_x, 52), (notch_x - side * 30, 92), (notch_x, 132), (cx - side * 50, 132)]
        chunky(cv, (lambda P: lambda x, y: sd_poly(x, y, P) - 5)(P), hexc("#46e0c4"), hexc("#0f8f7d"), outline=8, shadow=7, gloss=False)
    chunky(cv, lambda x, y: sd_rrect(x, y, 360, 78, 260, 56, 24), hexc("#6cf5d9"), hexc("#11a890"), outline=9, shadow=9, gloss_alpha=0.42)
    chunky_text(cv, "YOU GOT!", 360, 78, 64, stroke=9, tracking=3)
    out(cv.image(), "T_DR_PopupBanner")


def type_labels():
    labels = dict(Coins=("COINS", "#fff4b0", "#ffc61a"), Cash=("CASH", "#d8ffc4", "#5fe04a"),
                  Gems=("GEMS", "#d6fbff", "#4fd2ff"), Boost=("2X BOOST", "#f1ddff", "#c27bff"),
                  Gift=("MYSTERY GIFT", "#ffe0e0", "#ff6b6b"), Chest=("CHEST", "#ffe9cf", "#ff9f40"),
                  Mega=("MEGA CHEST", "#fff4b0", "#ffb300"))
    for key, (txt, a, b) in labels.items():
        cv = Canvas(420, 80, ss=3)
        chunky_text(cv, txt, 210, 40, 50, stroke=8, top=hexc(a), bottom=hexc(b), tracking=2)
        out(cv.image(), f"T_DR_Lbl_{key}")


# ====================================================================== glyphs

GLYPHS = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
          "Plus": "+", "K": "K", "M": "M", "X": "x", "Colon": ":", "Dot": "."}


def glyphs():
    from PIL import ImageDraw, ImageFont
    size, stroke = 64, 9
    f = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", size)
    for name, ch in GLYPHS.items():
        w = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(ch, font=f)) + stroke * 2 + 8
        if ch in ":.":
            w = max(w, 30)
        cv = Canvas(w, 96, ss=4)
        chunky_text(cv, ch, w / 2, 46, size, stroke=stroke, top=hexc("#ffffff"), bottom=hexc("#e2ebff"), shadow=5)
        out(cv.image(), f"T_DR_G_{name}")


# ====================================================================== FX textures

def rays():
    N = 1024
    y, x = np.mgrid[0:N, 0:N].astype(np.float32) + 0.5
    dx, dy = x - N / 2, y - N / 2
    r = np.hypot(dx, dy) / (N / 2)
    th = np.arctan2(dy, dx)
    k = 14
    s = 0.5 + 0.5 * np.cos(th * k)
    ray = np.clip((s - 0.42) / 0.16, 0, 1)
    fall = np.clip(1 - r, 0, 1) ** 1.3 * np.clip(r / 0.12, 0, 1)
    a = ray * fall * 0.85 + np.clip(1 - r / 0.55, 0, 1) ** 2 * 0.35
    img = np.dstack([np.ones_like(a), np.ones_like(a), np.ones_like(a), np.clip(a, 0, 1)])
    out(Image.fromarray((img * 255).astype(np.uint8), "RGBA"), "T_DR_Rays")


def glow():
    N = 512
    y, x = np.mgrid[0:N, 0:N].astype(np.float32) + 0.5
    r = np.hypot(x - N / 2, y - N / 2)
    a = np.exp(-((r - 170) / 55) ** 2) * 0.9 + np.exp(-(r / 190) ** 2) * 0.55
    a *= np.clip((N / 2 - r) / 20, 0, 1)
    img = np.dstack([np.ones_like(a)] * 3 + [np.clip(a, 0, 1)])
    out(Image.fromarray((img * 255).astype(np.uint8), "RGBA"), "T_DR_Glow")


def sparkle():
    cv = Canvas(128, 128, ss=4)
    g = np.exp(-(np.hypot(cv.x - 64, cv.y - 64) / 22) ** 2) * 0.7
    cv.paint(g, WHITE)
    sp = star_pts(64, 64, 60, 9, n=4, rot_deg=0)
    cv.paint(cv.cov(sd_poly(cv.x, cv.y, sp)), WHITE)
    out(cv.image(), "T_DR_Sparkle")


def confetti():
    N = 512
    cv = Canvas(N, N, ss=2)
    rnd = random.Random(7)
    cols = ["#ff4d6d", "#ffd23f", "#3bceac", "#4d9de0", "#b56bff", "#ff8c42", "#7bf05a"]
    for _ in range(85):
        px, py = rnd.uniform(0, N), rnd.uniform(0, N)
        col = hexc(rnd.choice(cols))
        kind = rnd.random()
        ang = rnd.uniform(0, 180)
        for ox in (-N, 0, N):
            for oy in (-N, 0, N):
                cx, cy = px + ox, py + oy
                if not (-30 < cx < N + 30 and -30 < cy < N + 30):
                    continue
                if kind < 0.65:
                    d = sd_rrect(*rot(cv.x, cv.y, cx, cy, ang), cx, cy, 5, 10, 2)
                else:
                    d = sd_circle(cv.x, cv.y, cx, cy, 6)
                cv.paint(cv.cov(d), col)
    out(cv.image(), "T_DR_Confetti")


def white():
    out(Image.new("RGBA", (16, 16), (255, 255, 255, 255)), "T_DR_White")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    jobs = [panel, inner, title, day_labels, tag_today, icon_coins, icon_cash, icon_gems, icon_boost,
            icon_gift, icon_chest, icon_mega, check, close_btn, pills, buttons, popup_banner, type_labels,
            glyphs, rays, glow, sparkle, confetti, white]
    for st in ("locked", "today", "claimed"):
        jobs.append((lambda s: (lambda: card_frame(s)))(st))
        jobs.append((lambda s: (lambda: card_frame(s, mega=True)))(st))
    for j in jobs:
        if only and j.__name__ not in only and j.__name__ != "<lambda>":
            continue
        j()
