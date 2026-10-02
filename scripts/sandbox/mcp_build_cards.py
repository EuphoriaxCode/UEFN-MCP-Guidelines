# Builds WBP_DR_Card and WBP_DR_MegaCard (run after mcp_umglib.py in the same globals).
#
# Tree:  Root(SizeBox, container) > RootOverlay
#          GlowSwitch [none | glow | none]               (State)
#          AnimBox(SizeBox W/H/Angle) > ScaleBox(Fill) > Design(SizeBox) > Content(Overlay)
#             FrameSwitch [locked | today | claimed]     (State)
#             DaySwitch / DayLabel                       (DayIndex)
#             IconSwitch [7 bobbing icon MIs]            (IconIndex, IconOpacity)
#             NumBox > ScaleBox > StackBox > 5 glyphs    (G1..G5)
#             TagSwitch [none | "CLAIM ME!" | none]      (State)
#             Flash (white silhouette)                   (Flash)
#             CheckBox(SizeBox) > Check                  (CheckSize)


def build_card(name, mega):
    if mega:
        DW, DH, CW, CH = 350, 540, 440, 640
    else:
        DW, DH, CW, CH = 250, 270, 340, 360
    b = WB(name)
    root = b.add('SizeBox', 'Root', None, SIZE(CW, CH))
    ov = b.add('Overlay', 'RootOverlay', root)
    gs = b.add('WidgetSwitcher', 'GlowSwitch', ov, {'visibility': 'HitTestInvisible'}, FILL)
    b.empty('GlowNone0', gs)
    b.img('Glow', gs, 'MI_DR_Glow_Purple' if mega else 'MI_DR_Glow_Gold', CW, CH)
    b.empty('GlowNone2', gs)
    anim = b.add('SizeBox', 'AnimBox', ov, SIZE(DW, DH), C())
    sc = b.add('ScaleBox', 'AnimScale', anim, {'stretch': 'Fill'})
    design = b.add('SizeBox', 'Design', sc, SIZE(DW, DH))
    ct = b.add('Overlay', 'Content', design)
    fs = b.add('WidgetSwitcher', 'FrameSwitch', ct, {'visibility': 'HitTestInvisible'}, FILL)
    pre = 'T_DR_Mega_' if mega else 'T_DR_Card_'
    for st in ('Locked', 'Today', 'Claimed'):
        b.img('Frame' + st, fs, pre + st, DW, DH)
    ds = None
    if mega:
        b.img('DayLabel', ct, 'T_DR_Day7Big', 280, 76, C('HAlign_Center', 'VAlign_Top', (0, 16, 12, 0)))
    else:
        ds = b.add('WidgetSwitcher', 'DaySwitch', ct, {'visibility': 'HitTestInvisible'},
                   C('HAlign_Center', 'VAlign_Top', (0, 10, 12, 0)))
        for d in range(1, 8):
            b.img('Day%d' % d, ds, 'T_DR_Day%d' % d, 200, 60)
    isz = 250 if mega else 150
    isw = b.add('WidgetSwitcher', 'IconSwitch', ct, {'visibility': 'HitTestInvisible'},
                C(pad=(0, 0, 0, 40 if mega else 22)))
    for n in ('Coins', 'Cash', 'Gems', 'Boost', 'Gift', 'Chest', 'Mega'):
        b.img('Icon' + n, isw, 'MI_DR_Icon_' + n, isz, isz)
    nb = b.add('SizeBox', 'NumBox', ct, SIZE(300 if mega else 220, 66 if mega else 46),
               C('HAlign_Center', 'VAlign_Bottom', (0, 0, 0, 40 if mega else 22)))
    ns = b.add('ScaleBox', 'NumScale', nb, {'stretch': 'ScaleToFit'})
    row = b.add('StackBox', 'NumRow', ns, {'orientation': 'Orient_Horizontal'})
    b.glyphs('G', 5, row)
    ts = b.add('WidgetSwitcher', 'TagSwitch', ct, {'visibility': 'HitTestInvisible'},
               C('HAlign_Center', 'VAlign_Top', (0, -46, 0, 0)))
    b.empty('TagNone0', ts)
    b.img('Tag', ts, 'MI_DR_Tag', 170, 72)
    b.empty('TagNone2', ts)
    fl = b.img('FlashImg', ct, 'T_DR_Mega_Flash' if mega else 'T_DR_Card_Flash', DW, DH, FILL, {'renderOpacity': 0.0})
    ck = b.add('SizeBox', 'CheckBox', ct, SIZE(0, 0),
               C('HAlign_Right', 'VAlign_Bottom', (0, 0, -10, 70 if mega else 48)))
    b.img('Check', ck, 'T_DR_Check', 180, 180)

    b.field('State', 'int', '0')
    b.bind('State', fs, 'ActiveWidgetIndex')
    b.bind('State', gs, 'ActiveWidgetIndex')
    b.bind('State', ts, 'ActiveWidgetIndex')
    b.field('CardW', 'float', str(DW))
    b.bind('CardW', anim, 'WidthOverride')
    b.field('CardH', 'float', str(DH))
    b.bind('CardH', anim, 'HeightOverride')
    b.field('CardAngle', 'float', '0')
    b.bind('CardAngle', anim, 'SetRenderTransformAngle')
    b.field('Flash', 'float', '0')
    b.bind('Flash', fl, 'RenderOpacity')
    b.field('CheckSize', 'float', '0')
    b.bind('CheckSize', ck, 'WidthOverride')
    b.bind('CheckSize', ck, 'HeightOverride')
    b.field('IconIndex', 'int', '0')
    b.bind('IconIndex', isw, 'ActiveWidgetIndex')
    b.field('IconOpacity', 'float', '1')
    b.bind('IconOpacity', isw, 'RenderOpacity')
    if ds is not None:
        b.field('DayIndex', 'int', '0')
        b.bind('DayIndex', ds, 'ActiveWidgetIndex')
    b.field('CardOpacity', 'float', '1')
    b.bind('CardOpacity', root, 'RenderOpacity')
    return b.done()


def main():
    r = {'card': build_card('WBP_DR_Card', False), 'mega': build_card('WBP_DR_MegaCard', True), 'err': ERR}
    return r
