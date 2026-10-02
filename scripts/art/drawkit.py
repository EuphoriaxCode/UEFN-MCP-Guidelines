"""drawkit: tiny antialiased SDF renderer for chunky Roblox-style UI art.

All coordinates are in FINAL pixels; shapes are rendered at `ss`x supersampling
and box-filtered down, which gives clean antialiased edges and outlines.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_BLACK = "C:/Windows/Fonts/ariblk.ttf"

# ---------------------------------------------------------------- colours

def hexc(h, a=1.0):
    h = h.lstrip("#")
    return np.array([int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0, a], np.float32)

OUTLINE = hexc("#14182b")

# ---------------------------------------------------------------- canvas


class Canvas:
    def __init__(self, w, h, ss=4):
        self.w, self.h, self.ss = w, h, ss
        W, H = w * ss, h * ss
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        self.x = (xs + 0.5) / ss
        self.y = (ys + 0.5) / ss
        self.rgba = np.zeros((H, W, 4), np.float32)  # premultiplied

    # composite a colour field (H,W,4 straight alpha OR (4,) constant) with coverage mask
    def paint(self, cov, color):
        if cov is None:
            return
        if np.ndim(color) == 1:
            col = np.broadcast_to(color, self.rgba.shape)
        else:
            col = color
        a = np.clip(cov, 0, 1) * col[..., 3]
        src = np.empty_like(self.rgba)
        src[..., :3] = col[..., :3] * a[..., None]
        src[..., 3] = a
        self.rgba = src + self.rgba * (1.0 - a[..., None])

    def paint_under(self, cov, color):
        """Paint behind existing content (for shadows/glows)."""
        old = self.rgba.copy()
        self.rgba[:] = 0
        self.paint(cov, color)
        a = old[..., 3:4]
        self.rgba = old + self.rgba * (1.0 - a)

    def image(self):
        ss = self.ss
        H, W = self.h, self.w
        r = self.rgba.reshape(H, ss, W, ss, 4).mean(axis=(1, 3))
        a = r[..., 3:4]
        rgb = np.where(a > 1e-5, r[..., :3] / np.maximum(a, 1e-5), 0)
        out = np.concatenate([rgb, a], axis=-1)
        return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")

    # coverage helper (d in final px)
    def cov(self, d):
        return np.clip(0.5 - d * self.ss, 0.0, 1.0)

    # vertical gradient colour field between y0..y1
    def vgrad(self, c0, c1, y0, y1):
        t = np.clip((self.y - y0) / max(1e-5, (y1 - y0)), 0, 1)[..., None]
        return c0 * (1 - t) + c1 * t

    def rgrad(self, c0, c1, cx, cy, r):
        t = np.clip(np.hypot(self.x - cx, self.y - cy) / r, 0, 1)[..., None]
        return c0 * (1 - t) + c1 * t


# ---------------------------------------------------------------- SDFs (final px)

def rot(x, y, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    dx, dy = x - cx, y - cy
    return cx + dx * c + dy * s, cy - dx * s + dy * c


def sd_rrect(x, y, cx, cy, hw, hh, r):
    qx = np.abs(x - cx) - (hw - r)
    qy = np.abs(y - cy) - (hh - r)
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r


def sd_circle(x, y, cx, cy, r):
    return np.hypot(x - cx, y - cy) - r


def sd_ellipse(x, y, cx, cy, rx, ry):
    # approximate (good enough for chunky art)
    k = np.hypot((x - cx) / rx, (y - cy) / ry)
    return (k - 1.0) * min(rx, ry)


def sd_poly(x, y, pts):
    pts = np.asarray(pts, np.float32)
    n = len(pts)
    d = np.full(x.shape, 1e9, np.float32)
    sgn = np.ones(x.shape, np.float32)
    for i in range(n):
        ax, ay = pts[i - 1]
        bx, by = pts[i]
        ex, ey = bx - ax, by - ay
        wx, wy = x - ax, y - ay
        t = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey + 1e-9), 0, 1)
        dx, dy = wx - ex * t, wy - ey * t
        d = np.minimum(d, dx * dx + dy * dy)
        c1 = y >= ay
        c2 = y < by
        c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        sgn = np.where(flip, -sgn, sgn)
    return sgn * np.sqrt(d)


def sd_segment(x, y, ax, ay, bx, by, r):
    ex, ey = bx - ax, by - ay
    wx, wy = x - ax, y - ay
    t = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey + 1e-9), 0, 1)
    return np.hypot(wx - ex * t, wy - ey * t) - r


def star_pts(cx, cy, ro, ri, n=5, rot_deg=-90):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot_deg + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def smooth_union(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


# ---------------------------------------------------------------- styled shape

def chunky(cv, sdf_fn, top, bottom, outline=8.0, shadow=8.0, gloss=True, ocol=OUTLINE,
           y0=None, y1=None, gloss_alpha=0.38, inner_shade=True):
    """Draw a Roblox-style chunky shape: drop shadow, thick outline, vertical gradient,
    glossy top highlight and a soft inner bottom shade."""
    d = sdf_fn(cv.x, cv.y)
    inside = d < 0
    ys = cv.y[inside] if inside.any() else np.array([0.0, 1.0])
    y0 = float(ys.min()) if y0 is None else y0
    y1 = float(ys.max()) if y1 is None else y1
    if shadow:
        ds = sdf_fn(cv.x, cv.y - shadow)
        cv.paint(cv.cov(ds - outline), np.array([0, 0, 0, 0.35], np.float32))
    cv.paint(cv.cov(d - outline), ocol)
    cv.paint(cv.cov(d), cv.vgrad(top, bottom, y0, y1))
    if inner_shade:
        # darker band along the bottom inside edge
        dd = sdf_fn(cv.x, cv.y + outline * 0.9)
        band = np.clip(cv.cov(d) - cv.cov(dd), 0, 1)
        cv.paint(band, np.array([0, 0, 0, 0.18], np.float32))
    if gloss:
        h = (y1 - y0)
        dg = sdf_fn(cv.x, cv.y + min(h * 0.06, 16.0))  # shape shifted up a little
        # clip to the inside of the shape (inset) so the gloss can never poke out above the outline
        mask = cv.cov(dg + outline * 0.6) * cv.cov(d + max(4.0, outline * 0.5)) \
            * np.clip((y0 + h * 0.48 - cv.y) / (h * 0.25), 0, 1)
        cv.paint(mask, np.array([1, 1, 1, gloss_alpha], np.float32))
    return d


# ---------------------------------------------------------------- text

def text_mask(cv, text, cx, cy, size, stroke, font=FONT_BLACK, tracking=0):
    """Returns (fill_cov, stroke_cov) arrays at supersampled resolution, centred on (cx,cy)."""
    ss = cv.ss
    f = ImageFont.truetype(font, int(size * ss))
    st = int(stroke * ss)
    # measure
    tmp = Image.new("L", (10, 10))
    dr = ImageDraw.Draw(tmp)
    if tracking:
        widths = [dr.textlength(ch, font=f) for ch in text]
        total = sum(widths) + tracking * ss * (len(text) - 1)
    else:
        total = dr.textlength(text, font=f)
    asc, desc = f.getmetrics()
    H, W = cv.rgba.shape[:2]
    fill = Image.new("L", (W, H), 0)
    strk = Image.new("L", (W, H), 0)
    df, dsk = ImageDraw.Draw(fill), ImageDraw.Draw(strk)
    x0 = cx * ss - total / 2
    # vertical centre on cap height
    bbox = f.getbbox("HD0")
    cap_mid = (bbox[1] + bbox[3]) / 2
    y0 = cy * ss - cap_mid
    if tracking:
        x = x0
        for ch, wch in zip(text, widths):
            dsk.text((x, y0), ch, font=f, fill=255, stroke_width=st, stroke_fill=255)
            df.text((x, y0), ch, font=f, fill=255)
            x += wch + tracking * ss
    else:
        dsk.text((x0, y0), text, font=f, fill=255, stroke_width=st, stroke_fill=255)
        df.text((x0, y0), text, font=f, fill=255)
    return np.asarray(fill, np.float32) / 255.0, np.asarray(strk, np.float32) / 255.0


def chunky_text(cv, text, cx, cy, size, stroke=None, top=hexc("#ffffff"), bottom=hexc("#dfe9ff"),
                ocol=OUTLINE, shadow=None, tracking=0, rotate=0):
    stroke = stroke if stroke is not None else max(3, size * 0.12)
    shadow = shadow if shadow is not None else max(2, size * 0.08)
    fill, strk = text_mask(cv, text, cx, cy, size, stroke, tracking=tracking)
    ss = cv.ss
    sh = int(round(shadow * ss))
    shadow_m = np.zeros_like(strk)
    if sh > 0:
        shadow_m[sh:, :] = strk[:-sh, :]
    cv.paint(shadow_m, np.array([0, 0, 0, 0.45], np.float32))
    cv.paint(strk, ocol)
    cv.paint(fill, cv.vgrad(top, bottom, cy - size * 0.45, cy + size * 0.45))


def save(img, path):
    img.save(path)
    return path
