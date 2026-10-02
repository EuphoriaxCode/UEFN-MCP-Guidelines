# Run inside UEFN MCP sandbox AFTER mcp_matlib.py (concatenate both).
# Builds the 7 animated UI materials. All animation is client-side (Time node) => perfectly smooth.
# Sine/Cosine use period 1 (one cycle per input unit), so "Speed" params are in Hz.


def m_rays():
    g = G('M_DR_Rays')
    t = g.mul(g.time(), g.scalar('Speed', 0.25))
    tx = g.tex('Tex', 'T_DR_Rays', g.rotator(g.uv(), t))
    tint = g.vec('Tint', (1.0, 1.0, 1.0, 0.45))
    return g.finish(g.mul((tx, 'RGB'), (tint, 'RGB')), g.mul((tx, 'A'), (tint, 'A')))


def m_glow():
    g = G('M_DR_Glow')
    s = g.sin(g.add(g.mul(g.time(), g.scalar('Speed', 0.8)), g.scalar('Phase', 0.0)))
    k = g.add(g.mul(s, g.scalar('Amount', 0.07)), 1.0)
    tx = g.tex('Tex', 'T_DR_Glow', g.scale_uv(g.uv(), k))
    tint = g.vec('Tint', (1.0, 0.82, 0.2, 1.0))
    a = g.mul(g.mul((tx, 'A'), (tint, 'A')), g.add(g.mul(s, 0.28), 0.72))
    return g.finish(g.mul((tx, 'RGB'), (tint, 'RGB')), a)


def m_bob():
    g = G('M_DR_Bob')
    t = g.time()
    ph = g.scalar('Phase', 0.0)
    sp = g.scalar('Speed', 0.55)
    s1 = g.sin(g.add(g.mul(t, sp), ph))
    s2 = g.sin(g.add(g.mul(g.mul(t, sp), 0.5), ph))
    ang = g.mul(s2, g.scalar('Wobble', 0.012))          # turns
    c, s = g.cos(ang), g.sin(ang)
    p = g.sub(g.uv(), 0.5)
    px, py = g.mask(p, 'r'), g.mask(p, 'g')
    rx = g.add(g.mul(c, px), g.mul(s, py))
    ry = g.add(g.sub(g.mul(c, py), g.mul(s, px)), g.mul(s1, g.scalar('Bob', 0.035)))
    uv2 = g.add(g.app(rx, ry), 0.5)
    tx = g.tex('Tex', 'T_DR_IconCoins', uv2)
    tint = g.vec('Tint', (1.0, 1.0, 1.0, 1.0))
    return g.finish(g.mul((tx, 'RGB'), (tint, 'RGB')), g.mul((tx, 'A'), (tint, 'A')))


def m_shine():
    g = G('M_DR_Shine')
    t = g.time()
    k = g.add(g.mul(g.sin(g.mul(t, g.scalar('BreathSpeed', 0.9))), g.scalar('Breath', 0.022)), 1.0)
    uv2 = g.scale_uv(g.uv(), k)
    tx = g.tex('Tex', 'T_DR_BtnClaim', uv2)
    p = g.sub(g.mul(g.frac(g.mul(t, g.scalar('SweepSpeed', 0.4))), 2.6), 0.6)
    sd = g.div(g.add(g.mask(uv2, 'r'), g.mul(g.mask(uv2, 'g'), 0.35)), 1.35)
    band = g.sat(g.sub(1.0, g.div(g.abs(g.sub(sd, p)), g.scalar('Width', 0.10))))
    band = g.mul(g.mul(band, band), g.scalar('Strength', 0.7))
    em = g.add((tx, 'RGB'), g.mul(band, (tx, 'A')))
    return g.finish(em, (tx, 'A'))


def m_sparkle():
    g = G('M_DR_Sparkle')
    t = g.time()
    rot = g.rotator(g.uv(), t, 0.6)
    tw = g.pw(g.abs(g.sin(g.add(g.mul(t, g.scalar('Speed', 0.6)), g.scalar('Phase', 0.0)))), 2.0)
    k = g.add(g.mul(tw, 0.8), 0.2)
    tx = g.tex('Tex', 'T_DR_Sparkle', g.scale_uv(rot, k))
    tint = g.vec('Tint', (1.0, 0.97, 0.8, 1.0))
    return g.finish(g.mul((tx, 'RGB'), (tint, 'RGB')), g.mul(g.mul((tx, 'A'), tw), (tint, 'A')))


def m_confetti():
    g = G('M_DR_Confetti')
    t = g.time()
    uvt = g.mul(g.uv(), g.mask(g.vec('Tiling', (3.75, 2.1, 0.0, 0.0)), 'rg'))
    fall = g.scalar('Fall', 0.22)
    vy = g.mask(uvt, 'g')
    o1 = g.app(g.mul(g.sin(g.add(g.mul(t, 0.35), g.mul(vy, 0.6))), 0.05), g.mul(g.mul(t, fall), -1.0))
    tx1 = g.tex('Tex', 'T_DR_Confetti', g.add(uvt, o1))
    o2 = g.app(g.add(g.mul(g.sin(g.add(g.mul(t, 0.27), g.mul(vy, 0.45))), 0.06), 0.37),
               g.sub(0.21, g.mul(g.mul(t, fall), 1.4)))
    tx2 = g.tex('Tex', 'T_DR_Confetti', g.add(g.mul(uvt, 1.55), o2))
    tint = g.vec('Tint', (1.0, 1.0, 1.0, 1.0))
    col = g.lerp((tx2, 'RGB'), (tx1, 'RGB'), (tx1, 'A'))
    a = g.mul(g.mx((tx1, 'A'), g.mul((tx2, 'A'), 0.85)), (tint, 'A'))
    return g.finish(col, a)


def m_stripes():
    g = G('M_DR_Stripes')
    t = g.time()
    uv = g.uv()
    tx = g.tex('Tex', 'T_DR_Inner', uv)
    d = g.sub(g.mul(g.add(g.mul(g.mask(uv, 'r'), g.scalar('Aspect', 1.915)), g.mask(uv, 'g')), g.scalar('Freq', 7.0)),
              g.mul(t, g.scalar('Speed', 0.25)))
    tri = g.mul(g.abs(g.sub(g.frac(d), 0.5)), 2.0)
    st = g.sat(g.mul(g.sub(tri, 0.5), 12.0))
    em = g.mul((tx, 'RGB'), g.sub(1.0, g.mul(st, g.scalar('Strength', 0.06))))
    return g.finish(em, (tx, 'A'))


def run():
    made = []
    for f in (m_rays, m_glow, m_bob, m_shine, m_sparkle, m_confetti, m_stripes):
        made.append(f()['refPath'])
    T(AT + 'save_assets', {'asset_paths': []})
    return {'made': made}
