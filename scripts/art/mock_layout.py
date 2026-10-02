"""Composes the generated art into a 1920x1080 mockup (static preview of the final layout)."""
import os
from PIL import Image, ImageDraw

A = os.path.join(os.path.dirname(__file__), "..", "art")
W, H = 1920, 1080
CX, CY = W // 2, H // 2


def img(n):
    return Image.open(os.path.join(A, n + ".png")).convert("RGBA")


def place(base, im, x, y, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if alpha < 1.0:
        a = im.split()[3].point(lambda v: int(v * alpha))
        im.putalpha(a)
    base.alpha_composite(im, (int(CX + x - im.width / 2), int(CY + y - im.height / 2)))


def number(base, text, x, y, scale=1.0):
    names = {"+": "Plus", "x": "X", ":": "Colon", ".": "Dot"}
    ims = [img("T_DR_G_" + names.get(c, c)) for c in text]
    ims = [i.resize((int(i.width * scale), int(i.height * scale)), Image.LANCZOS) for i in ims]
    tw = sum(i.width for i in ims) - int(14 * scale) * (len(ims) - 1)
    cx = x - tw / 2
    for i in ims:
        base.alpha_composite(i, (int(CX + cx), int(CY + y - i.height / 2)))
        cx += i.width - int(14 * scale)


def main():
    base = Image.new("RGBA", (W, H), (70, 140, 90, 255))
    base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 150)))
    rays = img("T_DR_Rays")
    rays = Image.merge("RGBA", (*[c.point(lambda v: v) for c in rays.split()[:3]], rays.split()[3].point(lambda v: int(v * 0.45))))
    place(base, rays.resize((1500, 1500)), 0, 0)
    place(base, img("T_DR_Panel"), 0, 30)
    place(base, img("T_DR_Inner"), 0, 10)
    place(base, img("T_DR_Title"), 0, -365)
    for sx, sy in [(-470, -400), (470, -330), (-560, 300)]:
        place(base, img("T_DR_Sparkle"), sx, sy, 0.6)
    place(base, img("T_DR_Close"), 560, -340)
    days = [("Coins", "+500"), ("Cash", "+1K"), ("Gems", "+5"), ("Coins", "+2.5K"), ("Boost", "x2"), ("Gems", "+10")]
    states = ["Claimed", "Claimed", "Today", "Locked", "Locked", "Locked"]
    pos = [(-410, -138), (-160, -138), (90, -138), (-410, 150), (-160, 150), (90, 150)]
    for i, ((icon, amt), st, (x, y)) in enumerate(zip(days, states, pos)):
        if st == "Today":
            g = img("T_DR_Glow")
            g = Image.merge("RGBA", (*Image.new("RGB", g.size, (255, 220, 60)).split(), g.split()[3]))
            place(base, g, x, y, 0.85)
        place(base, img("T_DR_Card_" + st), x, y)
        place(base, img(f"T_DR_Day{i + 1}"), x - 6, y - 96)
        place(base, img("T_DR_Icon" + icon), x, y - 2, 0.68, 0.6 if st == "Locked" else 1)
        number(base, amt, x, y + 82, 0.55)
        if st == "Claimed":
            place(base, img("T_DR_Check"), x + 62, y + 30, 0.55)
        if st == "Today":
            place(base, img("T_DR_TagToday"), x, y - 150, 0.8)
    place(base, img("T_DR_Mega_Locked"), 395, 6)
    place(base, img("T_DR_Day7Big"), 395, -210)
    place(base, img("T_DR_IconMega"), 395, -20, 0.95)
    number(base, "+10K", 395, 150, 0.75)
    place(base, img("T_DR_StreakPill"), -400, 375, 0.8)
    number(base, "3", -400 + 0.8 * 116, 375, 0.55)
    place(base, img("T_DR_BtnClaim"), 0, 370, 0.9)
    place(base, img("T_DR_TimerPill"), 410, 375, 0.8)
    number(base, "23:59:12", 410 + 0.8 * 86, 375, 0.42)
    base.convert("RGB").save(os.path.join(A, "..", "mockup_main.png"))

    # popup mock
    base = Image.new("RGBA", (W, H), (70, 140, 90, 255))
    base.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 170)))
    r2 = img("T_DR_Rays")
    r2 = Image.merge("RGBA", (*Image.new("RGB", r2.size, (255, 214, 64)).split(), r2.split()[3]))
    place(base, r2.resize((1100, 1100)), 0, 0)
    place(base, img("T_DR_Confetti").resize((1920, 1920)).crop((0, 0, 1920, 1080)), 0, 0)
    place(base, img("T_DR_PopupBanner"), 0, -250)
    place(base, img("T_DR_IconCoins"), 0, -10, 1.5)
    number(base, "+2.5K", 0, 200, 1.0)
    place(base, img("T_DR_Lbl_Coins"), 0, 290, 0.9)
    base.convert("RGB").save(os.path.join(A, "..", "mockup_popup.png"))


if __name__ == "__main__":
    main()
