"""E09: procedural OBJ -> StaticMesh -> parameterised material -> Scene Graph mesh component with per-instance colour.

Run from the repo root:  python -X utf8 experiments/e09_mesh_material.py
Each step prints what it got back so failures are easy to log.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cli"))
from uefncli import api, sg  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = sg.content_root()  # e.g. /ca93dbca-6f58-4ce8-9bd2-c953b1864acf (new projects mount content under the plugin GUID)
MESHES = f"{ROOT}/SGKit/Meshes"
MATS = f"{ROOT}/SGKit/Materials"
MT = "material"


def step(title, fn):
    print(f"\n== {title}")
    try:
        r = fn()
        s = json.dumps(r, ensure_ascii=False) if not isinstance(r, str) else r
        print("  ->", s[:700])
        return r
    except Exception as e:
        print("  !! FAILED:", str(e)[:1200])
        return None


def exists(path):
    return api.tool("asset", "exists", {"path": path})


for f in (MESHES, MATS):
    step(f"create_folder {f}", lambda f=f: api.tool("asset", "create_folder", {"path": f}))

# 1) import meshes
for shape in ("cube", "sphere", "cylinder", "wedge", "torus"):
    name = f"SM_SG_{shape}"
    if exists(f"{MESHES}/{name}"):
        print(f"\n== {name} exists, skipping import")
        continue
    src = os.path.abspath(os.path.join(REPO, "assets", "meshes", f"SG_{shape}.obj"))
    step(f"import {name}", lambda name=name, src=src: api.tool("mesh", "import_file", {
        "folder_path": MESHES, "asset_name": name, "source_file": src,
        "import_materials": False, "import_textures": False, "combine_meshes": True}))

cube = {"refPath": f"{MESHES}/SM_SG_cube.SM_SG_cube"}
step("cube bounds", lambda: api.tool("mesh", "get_bounds", {"mesh": cube}))
slots = step("cube material slots", lambda: api.tool("mesh", "get_material_slots", {"mesh": cube}))

# 2) one parameterised surface material
MAT = f"{MATS}/M_SG_Color"


def make_material():
    if exists(MAT):
        return "exists"
    m = api.tool(MT, "create_material", {"folder_path": MATS, "asset_name": "M_SG_Color"})

    def node(cls, x, y, props=None):
        e = api.tool(MT, "add_expression", {"material_or_function": m,
                                            "expression_class": {"refPath": "/Script/Engine.MaterialExpression" + cls},
                                            "x": x, "y": y})
        if props:
            api.tool("object", "set_properties", {"instance": e, "values": json.dumps(props)})
        return e

    color = node("VectorParameter", -600, 0, {"parameterName": "Color", "defaultValue": {"r": 0.8, "g": 0.8, "b": 0.8, "a": 1}})
    glow = node("ScalarParameter", -600, 200, {"parameterName": "Glow", "defaultValue": 0.0})
    rough = node("ScalarParameter", -600, 320, {"parameterName": "Roughness", "defaultValue": 0.5})
    metal = node("ScalarParameter", -600, 440, {"parameterName": "Metallic", "defaultValue": 0.0})
    mul = node("Multiply", -300, 150)
    api.tool(MT, "connect_expressions", {"from_expression": color, "from_output_name": "", "to_expression": mul, "to_input_name": "A"})
    api.tool(MT, "connect_expressions", {"from_expression": glow, "from_output_name": "", "to_expression": mul, "to_input_name": "B"})
    api.tool(MT, "connect_to_output", {"expression": color, "output_name": "", "material_property": "MP_BaseColor"})
    api.tool(MT, "connect_to_output", {"expression": mul, "output_name": "", "material_property": "MP_EmissiveColor"})
    api.tool(MT, "connect_to_output", {"expression": rough, "output_name": "", "material_property": "MP_Roughness"})
    api.tool(MT, "connect_to_output", {"expression": metal, "output_name": "", "material_property": "MP_Metallic"})
    api.tool(MT, "recompile", {"material_or_function": m})
    return m


step("material M_SG_Color", make_material)

# 3) a few instances
COLORS = {"Red": (1, 0.05, 0.05), "Green": (0.05, 1, 0.1), "Blue": (0.05, 0.2, 1), "Gold": (1, 0.7, 0.1)}
for cname, (r, g, b) in COLORS.items():
    path = f"{MATS}/MI_SG_{cname}"
    if exists(path):
        continue

    def mk(cname=cname, r=r, g=g, b=b):
        mi = api.tool("mi", "create", {"folder_path": MATS, "asset_name": f"MI_SG_{cname}",
                                       "parent": {"refPath": f"{MAT}.M_SG_Color"}})
        api.tool("mi", "set_vector_parameter", {"instance": mi, "name": "Color", "value": {"r": r, "g": g, "b": b, "a": 1}})
        api.tool("mi", "set_scalar_parameter", {"instance": mi, "name": "Glow", "value": 2.0 if cname == "Gold" else 0.0})
        return mi
    step(f"MI_SG_{cname}", mk)

# 4) assign the base material to every mesh's first slot
for shape in ("cube", "sphere", "cylinder", "wedge", "torus"):
    mesh = {"refPath": f"{MESHES}/SM_SG_{shape}.SM_SG_{shape}"}
    s = api.tool("mesh", "get_material_slots", {"mesh": mesh}) if exists(f"{MESHES}/SM_SG_{shape}") else []
    print(f"\n== slots of SM_SG_{shape}: {s}")
    if s:
        slot = s[0] if isinstance(s[0], str) else (s[0].get("slotName") or s[0].get("name") or json.dumps(s[0]))
        step(f"set_material {shape}.{slot}", lambda mesh=mesh, slot=slot: api.tool("mesh", "set_material", {
            "mesh": mesh, "slot_name": slot, "material": {"refPath": f"{MAT}.M_SG_Color"}}))

step("save", lambda: api.tool("asset", "save_assets", {"asset_paths": []}))
step("BuildAll", lambda: api.tool("verse", "BuildAll", {}))
step("component classes SM_SG", lambda: [c["className"] + " " + c["classPath"]["refPath"]
                                          for c in api.tool("entity", "ListComponentClasses", {"nameFilter": "SM_SG"})])
