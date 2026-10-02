# UMG builder used inside the UEFN MCP sandbox (ProgrammaticToolset.execute_tool_script).
# Concatenate in front of a build script. Only json + execute_tool are available there.
import json
U = 'UMGToolSet.UMGToolSet.'
OT = 'editor_toolset.toolsets.object.ObjectTools.'
AT = 'editor_toolset.toolsets.asset.AssetTools.'
V = 'VerseFieldsToolset.VerseFieldsToolset.'
MV = 'MVVMToolset.MVVMToolset.'
E = 'EditorToolset.EditorAppToolset.'
D = '/Custombuilds/DailyReward/UI'
TX = D + '/Textures/'
MAT = D + '/Materials/'
ERR = []


def T(n, a):
    return execute_tool(n, json.dumps(a))


def res(n):
    if n.startswith('MI_'):
        return {'refPath': MAT + 'Instances/' + n + '.' + n}
    if n.startswith('M_'):
        return {'refPath': MAT + n + '.' + n}
    return {'refPath': TX + n + '.' + n}


def C(h='HAlign_Center', v='VAlign_Center', pad=None):
    d = {'horizontalAlignment': h, 'verticalAlignment': v}
    if pad is not None:
        d['padding'] = {'left': pad[0], 'top': pad[1], 'right': pad[2], 'bottom': pad[3]}
    return d


FILL = {'horizontalAlignment': 'HAlign_Fill', 'verticalAlignment': 'VAlign_Fill'}


def CV(x, y, z=0, auto=True):
    return {'layoutData': {'anchors': {'minimum': {'x': 0.5, 'y': 0.5}, 'maximum': {'x': 0.5, 'y': 0.5}},
                           'alignment': {'x': 0.5, 'y': 0.5},
                           'offsets': {'left': x, 'top': y, 'right': 0, 'bottom': 0}},
            'bAutoSize': auto, 'zOrder': z}


def CVFULL(z=0):
    return {'layoutData': {'anchors': {'minimum': {'x': 0, 'y': 0}, 'maximum': {'x': 1, 'y': 1}},
                           'alignment': {'x': 0, 'y': 0},
                           'offsets': {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}},
            'bAutoSize': False, 'zOrder': z}


def SIZE(w=None, h=None):
    d = {}
    if w is not None:
        d.update({'bOverride_WidthOverride': True, 'widthOverride': float(w)})
    if h is not None:
        d.update({'bOverride_HeightOverride': True, 'heightOverride': float(h)})
    return d


class WB:
    def __init__(s, name):
        p = D + '/' + name
        if T(AT + 'exists', {'path': p})['returnValue']:
            T(AT + 'delete', {'path': p})
        s.name = name
        s.W = T(U + 'CreateWidgetBlueprint', {'folderPath': D, 'assetName': name,
                                             'parentClass': {'refPath': '/Script/UMG.UserWidget'}})['returnValue']
        T(E + 'OpenEditorForAsset', {'assetPath': p})  # makes Verse fields real (42.30)

    def setp(s, obj, props, what):
        if not props:
            return
        try:
            T(OT + 'set_properties', {'instance': obj, 'values': json.dumps(props)})
        except Exception as e:
            ERR.append([s.name, what, str(e)[-300:]])

    def add(s, cls, name, parent=None, props=None, slot=None):
        if '/' not in cls:
            cls = ('/Script/UIFramework.UIFrameworkCustomButtonWidget' if cls == 'CustomButton' else '/Script/UMG.' + cls)
        a = {'widgetBlueprint': s.W, 'widgetClass': {'refPath': cls}, 'widgetDisplayName': name}
        if parent is not None:
            a['parentWidget'] = parent
        r = T(U + 'AddWidget', a)['returnValue']
        s.setp(r['widget'], props, name + '.props')
        if slot and r.get('slot'):
            s.setp(r['slot'], slot, name + '.slot')
        return r['widget']

    def img(s, name, parent, resname, w, h, slot=None, props=None):
        p = {'brush': {'resourceObject': res(resname), 'imageSize': {'x': w, 'y': h}, 'drawAs': 'Image'},
             'visibility': 'HitTestInvisible'}
        if props:
            p.update(props)
        return s.add('Image', name, parent, p, slot)

    def empty(s, name, parent):
        return s.add('SizeBox', name, parent, SIZE(0, 0))

    def field(s, n, t, d=''):
        T(V + 'AddVerseField', {'widgetBlueprint': s.W, 'fieldName': n, 'spec': {
            'type': t, 'eventParameterTypes': [], 'defaultValue': d, 'visibility': 'Public',
            'writeAccess': '', 'bIsVar': t != 'event'}})

    def bind(s, f, widget, prop, conv=''):
        try:
            return T(MV + 'CreateViewBinding', {'widgetBlueprint': s.W, 'sourceContext': None, 'sourcePropertyPath': f,
                                                'destinationContext': widget, 'destinationPropertyPath': prop,
                                                'conversionName': conv})['returnValue']
        except Exception as e:
            ERR.append([s.name, 'bind ' + f + '->' + prop, str(e)[-300:]])

    def event(s, f, widget, ev):
        try:
            return T(MV + 'CreateViewEventBinding', {'widgetBlueprint': s.W, 'eventContext': widget,
                                                     'eventPropertyPath': ev, 'destinationContext': None,
                                                     'destinationPropertyPath': f})['returnValue']
        except Exception as e:
            ERR.append([s.name, 'event ' + ev + '->' + f, str(e)[-300:]])

    def glyphs(s, prefix, n, parent, overlap=7):
        cls = D + '/WBP_DR_Glyph.WBP_DR_Glyph_C'
        out = []
        for i in range(1, n + 1):
            g = s.add(cls, prefix + 'W' + str(i), parent, {'visibility': 'HitTestInvisible'},
                      C(pad=(-overlap, 0, -overlap, 0)))
            s.field(prefix + str(i), 'int', '16')
            s.bind(prefix + str(i), g, 'G')
            out.append(g)
        return out

    def done(s):
        ok = None
        try:
            ok = T(U + 'CompileWidgetBlueprint', {'widgetBlueprint': s.W})['returnValue']
        except Exception as e:
            ERR.append([s.name, 'compile', str(e)[-600:]])
        T(AT + 'save_assets', {'asset_paths': [D + '/' + s.name]})
        return ok
