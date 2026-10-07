"""Scene Graph helpers over ValkyrieToolset.EntityToolset.

Entities are addressed by *name paths*: "Showroom/BackWall" (short names = display names without the
editor's `_<hash>_<n>` suffix), by a full display name, or by a raw refPath.
Components are addressed by friendly class name or alias ("cube", "light", "lamp_toggle_component").
"""
import json
import os
import re
import tempfile

from . import api
from .xform import Xf

E = "entity"
ENTITY_CLASS = {"refPath": "/EntityFramework/_Verse/VNI/Entity.entity"}
SUFFIX = re.compile(r"_[a-z0-9]{10,16}_\d+$")
COMP_CACHE = os.path.join(tempfile.gettempdir(), "uefn_component_classes.json")

ALIASES = {
    "cube": "BasicShapes_cube", "sphere": "BasicShapes_sphere", "cylinder": "BasicShapes_cylinder",
    "cone": "BasicShapes_cone", "plane": "BasicShapes_plane",
    "light": "sphere_light_component", "pointlight": "sphere_light_component", "spot": "spot_light_component",
    "rectlight": "rect_light_component", "capsulelight": "capsule_light_component", "sun": "directional_light_component",
    "interact": "basic_interactable_component", "text": "text_display_component",
    "keyframed": "KeyframedMovement_keyframed_movement_component", "particles": "particle_system_component",
    "decal": "decal_component", "tags": "tag_component", "rigidbody": "rigid_body_component",
    "physics": "physics_component", "camera": "perspective_camera_component",
}


def short(name):
    return SUFFIX.sub("", name)


class Scene:
    """One snapshot of the level's entity forest (refreshed on demand)."""

    def __init__(self):
        self.refresh()

    def refresh(self):
        self.all = api.tool(E, "FindEntities", {})
        self.by_ref = {e["entity"]["refPath"]: e for e in self.all}

    def parent_ref(self, ref):
        p = ref.rsplit(".", 1)[0]
        return p if p in self.by_ref else None

    def children(self, ref=None):
        return [e for e in self.all if self.parent_ref(e["entity"]["refPath"]) == ref]

    def path_of(self, ref):
        parts = []
        while ref:
            parts.append(short(self.by_ref[ref]["displayName"]))
            ref = self.parent_ref(ref)
        return "/".join(reversed(parts))

    def resolve(self, spec, required=True):
        """name path / display name / refPath -> entity info dict"""
        if isinstance(spec, dict):
            return self.by_ref.get(spec.get("refPath")) or {"entity": spec}
        if spec in self.by_ref:
            return self.by_ref[spec]
        for e in self.all:
            if e["displayName"] == spec:
                return e
        cur = None
        for part in spec.strip("/").split("/"):
            kids = self.children(cur)
            hit = [k for k in kids if short(k["displayName"]) == part] or \
                  [k for k in kids if short(k["displayName"]).lower() == part.lower()]
            if not hit and cur is None:  # allow a bare unique name anywhere in the tree
                hit = [k for k in self.all if short(k["displayName"]) == part]
            if len(hit) != 1:
                if required:
                    raise KeyError(f"entity '{spec}': {'no match' if not hit else str(len(hit)) + ' matches'} for '{part}'")
                return None
            cur = hit[0]["entity"]["refPath"]
        return self.by_ref[cur]


def component_classes(refresh=False):
    if not refresh and os.path.exists(COMP_CACHE):
        with open(COMP_CACHE) as f:
            return json.load(f)
    c = api.tool(E, "ListComponentClasses", {})
    with open(COMP_CACHE, "w") as f:
        json.dump(c, f)
    return c


def comp_class(name):
    """friendly name / alias / refPath -> class refPath"""
    if name.startswith("/"):
        return name
    name = ALIASES.get(name, name)
    for refresh in (False, True):
        cls = component_classes(refresh)
        exact = [c for c in cls if c["className"] == name]
        if not exact:
            exact = [c for c in cls if c["className"].endswith("-" + name) or c["className"].endswith("_" + name)]
        if len(exact) >= 1:
            return exact[0]["classPath"]["refPath"]
    raise KeyError(f"component class '{name}' not found (try `uefn sg classes {name}`)")


def comps(ent):
    return api.tool(E, "GetComponents", {"entity": ent["entity"] if "entity" in ent else ent})


def find_comp(ent, name):
    cls = comp_class(name)
    for c in comps(ent):
        if c["componentClass"]["refPath"] == cls:
            return c
    for c in comps(ent):  # loose: friendly-name prefix (componentName is like "BasicShapes_cube_0")
        if c["componentName"].startswith(ALIASES.get(name, name)):
            return c
    return None


def world(ent):
    return Xf.from_json(api.tool(E, "GetEntityTransform", {"entity": ent["entity"]}))


def set_world(ent, xf):
    return api.tool(E, "SetEntityTransform", {"entity": ent["entity"], "transform": xf.to_json()})


def local(scene, ent):
    w = world(ent)
    p = scene.parent_ref(ent["entity"]["refPath"])
    return scene.by_ref[p] and world(scene.by_ref[p]).relative(w) if p else w


def set_local(scene, ent, xf):
    p = scene.parent_ref(ent["entity"]["refPath"])
    w = world(scene.by_ref[p]).compose(xf) if p else xf
    return set_world(ent, w)


def jval(v):
    """python value -> JSON string for SetComponentProperty (strings that already look like JSON pass through)"""
    if isinstance(v, str):
        s = v.strip()
        if s[:1] in "{[\"" or s in ("true", "false") or re.fullmatch(r"-?\d+(\.\d+)?([eE]-?\d+)?", s):
            return s
        return json.dumps(v)
    return json.dumps(v)


def set_prop(comp, prop, value):
    return api.tool(E, "SetComponentProperty", {"component": comp["component"], "propertyName": prop, "value": jval(value)})


def get_prop(comp, prop):
    return api.tool(E, "GetComponentProperty", {"component": comp["component"], "propertyName": prop})


def create(name, parent=None, xf=None, cls=None):
    a = {"entityClass": {"refPath": cls} if cls else ENTITY_CLASS, "name": name, "transform": (xf or Xf()).to_json()}
    if parent:
        a["parentEntity"] = parent["entity"]
    return api.tool(E, "CreateEntity", a)


def add_comp(ent, name):
    return api.tool(E, "AddComponent", {"entity": ent["entity"], "componentClass": {"refPath": comp_class(name)}})


# ---------------------------------------------------------------- declarative specs
#
# {"name": "Lamp", "at": [x,y,z], "rot": [pitch,yaw,roll], "scale": [sx,sy,sz] | s,
#  "class": "<entity class refPath or prefab>",            (optional)
#  "components": {"cube": {}, "sphere_light_component": {"Intensity": 200, "ColorFilter": {"r":1,"g":0,"b":0}}},
#  "children": [ ...same shape... ],
#  "repeat": {"count": 6, "step": [200,0,0], "name": "Pillar_{i}"}   (optional, expands into siblings)}
# Transforms of children are LOCAL to the parent. apply() is idempotent: existing entities (matched by
# name under the same parent) are updated, missing ones are created. With prune=True, unlisted children are deleted.

def _expand(nodes):
    out = []
    for n in nodes:
        r = n.get("repeat")
        if not r:
            out.append(n)
            continue
        for i in range(int(r["count"])):
            m = json.loads(json.dumps(n))
            m.pop("repeat")
            m["name"] = r.get("name", n["name"] + "_{i}").format(i=i, n=i + 1)
            base = m.get("at", [0, 0, 0])
            step = r.get("step", [0, 0, 0])
            m["at"] = [b + s * i for b, s in zip(base, step)]
            if "yaw_step" in r:
                rot = list(m.get("rot", [0, 0, 0]))
                rot[1] += r["yaw_step"] * i
                m["rot"] = rot
            out.append(m)
    return out


def _spec_xf(n):
    from .xform import parse_vec
    s = n.get("scale", 1)
    return Xf(parse_vec(n.get("at"), (0, 0, 0)), parse_vec(n.get("rot"), (0, 0, 0)), parse_vec(s, (1, 1, 1)))


def apply(spec, parent_path=None, prune=False, log=print, scene=None):
    scene = scene or Scene()
    nodes = _expand(spec if isinstance(spec, list) else [spec])
    parent = scene.resolve(parent_path) if parent_path else None
    parent_world = world(parent) if parent else Xf()
    stats = {"created": 0, "updated": 0, "deleted": 0}
    pref = parent["entity"]["refPath"] if parent else None
    existing = {short(k["displayName"]): k for k in scene.children(pref)}
    if pref is None:  # top level: only consider entities directly under the LevelEntity
        existing = {short(k["displayName"]): k for k in scene.all if scene.parent_ref(k["entity"]["refPath"]) is None}
    for n in nodes:
        lx = _spec_xf(n)
        ent = existing.get(n["name"])
        if ent is None:
            ent = create(n["name"], parent, lx, n.get("class"))
            stats["created"] += 1
            log(f"+ {(parent_path + '/') if parent_path else ''}{n['name']}")
        else:
            set_world(ent, parent_world.compose(lx))
            stats["updated"] += 1
        have = {c["componentClass"]["refPath"]: c for c in comps(ent)}
        for cname, props in (n.get("components") or {}).items():
            cls = comp_class(cname)
            c = have.get(cls) or add_comp(ent, cname)
            for p, v in (props or {}).items():
                r = set_prop(c, p, v)
                if r is False:
                    log(f"  ! {n['name']}.{cname}.{p} rejected")
        if n.get("children") is not None:
            scene.refresh()
            path = ((parent_path + "/") if parent_path else "") + n["name"]
            sub = apply(n["children"], path, prune, log, scene)
            for k in stats:
                stats[k] += sub[k]
    if prune:
        keep = {n["name"] for n in nodes}
        for name, ent in existing.items():
            if name not in keep and pref is not None:
                api.tool(E, "DeleteEntity", {"entity": ent["entity"]})
                stats["deleted"] += 1
                log(f"- {name}")
    scene.refresh()
    return stats


# ---------------------------------------------------------------- spec prefabs
#
# UEFN has no tool to create prefab assets, so templates live in JSON:
#   template  = a spec (above) whose root is the "prefab root"
#   instances = sidecar <template>.instances.json: {"<Parent/Name>": {"at":..,"rot":..,"scale":..,"overrides":{...}}}
#   overrides = {"Bulb": {"sphere_light_component": {"Intensity": 400}}, "": {"lamp_toggle_component": {...}}}
#               keys are child paths relative to the instance root ("" = root itself)
# `stamp` creates/updates one instance and records it; `propagate` re-applies the template to every recorded
# instance, so template edits flow to all instances while each keeps its overrides.

def _node_at(spec, rel):
    n = spec
    for part in [p for p in rel.split("/") if p]:
        kids = {c["name"]: c for c in _expand(n.get("children") or [])}
        if part not in kids:
            raise KeyError(f"override path '{rel}': no child '{part}' in template")
        # materialise expanded repeats so the override lands on the concrete node
        n["children"] = list(kids.values())
        n = kids[part]
    return n


def with_overrides(template, name, at=None, rot=None, scale=None, overrides=None):
    spec = json.loads(json.dumps(template))
    spec["name"] = name
    if at is not None:
        spec["at"] = list(at)
    if rot is not None:
        spec["rot"] = list(rot)
    if scale is not None:
        spec["scale"] = scale
    for rel, comps_ in (overrides or {}).items():
        node = _node_at(spec, rel)
        node.setdefault("components", {})
        for cname, props in comps_.items():
            node["components"].setdefault(cname, {})
            node["components"][cname] = dict(node["components"][cname] or {}, **props)
    return spec


def sidecar(template_path):
    return template_path[:-5] + ".instances.json" if template_path.endswith(".json") else template_path + ".instances.json"


def load_instances(template_path):
    p = sidecar(template_path)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


def stamp(template_path, inst_path, at=None, rot=None, scale=None, overrides=None, log=print):
    with open(template_path, encoding="utf-8") as f:
        template = json.load(f)
    insts = load_instances(template_path)
    rec = insts.get(inst_path, {})
    if at is not None:
        rec["at"] = list(at)
    if rot is not None:
        rec["rot"] = list(rot)
    if scale is not None:
        rec["scale"] = scale
    if overrides:
        merged = rec.get("overrides", {})
        for rel, cs in overrides.items():
            for cname, props in cs.items():
                merged.setdefault(rel, {}).setdefault(cname, {}).update(props)
        rec["overrides"] = merged
    parent, _, name = inst_path.rpartition("/")
    spec = with_overrides(template, name, rec.get("at"), rec.get("rot"), rec.get("scale"), rec.get("overrides"))
    st = apply(spec, parent or None, log=log)
    insts[inst_path] = rec
    with open(sidecar(template_path), "w", encoding="utf-8") as f:
        json.dump(insts, f, indent=1)
    return st


def propagate(template_path, prune=False, log=print):
    with open(template_path, encoding="utf-8") as f:
        template = json.load(f)
    total = {"created": 0, "updated": 0, "deleted": 0, "instances": 0}
    scene = Scene()
    for inst_path, rec in load_instances(template_path).items():
        parent, _, name = inst_path.rpartition("/")
        spec = with_overrides(template, name, rec.get("at"), rec.get("rot"), rec.get("scale"), rec.get("overrides"))
        st = apply(spec, parent or None, prune=prune, log=log, scene=scene)
        for k in st:
            total[k] += st[k]
        total["instances"] += 1
    return total


def parse_override(s):
    """'Bulb.sphere_light_component.Intensity=400' -> ('Bulb', comp, prop, value); root: '.lamp_toggle_component.X=1'"""
    lhs, _, val = s.partition("=")
    rel, comp, prop = lhs.rsplit(".", 2) if lhs.count(".") >= 2 else ("",) + tuple(lhs.split(".", 1))
    try:
        v = json.loads(val)
    except ValueError:
        v = val
    return rel.replace(".", "/"), comp, prop, v


def dump(scene, ent, with_props=False):
    lx = local(scene, ent)
    n = {"name": short(ent["displayName"]), "at": [round(v, 3) for v in lx.loc]}
    if any(abs(v) > 1e-4 for v in lx.rot):
        n["rot"] = [round(v, 3) for v in lx.rot]
    if any(abs(v - 1) > 1e-4 for v in lx.scale):
        n["scale"] = [round(v, 4) for v in lx.scale]
    cls = ent["entityClass"]["refPath"]
    if cls != ENTITY_CLASS["refPath"]:
        n["class"] = cls
    cs = {}
    for c in comps(ent):
        name = c["componentName"].rsplit("_", 1)[0] if re.search(r"_\d+$", c["componentName"]) else c["componentName"]
        if name == "transform_component":
            continue
        props = {}
        if with_props:
            for p in api.tool(E, "ListComponentProperties", {"component": c["component"]}):
                if not p.get("bReadOnly") and "refPath" not in str(p.get("value")):
                    try:
                        props[p["name"]] = json.loads(p["value"])
                    except (ValueError, TypeError):
                        props[p["name"]] = p["value"]
        cs[name] = props
    if cs:
        n["components"] = cs
    kids = scene.children(ent["entity"]["refPath"])
    if kids:
        n["children"] = [dump(scene, k, with_props) for k in kids]
    return n
