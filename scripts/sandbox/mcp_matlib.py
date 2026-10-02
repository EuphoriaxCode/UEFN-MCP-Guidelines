# Material-graph builder used inside the UEFN MCP sandbox (ProgrammaticToolset.execute_tool_script).
# This file is concatenated in front of the per-run script; it only uses json + execute_tool.
import json
MT = 'editor_toolset.toolsets.material.MaterialTools.'
OT = 'editor_toolset.toolsets.object.ObjectTools.'
AT = 'editor_toolset.toolsets.asset.AssetTools.'
MI = 'editor_toolset.toolsets.material_instance.MaterialInstanceTools.'
F = '/Custombuilds/DailyReward/UI/Materials'
TX = '/Custombuilds/DailyReward/UI/Textures/'


def T(n, a):
    return execute_tool(n, json.dumps(a))


def tref(n):
    return {'refPath': TX + n + '.' + n}


class G:
    def __init__(s, name):
        p = F + '/' + name
        if T(AT + 'exists', {'path': p})['returnValue']:
            T(AT + 'delete', {'path': p})
        s.m = T(MT + 'create_material', {'folder_path': F, 'asset_name': name})['returnValue']
        T(OT + 'set_properties', {'instance': s.m, 'values': json.dumps(
            {'materialDomain': 'MD_UI', 'blendMode': 'BLEND_Translucent', 'shadingModel': 'MSM_Unlit'})})
        s.k = 0
        s._uv = None
        s._t = None

    def node(s, cls, props=None):
        s.k += 1
        x = T(MT + 'add_expression', {'material_or_function': s.m,
                                      'expression_class': {'refPath': '/Script/Engine.MaterialExpression' + cls},
                                      'x': -260 * (s.k % 10) - 300, 'y': 140 * (s.k // 10)})['returnValue']
        if props:
            T(OT + 'set_properties', {'instance': x, 'values': json.dumps(props)})
        return x

    def link(s, src, dst, pin):
        ref, out = src if isinstance(src, tuple) else (src, '')
        T(MT + 'connect_expressions', {'from_expression': ref, 'from_output_name': out,
                                       'to_expression': dst, 'to_input_name': pin})

    def val(s, v):
        if isinstance(v, (int, float)):
            return s.node('Constant', {'r': float(v)})
        return v

    def bin(s, cls, a, b, pa='A', pb='B'):
        x = s.node(cls)
        s.link(s.val(a), x, pa)
        s.link(s.val(b), x, pb)
        return x

    def add(s, a, b): return s.bin('Add', a, b)
    def sub(s, a, b): return s.bin('Subtract', a, b)
    def mul(s, a, b): return s.bin('Multiply', a, b)
    def div(s, a, b): return s.bin('Divide', a, b)
    def mx(s, a, b): return s.bin('Max', a, b)
    def app(s, a, b): return s.bin('AppendVector', a, b)
    def pw(s, a, b): return s.bin('Power', a, b, 'Base', 'Exp')

    def un(s, cls, a):
        x = s.node(cls)
        s.link(s.val(a), x, '')
        return x

    def sin(s, a): return s.un('Sine', a)          # period 1  -> sin(2*pi*a)
    def cos(s, a): return s.un('Cosine', a)
    def frac(s, a): return s.un('Frac', a)
    def abs(s, a): return s.un('Abs', a)
    def sat(s, a): return s.un('Saturate', a)

    def mask(s, a, ch):
        x = s.node('ComponentMask', {'r': 'r' in ch, 'g': 'g' in ch, 'b': 'b' in ch, 'a': 'a' in ch})
        s.link(s.val(a), x, '')
        return x

    def lerp(s, a, b, t):
        x = s.node('LinearInterpolate')
        s.link(s.val(a), x, 'A')
        s.link(s.val(b), x, 'B')
        s.link(s.val(t), x, 'Alpha')
        return x

    def uv(s):
        if s._uv is None:
            s._uv = s.node('TextureCoordinate')
        return s._uv

    def time(s):
        if s._t is None:
            s._t = s.node('Time')
        return s._t

    def scalar(s, name, v):
        return s.node('ScalarParameter', {'parameterName': name, 'defaultValue': float(v)})

    def vec(s, name, c):
        return s.node('VectorParameter', {'parameterName': name,
                                          'defaultValue': {'r': c[0], 'g': c[1], 'b': c[2], 'a': c[3]}})

    def tex(s, name, texname, uvs):
        x = s.node('TextureSampleParameter2D', {'parameterName': name, 'texture': tref(texname)})
        s.link(uvs, x, 'UVs')
        return x

    def rotator(s, coord, tm, speed=1.0):
        x = s.node('Rotator', {'centerX': 0.5, 'centerY': 0.5, 'speed': speed})
        s.link(coord, x, 'Coordinate')
        s.link(tm, x, 'Time')
        return x

    def scale_uv(s, uvs, k):  # (uv-0.5)/k + 0.5
        return s.add(s.div(s.sub(uvs, 0.5), k), 0.5)

    def out(s, e, prop):
        ref, o = e if isinstance(e, tuple) else (e, '')
        T(MT + 'connect_to_output', {'expression': ref, 'output_name': o, 'material_property': prop})

    def finish(s, emissive, opacity):
        s.out(emissive, 'MP_EmissiveColor')
        s.out(opacity, 'MP_Opacity')
        T(MT + 'layout_expressions', {'material_or_function': s.m})
        T(MT + 'recompile', {'material_or_function': s.m})
        return s.m


def make_mi(name, parent, textures=None, scalars=None, vectors=None):
    p = F + '/Instances/' + name
    if T(AT + 'exists', {'path': p})['returnValue']:
        T(AT + 'delete', {'path': p})
    mi = T(MI + 'create', {'folder_path': F + '/Instances', 'asset_name': name,
                           'parent': {'refPath': F + '/' + parent + '.' + parent}})['returnValue']
    for k, v in (textures or {}).items():
        T(MI + 'set_texture_parameter', {'instance': mi, 'name': k, 'value': tref(v)})
    for k, v in (scalars or {}).items():
        T(MI + 'set_scalar_parameter', {'instance': mi, 'name': k, 'value': float(v)})
    for k, v in (vectors or {}).items():
        T(MI + 'set_vector_parameter', {'instance': mi, 'name': k, 'value': {'r': v[0], 'g': v[1], 'b': v[2], 'a': v[3]}})
    return mi
